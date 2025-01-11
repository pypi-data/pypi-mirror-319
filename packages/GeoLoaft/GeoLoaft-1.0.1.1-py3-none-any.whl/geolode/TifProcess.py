'''
Descripttion: 
version: Tif基本处理
Author: Anchenry
Date: 2024-12-19 13:06:34
LastEditors: Anchenry
LastEditTime: 2024-12-20 13:06:43
'''

import numpy as np
from osgeo import gdal

def readTif(fileName, xoff=0, yoff=0, data_width=0, data_height=0, bands=None):
    """
    Description: 读取tif文件
    Parm: 文件路径，起始点，读取长宽
    Return: 返回遥感影像值和
    """
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "文件无法打开")
        return
    #  栅格矩阵的列数
    width = dataset.RasterXSize
    #  栅格矩阵的行数
    height = dataset.RasterYSize
    #  获取数据
    if (data_width == 0 and data_height == 0):
        data_width = width
        data_height = height
    data = dataset.ReadAsArray(xoff, yoff, data_width, data_height)

    # 如果未指定波段，默认读取所有波段
    if bands is None:
        bands = range(1, dataset.RasterCount + 1)  # 从第1个波段到最后一个波段

    # 读取指定波段的数据
    data = []
    for band_idx in bands:
        band = dataset.GetRasterBand(band_idx)
        band_data = band.ReadAsArray(xoff, yoff, data_width, data_height)
        data.append(band_data)
    
    # 将多个波段的数据合并成一个三维数组（波段, 高度, 宽度）
    data = np.array(data)

    # 获取影像的地理信息
    geo_transform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()
    # 影像的仿射矩阵
    block_geo_transform = (
        geo_transform[0] + xoff * geo_transform[1] + yoff * geo_transform[2],  # 左上角X（考虑旋转）
        geo_transform[1],  # 每个像素的宽度（未变）
        geo_transform[2],  # 旋转系数X（保持不变）
        geo_transform[3] + xoff * geo_transform[4] + yoff * geo_transform[5],  # 左上角Y（考虑旋转）
        geo_transform[4],  # 旋转系数Y（保持不变）
        geo_transform[5],  # 每个像素的高度（未变）
    )

    dataset = None
    return data, block_geo_transform, projection


def readTifInChunksPix(fileName, chunk_width=256, chunk_height=256, bands=None):
    """
    Description: 读取TIF文件并按块读取
    Parm:
        fileName: 文件路径
        chunk_width: 每块读取的列宽
        chunk_height: 每块读取的行高
    Return:
        返回影像数据的生成器，按块逐个返回数据
    """
    # 打开TIF文件
    dataset = gdal.Open(fileName)
    if dataset is None:
        print(f"{fileName} 文件无法打开")
        return

    # 获取影像的宽度和高度
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    
    # 分块读取
    for yoff in range(0, height, chunk_height):
        for xoff in range(0, width, chunk_width):
            # 计算每个块的实际宽度和高度，防止越界
            data_width = min(chunk_width, width - xoff)
            data_height = min(chunk_height, height - yoff)
            
            # 读取数据块
            data, geo_transform, proj = readTif(fileName, xoff, yoff, data_width, data_height, bands)
            
            # 返回每个块的数据
            yield data, geo_transform, proj


def readTifInChunksNum(fileName, num_chunks_x=10, num_chunks_y=10, bands=None):
    """
    Description: 读取TIF文件并按块读取，按给定的分块数量进行分块
    Parm:
        fileName: 文件路径
        num_chunks_x: 水平方向上的分块数
        num_chunks_y: 垂直方向上的分块数
    Return:
        返回影像数据的生成器，按块逐个返回数据
    """
    # 打开TIF文件
    dataset = gdal.Open(fileName)
    if dataset is None:
        print(f"{fileName} 文件无法打开")
        return

    # 获取影像的宽度和高度
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    
    # 计算每块的宽度和高度
    chunk_width = width // num_chunks_x
    chunk_height = height // num_chunks_y

    # 确保每块的宽度和高度都不小于1
    if chunk_width == 0 or chunk_height == 0:
        print("无法将影像分成如此多的块，请调整分块数量")
        return

    # 分块读取
    for yoff in range(0, height, chunk_height):
        for xoff in range(0, width, chunk_width):
            # 计算每个块的实际宽度和高度，防止越界
            data_width = min(chunk_width, width - xoff)
            data_height = min(chunk_height, height - yoff)
            
            # 读取数据块
            data, geo_transform, proj = readTif(fileName, xoff, yoff, data_width, data_height, bands)
            
            # 返回每个块的数据
            yield data, geo_transform, proj


