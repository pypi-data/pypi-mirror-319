'''
Descripttion: 样本制作
version: 
Author: Anchenry
Date: 2024-12-19 15:11:58
LastEditors: Anchenry
LastEditTime: 2024-12-20 09:34:02
'''

import geolode.ShapefileProcess as shplode
import geolode.TifProcess as tiflode
from osgeo import ogr

def CalSampleBo(feature_extent, tif_extent, sample_width, sample_height):
    """
    Description: 根据feature_extend和sample大小计算分块边界和数量
    Parm:
        feature_extent: 要素的外包矩形 (min_x, min_y, max_x, max_y)
        tif_extent: 栅格图像的外包矩形 (min_x, min_y, max_x, max_y)
        sample_width: 每个样本块的宽度，经纬度坐标
        sample_height: 每个样本块的高度，经纬度坐标
    Return:
        返回所有可以裁剪的样本块边界的列表
    """

    # 计算要素和栅格相交的区域
    feature_min_x, feature_min_y, feature_max_x, feature_max_y = feature_extent
    tif_min_x, tif_min_y, tif_max_x, tif_max_y = tif_extent
    # 计算相交区域的范围
    min_x = max(feature_min_x, tif_min_x)
    min_y = max(feature_min_y, tif_min_y)
    max_x = min(feature_max_x, tif_max_x)
    max_y = min(feature_max_y, tif_max_y)
    # 确保范围合法
    if min_x >= max_x or min_y >= max_y:
        return []  # 没有交集，返回空列表
    
    # 计算扩展大小
    expand_size_x = (sample_width - (max_x - min_x) % sample_width) % sample_width
    expand_size_y = (sample_height - (max_y - min_y) % sample_height) % sample_height
    # 向外扩展每个样本块的边界
    extended_min_x = min_x - expand_size_x // 2
    extended_min_y = min_y - expand_size_y // 2
    extended_max_x = max_x + expand_size_x - expand_size_x // 2
    extended_max_y = max_y + expand_size_y - expand_size_y // 2
    # # 确保扩展后的边界不会超出栅格图像的范围
    # extended_min_x = max(extended_min_x, tif_min_x)
    # extended_min_y = max(extended_min_y, tif_min_y)
    # extended_max_x = min(extended_max_x, tif_max_x)
    # extended_max_y = min(extended_max_y, tif_max_y)

    # 计算可以裁剪的样本块的数量
    sample_blocks = []   
    # 从扩展后的左上角开始，按样本块大小裁剪
    for y in range(extended_min_y, extended_max_y, sample_height):
        for x in range(extended_min_x, extended_max_x, sample_width):
            # 样本块的右下角边界
            block_min_x = x
            block_max_x = min(x + sample_width, extended_max_x)
            block_min_y = y
            block_max_y = min(y + sample_height, extended_max_y)
            
            # 确保样本块没有超出栅格图像的范围
            if block_min_x < tif_min_x or block_min_y < tif_min_y or block_max_x > tif_max_x or block_max_y > tif_max_y:
                continue  # 超出栅格图像范围，跳过该块
            
            # 添加样本块的边界到列表
            sample_blocks.append((block_min_x, block_min_y, block_max_x, block_max_y))
    
    return sample_blocks


def CalIntersectSampleBo(feature, sample_blocks):
    """
    Description: 根据给定的要素和样本块，筛选出与要素相交的样本块。
    Parm:
        feature: 要素的几何对象
        sample_blocks: 样本块列表，每个样本块是一个元组 (min_x, min_y, max_x, max_y)
    Return:
        返回与要素相交的样本块列表
    """
    interesect_blocks = []
    for block in sample_blocks:
        # 检查样本块是否与要素相交或完全在要素内部
        if shplode.is_intersecting(block, feature) or shplode.is_contained(block, feature):
            interesect_blocks.append(block)  # 只需要追加块本身，不需要展开
    return interesect_blocks

def pixel_to_geo(pixel_x, pixel_y, geo_transform):
    """
    将栅格的像素坐标转换为地理坐标
    Parm:
        pixel_x: 像素坐标X
        pixel_y: 像素坐标Y
        geo_transform: 栅格的地理变换
    Return:
        对应的地理坐标 (geo_x, geo_y)
    """
    geo_x = geo_transform[0] + pixel_x * geo_transform[1] + pixel_y * geo_transform[2]
    geo_y = geo_transform[3] + pixel_x * geo_transform[4] + pixel_y * geo_transform[5]
    return geo_x, geo_y


