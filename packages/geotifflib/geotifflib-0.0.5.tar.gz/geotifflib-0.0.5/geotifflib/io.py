#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Tuple, Optional, Union, Callable, List

import numpy as np
from osgeo import gdal, osr


def read_geo(
    file_path: Union[Path, str]
) -> Tuple[Optional[np.ndarray], Optional[tuple], Optional[str]]:
    """
    读取 GeoTIFF 文件，返回数据 (np.ndarray)、地理变换 (tuple) 和投影 (str)。
    读出的数据默认形状：若是多波段则 [bands, height, width]，单波段则 [height, width]。
    """
    # 如果输入是 Path，则转换为字符串
    if isinstance(file_path, Path):
        file_path = str(file_path)

    ds = gdal.Open(file_path, gdal.GA_ReadOnly)
    if ds is None:
        print(f"[read_geo] Cannot open {file_path}")
        return None, None, None

    width = ds.RasterXSize
    height = ds.RasterYSize

    # ReadAsArray 会根据波段数量返回不同形状：
    #  - 多波段：shape=(bands, height, width)
    #  - 单波段：shape=(height, width)
    data = ds.ReadAsArray(0, 0, width, height)
    geotransform = ds.GetGeoTransform()
    projection = ds.GetProjection()

    ds = None  # 关闭数据集
    return data, geotransform, projection


def save(
    save_path: Union[Path, str],
    data: np.ndarray,
    geotransform: tuple,
    projection: str,
    output_dtype=gdal.GDT_Float32
) -> None:
    """
    使用内存映射的方式保存为 GeoTIFF，默认带 LZW 压缩，并指定 PHOTOMETRIC=MINISBLACK 以避免 ExtraSamples 警告。
    
    :param save_path: 输出文件路径 (Path | str)
    :param data: np.ndarray, [bands, height, width] 或 [height, width]
    :param geotransform: 地理变换 (tuple)
    :param projection: 投影 (WKT str)
    :param output_dtype: GDAL 数据类型 (默认为 gdal.GDT_Float32)
    """
    if isinstance(save_path, Path):
        save_path = str(save_path)

    # 判断数据维度决定波段数 / 行列数
    if len(data.shape) == 2:
        im_bands = 1
        im_height, im_width = data.shape
    else:
        im_bands, im_height, im_width = data.shape

    # 1) 创建内存数据集（MEM driver）
    mem_driver = gdal.GetDriverByName("MEM")
    mem_ds = mem_driver.Create('', im_width, im_height, im_bands, output_dtype)
    if not mem_ds:
        raise IOError("Cannot create in-memory dataset.")

    # 设置地理信息
    mem_ds.SetGeoTransform(geotransform)
    mem_ds.SetProjection(projection)

    # 将数据写入内存数据集
    if im_bands == 1:
        mem_ds.GetRasterBand(1).WriteArray(data)
    else:
        for i in range(im_bands):
            mem_ds.GetRasterBand(i + 1).WriteArray(data[i])

    # 2) 使用 CreateCopy 或 CreateCopy-like 方法将内存数据集保存到硬盘
    #    这里使用 CreateCopy，带上创建选项 COMPRESS=LZW + PHOTOMETRIC=MINISBLACK
    file_driver = gdal.GetDriverByName("GTiff")
    creation_opts = [
        "COMPRESS=LZW",              # 压缩
        "PHOTOMETRIC=MINISBLACK"     # 避免 ExtraSamples 警告
    ]
    file_driver.CreateCopy(save_path, mem_ds, 0, creation_opts)

    # 清理内存数据集
    mem_ds = None


def save_without_memory_mapping(
    save_path: Union[Path, str],
    data: np.ndarray,
    geotransform: tuple,
    projection: str,
    output_dtype=gdal.GDT_Float32,
) -> None:
    """
    直接将数据写入到 GeoTIFF 文件（无内存映射）。
    同样指定 PHOTOMETRIC=MINISBLACK，避免多波段时出现 ExtraSamples 警告。

    :param save_path: 输出的 GeoTIFF 文件路径
    :param data: np.ndarray, shape=[bands, height, width] 或 [height, width]
    :param geotransform: (tuple) 地理变换
    :param projection: (str) 投影 (WKT)
    :param output_dtype: (GDAL DataType) 输出数据类型
    """
    if isinstance(save_path, Path):
        save_path = str(save_path)

    # 判断数据维度
    if len(data.shape) == 2:
        im_bands = 1
        im_height, im_width = data.shape
    else:
        im_bands, im_height, im_width = data.shape

    driver = gdal.GetDriverByName("GTiff")
    creation_opts = [
        "COMPRESS=LZW",
        "PHOTOMETRIC=MINISBLACK"
    ]
    out_ds = driver.Create(
        save_path,
        im_width,
        im_height,
        im_bands,
        output_dtype,
        options=creation_opts
    )
    if not out_ds:
        raise IOError(f"Cannot create file {save_path}")

    # 设置地理信息
    out_ds.SetGeoTransform(geotransform)
    out_ds.SetProjection(projection)

    # 写数组到波段
    if im_bands == 1:
        out_ds.GetRasterBand(1).WriteArray(data)
    else:
        for i in range(im_bands):
            out_ds.GetRasterBand(i + 1).WriteArray(data[i])

    out_ds.FlushCache()
    out_ds = None


def read(file_path: Union[Path, str]) -> Optional[np.ndarray]:
    """
    仅返回数据本身（np.ndarray），不返回投影和地理变换。
    """
    if isinstance(file_path, Path):
        file_path = str(file_path)

    ds = gdal.Open(file_path, gdal.GA_ReadOnly)
    if ds is None:
        print(f"[read] Cannot open {file_path}")
        return None

    w = ds.RasterXSize
    h = ds.RasterYSize
    arr = ds.ReadAsArray(0, 0, w, h)
    ds = None
    return arr