def calBoundingBox(geo_transform, width, height):
    """
    Description: 计算旋转后的栅格图像外包矩形的地理范围
    Parm:
        geo_transform: 仿射变换元组
        width: 图像宽度（像素数）
        height: 图像高度（像素数）
    return: 
        外包矩形的地理范围 (min_x, min_y, max_x, max_y)
    """
    # 计算四个角的地理坐标
    # 左上角
    x1 = geo_transform[0]
    y1 = geo_transform[3]
    
    # 右上角
    x2 = geo_transform[0] + width * geo_transform[1] + 0 * geo_transform[2]
    y2 = geo_transform[3] + width * geo_transform[4] + 0 * geo_transform[5]
    
    # 左下角
    x3 = geo_transform[0] + 0 * geo_transform[1] + height * geo_transform[2]
    y3 = geo_transform[3] + 0 * geo_transform[4] + height * geo_transform[5]
    
    # 右下角
    x4 = geo_transform[0] + width * geo_transform[1] + height * geo_transform[2]
    y4 = geo_transform[3] + width * geo_transform[4] + height * geo_transform[5]
    
    # 计算外包矩形
    min_x = min(x1, x2, x3, x4)
    max_x = max(x1, x2, x3, x4)
    min_y = min(y1, y2, y3, y4)
    max_y = max(y1, y2, y3, y4)
    
    return (min_x, min_y, max_x, max_y)


def removeBand(input_tif, output_tif, bands_to_remove):
    """
    删除指定波段并保存新的 TIF 文件。

    Parm:
        input_tif: 输入的 TIF 文件路径
        output_tif: 输出的 TIF 文件路径
        bands_to_remove: 要删除的波段编号列表
    """
    # 打开输入的 GeoTIFF 文件
    dataset = gdal.Open(input_tif, gdal.GA_ReadOnly)
    if dataset is None:
        print(f"无法打开文件: {input_tif}")
        return

    # 获取图像的波段数量
    num_bands = dataset.RasterCount
    print(f"原始图像 {input_tif} 包含 {num_bands} 个波段")

    # 创建一个新的文件（使用原始图像的宽度和高度，减去删除的波段数量）
    driver = gdal.GetDriverByName('GTiff')
    band = dataset.GetRasterBand(1)
    data_type = band.DataType
    output_dataset = driver.Create(output_tif, dataset.RasterXSize, dataset.RasterYSize, 
                                   num_bands - len(bands_to_remove), gdal.GDT_Byte)

    if output_dataset is None:
        print(f"无法创建输出文件: {output_tif}")
        return

    # 设置仿射变换和投影信息
    output_dataset.SetGeoTransform(dataset.GetGeoTransform())
    output_dataset.SetProjection(dataset.GetProjection())

    # 将未删除的波段复制到输出文件
    output_band_index = 1  # 输出文件的波段编号
    for band_index in range(1, num_bands + 1):
        if band_index not in bands_to_remove:
            band = dataset.GetRasterBand(band_index)
            output_band = output_dataset.GetRasterBand(output_band_index)
            output_band.WriteArray(band.ReadAsArray())
            no_data_value = band.GetNoDataValue()  # 获取原始波段的 NoData 值
            if no_data_value is None:
                no_data_value = 0
            # 设置 NoData 值
            output_band.SetNoDataValue(no_data_value)
            output_band_index += 1

    # 清理并关闭文件
    del dataset
    del output_dataset

    print(f"新图像已保存为 {output_tif}")


# 保存tif文件函数
def writeTiff(fileName, data, im_geotrans=(0, 0, 0, 0, 0, 0), im_proj=""):
    if 'int8' in data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(data.shape) == 3:
        im_bands, im_height, im_width = data.shape
    elif len(data.shape) == 2:
        data = np.array([data])
        im_bands, im_height, im_width = data.shape
 
    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(fileName, int(im_width), int(im_height), int(im_bands), datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(data[i])
    del dataset