def geo_to_pixel(geo_x, geo_y, geo_transform):
    pixel_x = int((geo_x - geo_transform[0]) / geo_transform[1])
    pixel_y = int((geo_y - geo_transform[3]) / geo_transform[5])
    return pixel_x, pixel_y

import os
from osgeo import ogr

def field_exists(layer, field_name):
    layer_defn = layer.GetLayerDefn()
    for i in range(layer_defn.GetFieldCount()):
        field_def = layer_defn.GetFieldDefn(i)
        if field_def.GetName() == field_name:
            return True
    return False

def save_blocks_toshp(interesect_blocks, shp_path, currentnum, feature_fields=None):
    """
    将与要素相交的样本块追加到 Shapefile 中。
    
    Parm:
        interesect_blocks: 与要素相交的样本块列表，每个样本块是一个矩形（min_x, min_y, max_x, max_y）。
        shp_path: 输出 Shapefile 的路径。
        currentnum: 当前的样本块编号（可选，用于附加在文件名或字段中）。
    """

    # 检查 Shapefile 是否存在
    if os.path.exists(shp_path):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        ds = driver.Open(shp_path, 1)  # 更新模式
        layer = ds.GetLayer()
    else:
        driver = ogr.GetDriverByName('ESRI Shapefile')
        ds = driver.CreateDataSource(shp_path)
        srs = ogr.osr.SpatialReference()
        srs.ImportFromEPSG(4326)
        layer = ds.CreateLayer('intersect_blocks', srs, ogr.wkbPolygon)

        # 创建字段 SampleID
        field_sample_id = ogr.FieldDefn("Num", ogr.OFTInteger)
        layer.CreateField(field_sample_id)

    # 动态添加字段
    for field_name, field_value in feature_fields.items():
        if not field_exists(layer, field_name):  # 检查字段是否存在
            field = ogr.FieldDefn(field_name, ogr.OFTInteger if isinstance(field_value, int) else ogr.OFTString)
            layer.CreateField(field)

    # 添加样本块
    for idx, block in enumerate(interesect_blocks, start=1):  # 根据块的顺序给 Num 字段赋值
        block_min_x, block_min_y, block_max_x, block_max_y = block

        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(block_min_x, block_min_y)
        ring.AddPoint(block_max_x, block_min_y)
        ring.AddPoint(block_max_x, block_max_y)
        ring.AddPoint(block_min_x, block_max_y)
        ring.CloseRings()

        polygon = ogr.Geometry(ogr.wkbPolygon)
        polygon.AddGeometry(ring)

        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetGeometry(polygon)
        
        # 设置 Num 字段为样本块的顺序编号
        feature.SetField("Num", idx)  # 使用 idx 动态赋值

        # 动态设置其他字段值
        if feature_fields:
            for field_name, field_value in feature_fields.items():
                feature.SetField(field_name, field_value)

        layer.CreateFeature(feature)
    
    # 清理资源
    ds = None  # 关闭数据源
    print(f"Shapefile {shp_path} 更新完成，添加了 {len(interesect_blocks)} 个样本块。")