def hsi_to_rgb(
    hsi_data: np.ndarray,
    r_band_index: int,
    g_band_index: int,
    b_band_index: int,
) -> np.ndarray:
    """
    将高光谱数据指定的波段索引提取为 RGB，并进行简单归一化和 gamma 调整。
    返回 shape = [height, width, 3]
    """
    # 提取RGB波段 (bands, height, width) -> 选取3个波段
    rgb_ = hsi_data[[r_band_index, g_band_index, b_band_index], :, :]

    # NaN -> 0
    rgb_ = np.nan_to_num(rgb_)
    rgb_[rgb_ < 0] = 0

    # 简单归一化
    max_value = (np.mean(rgb_[1]) + 3 * np.std(rgb_[1])) * 1.5
    min_value = np.min(rgb_)
    print(f"[hsi_to_rgb] max: {max_value:.2f}, min: {min_value:.2f}")
    rgb_ = (rgb_ - min_value) / (max_value - min_value)
    rgb_ = np.clip(rgb_, 0, 1)

    # gamma校正
    rgb_ = rgb_ ** 0.6

    # 背景(=0)设为白色
    rgb_[rgb_ == 0] = 1

    # 转为 [height, width, 3]
    return np.moveaxis(rgb_, 0, -1)


def make_format_coord(
    geotransform_: tuple
) -> Callable[[float, float], str]:
    """
    返回一个可用于格式化坐标的函数，用于可视化时在 matplotlib 中显示地理坐标。

    :param geotransform_: 6 元素地理变换 (origin_x, pixel_size_x, 0, origin_y, 0, pixel_size_y)
    :return: function(x, y) -> str
    """
    def format_coord(x, y):
        x_origin = geotransform_[0]
        y_origin = geotransform_[3]
        x_pixel = geotransform_[1]
        y_pixel = geotransform_[5]

        lon = x_pixel * x + x_origin
        lat = y_pixel * y + y_origin
        return f"x={lon:.3f}, y={lat:.3f}"

    return format_coord


def set_background_to_zero(
    data: np.ndarray,
    start_band: int,
    end_band: int,
) -> np.ndarray:
    """
    在指定的波段范围内，如果像素点各波段之和<0，则在所有波段将该像素置为0。
    形状: data [bands, height, width]
    """
    if start_band < 0 or end_band >= data.shape[0]:
        raise ValueError("Band index out of range.")

    selected_bands = data[start_band:end_band + 1]  # 选取部分波段
    sum_over_bands = np.sum(selected_bands, axis=0)  # [height, width]
    mask = sum_over_bands < 0

    data[:, mask] = 0
    return data


def set_nodata(
    input_file: Union[Path, str],
    number: float = 0
) -> None:
    """
    将 TIFF 图像中某个数值设置为 NoData，用于后续合并（merge）时自动忽略该值。

    :param input_file: 需要修改的 TIFF 文件
    :param number: 要设置为 NoData 的值
    """
    if isinstance(input_file, Path):
        input_file = str(input_file)

    ds = gdal.Open(input_file, gdal.GA_Update)
    if ds is None:
        print(f"[set_nodata] 无法打开文件: {input_file}")
        return

    try:
        for i in range(1, ds.RasterCount + 1):
            band = ds.GetRasterBand(i)
            band.SetNoDataValue(number)
            band.FlushCache()
    finally:
        ds = None


def merge(
    input_files: List[Union[Path, str]],
    output_file: Union[Path, str]
) -> None:
    """
    将多个 GeoTIFF 文件合并到一个文件当中。要求输入文件已经使用 set_nodata() 将背景设为 NoData。
    使用 GDAL.BuildVRT 生成临时 VRT，再由 gdal.Translate 输出为 TIFF。
    """
    if isinstance(output_file, Path):
        output_file = str(output_file)

    # 为每个输入文件设置 NoData
    for f in input_files:
        set_nodata(f, 0)

    # 创建临时 VRT
    vrt_filename = os.path.join(os.path.dirname(output_file), "temp.vrt")
    vrt_ds = gdal.BuildVRT(vrt_filename, [str(f) for f in input_files])
    if vrt_ds is None:
        print("[merge] 无法创建虚拟数据集 (VRT)")
        return

    try:
        # 转成 GeoTIFF
        gdal.Translate(output_file, vrt_ds, format="GTiff")
    finally:
        vrt_ds = None

    # 删除临时 VRT
    if os.path.exists(vrt_filename):
        os.remove(vrt_filename)

    print(f"[merge] 合并完成 => {output_file}")


if __name__ == '__main__':
    # 下面是一个简单的测试示例，使用前请自行修改路径。
    
    # 假设我们有一个示例输入影像 example_input.tif
    example_input = Path("example_input.tif")

    # 1) 读取
    data_arr, geo_t, proj = read_geo(example_input)
    if data_arr is not None:
        print("读到的数据形状:", data_arr.shape)
        print("地理变换:", geo_t)
        print("投影信息:", proj)

        # 2) 保存（有内存映射）
        out_file = Path("example_output_mem.tif")
        save(out_file, data_arr, geo_t, proj, gdal.GDT_Float32)
        print(f"已保存 (内存映射): {out_file}")

        # 3) 保存（无内存映射）
        out_file2 = Path("example_output_direct.tif")
        save_without_memory_mapping(out_file2, data_arr, geo_t, proj, gdal.GDT_Float32)
        print(f"已保存 (直接写出): {out_file2}")

    # 若需要合并图像：
    # input_files = ["image1.tif", "image2.tif"]
    # merged_output = "merged_output.tif"
    # merge(input_files, merged_output)