def clipandsavechunk(feature, tif_data, geo_transform, shp_output_path, currentnum, sample_width=128, sample_height=128):
    """
    裁剪栅格块并保存
    Parm:
        feature: 要素
        tif_data: 栅格数据块
        geo_transform: 栅格的地理变换
        sample_width: 每个样本的宽度
        sample_height: 每个样本的高度
    Return:
        裁剪后的栅格数据，新的 geo_transform 和投影
    """
    width, height = tif_data.shape[2], tif_data.shape[1]

    tif_extent = tiflode.calBoundingBox(geo_transform, width, height)  # 分块栅格外边界
    tif_min_x, tif_min_y, tif_max_x, tif_max_y = tif_extent
    tif_min_pixel_x, tif_max_pixel_y = geo_to_pixel(tif_min_x, tif_min_y, geo_transform)
    tif_max_pixel_x, tif_min_pixel_y = geo_to_pixel(tif_max_x, tif_max_y, geo_transform)
    # 将要素外包矩形（地理坐标）转换为像素坐标
    feature_extent = shplode.featureExtent(feature)  # 要素外包矩形
    feature_min_x, feature_min_y, feature_max_x, feature_max_y = feature_extent
    feature_min_pixel_x, feature_max_pixel_y = geo_to_pixel(feature_min_x, feature_min_y, geo_transform)
    feature_max_pixel_x, feature_min_pixel_y = geo_to_pixel(feature_max_x, feature_max_y, geo_transform)
    # 计算栅格的外包矩形（像素坐标）
    feature_extent_pixel = (feature_min_pixel_x, feature_min_pixel_y, feature_max_pixel_x, feature_max_pixel_y)
    tif_extent_pixel = (tif_min_pixel_x, tif_min_pixel_y, tif_max_pixel_x, tif_max_pixel_y)
    sample_blocks = CalSampleBo(feature_extent_pixel, tif_extent_pixel, sample_width, sample_height)  # 与外接矩形相交的裁剪框
    
    # 将每个样本块的像素坐标转换为地理坐标
    geo_sample_blocks = []
    for block in sample_blocks:
        block_min_x, block_min_y, block_max_x, block_max_y = block    
        # 将像素坐标转换为地理坐标
        geo_min_x, geo_max_y = pixel_to_geo(block_min_x, block_min_y, geo_transform)
        geo_max_x, geo_min_y = pixel_to_geo(block_max_x, block_max_y, geo_transform)
        geo_sample_blocks.append((geo_min_x, geo_min_y, geo_max_x, geo_max_y))
    interesect_blocks = CalIntersectSampleBo(feature, geo_sample_blocks)  # 获取与要素相交的样本块
    # 获取 feature 的字段值
    attributes = feature.get("attributes", {})  # 确保 attributes 存在，否则返回空字典
    feature_type = attributes.get("Type")
    feature_year = attributes.get("Year")
    feature_id = attributes.get("Id")

    # 创建一个包含字段名和值的字典
    feature_fields = {}
    if feature_type is not None:
        feature_fields["Type"] = feature_type
    if feature_year is not None:
        feature_fields["Year"] = feature_year
    if feature_id is not None:
        feature_fields["Id"] = feature_id
    save_blocks_toshp(interesect_blocks, shp_output_path, currentnum, feature_fields)  # 保存与要素相交的样本块到 Shapefile

    return len(interesect_blocks)



    # # 存储裁剪数据和相应的 geo_transform
    # clipped_data = []

    # # 遍历每个相交的样本块
    # for block in interesect_blocks:
    #     block_min_x, block_min_y, block_max_x, block_max_y = block
        
    #     # 将地理坐标 (block_min_x, block_min_y) 转换为栅格像素坐标
    #     block_min_pixel_x, block_max_pixel_y = geo_to_pixel(block_min_x, block_min_y, geo_transform)
    #     block_max_pixel_x, block_min_pixel_y = geo_to_pixel(block_max_x, block_max_y, geo_transform)

    #     # 从栅格数据中读取裁剪块的数据
    #     chunk_data = tif_data[:, block_min_pixel_y:block_max_pixel_y, block_min_pixel_x:block_max_pixel_x]

    #     # 计算新的 geo_transform
    #     block_geo_transform = (
    #         geo_transform[0] + block_min_pixel_x * geo_transform[1] + block_min_pixel_y * geo_transform[2],
    #         geo_transform[1],  # 水平分辨率不变
    #         geo_transform[2],  # 旋转系数 X，通常为 0
    #         geo_transform[3] + block_min_pixel_x * geo_transform[4] + block_min_pixel_y * geo_transform[5] ,
    #         geo_transform[4],  # 旋转系数 Y，通常为 0
    #         geo_transform[5],  # 垂直分辨率不变
    #     )

    #     # 将裁剪块的数据和对应的 geo_transform 存储为字典
    #     clipped_data.append({
    #         "data": chunk_data,
    #         "geo_transform": block_geo_transform,
    #     })

    # # 返回裁剪后的数据和相应的 geo_transform，以及投影信息
    # return clipped_data