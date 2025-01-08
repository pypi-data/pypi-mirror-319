'''
Descripttion: 
version: 综合shp和tif进行处理
Author: Anchenry
Date: 2024-12-19 14:15:10
LastEditors: Anchenry
LastEditTime: 2024-12-19 15:02:25
'''

import os
from osgeo import ogr, gdal
import geolode.ShapefileProcess as shplode

def filterFeaturesByExtent(features, tif_extent):
    """
    Description: 筛选出位于遥感影像范围内的要素
    Parm: 所有要素，遥感影像范围 (min_x, min_y, max_x, max_y)
    Return: 筛选后的要素列表
    """
    filtered_features = []
    min_x, min_y, max_x, max_y = tif_extent

    for feature in features:
        # 获取要素的边界框
        geom_extent = shplode.featureExtent(feature)  # (min_x, min_y, max_x, max_y)
        
        # 判断要素是否与遥感影像的范围相交
        if (geom_extent[0] < max_x and geom_extent[2] > min_x and
            geom_extent[1] < max_y and geom_extent[3] > min_y):
            filtered_features.append(feature)

    return filtered_features

def RasterShpIntersect(tif_data, geo_transform, feature):
    """
    判断栅格数据与要素是否相交
    Parm:
        tif_data: 栅格数据块（numpy 数组）
        geo_transform: 栅格的地理变换（affine transformation）
        feature: 要素（包含 WKT 几何）
    Return:
        如果栅格数据与要素相交，则返回 True；否则返回 False
    """
    # 获取要素的几何对象
    geometry = ogr.CreateGeometryFromWkt(feature['geometry'])
    
    # 计算栅格块的范围
    x_size, y_size = tif_data.shape[1], tif_data.shape[0]  # 栅格数据的宽度和高度
    min_x, max_y = geo_transform[0], geo_transform[3]  # 左上角坐标
    pixel_width, pixel_height = geo_transform[1], geo_transform[5]  # 每个像素的宽度和高度
    
    # 计算栅格的四个角点
    max_x = min_x + pixel_width * x_size
    min_y = max_y + pixel_height * y_size
    
    # 创建栅格的外包多边形
    raster_polygon = ogr.Geometry(ogr.wkbPolygon)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(min_x, min_y)
    ring.AddPoint(max_x, min_y)
    ring.AddPoint(max_x, max_y)
    ring.AddPoint(min_x, max_y)
    ring.AddPoint(min_x, min_y)
    raster_polygon.AddGeometry(ring)
    
    # 判断栅格与要素的几何是否相交
    return raster_polygon.Intersects(geometry)

def check_tif_size(tif_path, expected_width=128, expected_height=128):
    """
    检查指定 TIF 文件的尺寸是否为预期的大小。
    
    Parm:
        tif_path: TIF 文件路径。
        expected_width: 预期的宽度（默认 256 像素）。
        expected_height: 预期的高度（默认 256 像素）。
        
    Return:
        是否符合预期尺寸，以及实际尺寸 (width, height)。
    """
    tif_ds = gdal.Open(tif_path)
    if not tif_ds:
        raise RuntimeError(f"无法打开 TIF 文件: {tif_path}")
    
    # 获取栅格的大小
    width = tif_ds.RasterXSize
    height = tif_ds.RasterYSize
    tif_ds = None  # 关闭数据集

    # 检查是否为预期的大小
    if width == expected_width and height == expected_height:
        return True, (width, height)
    else:
        return False, (width, height)

# 这里使用的是外接矩形
def clip_tif_by_shapefile(tif_path, shp_path, output_dir, tif_suffix):
    """
    使用 Shapefile 对 TIF 文件进行裁剪并保存每个要素为单独的 TIF 文件。
    
    Parm:
        tif_path: 输入的 TIF 文件路径。
        shp_path: 用于裁剪的 Shapefile 文件路径。
        output_dir: 裁剪结果保存的文件夹。
    """
    # 打开 Shapefile
    shp_ds = ogr.Open(shp_path)
    features = shplode.readShapefile(shp_path)
    # if not shp_ds:
    #     raise RuntimeError(f"无法打开 Shapefile: {shp_path}")
    
    # 获取 Shapefile 的图层
    layer = shp_ds.GetLayer()
    
    # 读取 TIF 文件
    tif_ds = gdal.Open(tif_path)
    if not tif_ds:
        raise RuntimeError(f"无法打开 TIF 文件: {tif_path}")

    # 获取 TIF 的基本信息
    geo_transform = tif_ds.GetGeoTransform()
    pixel_width = abs(geo_transform[1])  # 每个像素的宽度
    pixel_height = abs(geo_transform[5]) # 每个像素的高度

    existing_files = [f for f in os.listdir(output_dir) if f.startswith(tif_suffix) and f.endswith('.tif')]
    startnum = len(existing_files)

    # 获取 Shapefile 中的每个要素并对每个要素裁剪
    for feature_id, feature in enumerate(features):
        # 获取当前要素的边界（bounding box）
        geometry = feature.get("geometry")
        geomwkt = ogr.CreateGeometryFromWkt(geometry)
        bbox = geomwkt.GetEnvelope()  # 返回 (minX, maxX, minY, maxY)
        minX, maxX, minY, maxY = bbox

        # 获取 feature 的字段值 
        attributes = feature.get("attributes", {})  # 确保 attributes 存在，否则返回空字典
        feature_type = attributes.get("Type")
        feature_year = attributes.get("Year")
        feature_Id = attributes.get("Id")
        feature_num = attributes.get("Num")

        if feature_year is not None and feature_Id is not None:
            output_tif = os.path.join(output_dir, f"{tif_suffix}_{feature_year}_{feature_Id}_{feature_num}.tif")
        else:
            # 如果 `feature_year` 或 `feature_id` 为空，则使用默认的输出路径命名
            output_tif = os.path.join(output_dir, f"{tif_suffix}_{startnum + feature_id}.tif")

        # 使用 gdal.Warp 裁剪 TIF 文件
        try:
            gdal.Warp(
                output_tif,                # 输出路径
                tif_ds,                    # 输入 TIF 文件
                format="GTiff",            # 输出格式
                outputBounds=(minX, minY, maxX, maxY),  # 裁剪区域的边界
                cropToCutline=True,        # 裁剪到 Shapefile 中的要素
                xRes=tif_ds.GetGeoTransform()[1],  # 保持原 TIF 分辨率
                yRes=abs(tif_ds.GetGeoTransform()[5]),  # 保持原 TIF 分辨率
            )
            print(f"裁剪结果已保存为: {output_tif}")
            
            # 检查裁剪结果是否为 256x256
            is_valid, size = check_tif_size(output_tif)
            if not is_valid:
                print(f"验证失败: {output_tif} 尺寸为 {size}，需要进一步处理")
        except Exception as e:
            print(f"裁剪失败: {e}")

    # 关闭数据源
    shp_ds = None
    tif_ds = None

# 直接使用了要素
def clip_tif_by_features(tif_path, shp_path, output_dir):
    """
    使用给定的要素几何裁剪 TIF 文件并保存每个要素为单独的 TIF 文件。
    
    Parm:
        tif_path: 输入的 TIF 文件路径。
        features: 要素列表，每个要素包含一个几何形状。
        output_dir: 裁剪结果保存的文件夹。
    """
    input_raster = gdal.Open(tif_path)
    output_tif = os.path.join(output_dir, f"TIF_QZ_2024.tif")
    # 使用 gdal.Warp 进行裁剪
    try:
        # 利用gdal.Warp进行裁剪

        result = gdal.Warp(
            output_tif,
            input_raster,
            format = 'GTiff',
            cutlineDSName = shp_path, # 用于裁剪的矢量
            cropToCutline = True, # 是否使用cutlineDSName的extent作为输出的界线
            dstNodata = 0 # 输出数据的nodata值
            )
        print(f"裁剪结果已保存为: {output_tif}")
        del result
    except Exception as e:
        print(f"裁剪失败: {e}")
    
    del input_raster

if __name__ == '__main__':
    # 使用示例
    TIFPath = r"//192.168.66.10/data_vol/huangzhijie/PV/rs/2024_mosaicdata/TIF_2024.tif"
    shp_output_path = r"//192.168.66.10/data_vol/huangzhijie/PV/rs/sample_augmentation/PvShp/CS.shp"
    output_dir = r"//192.168.66.10/data_vol/huangzhijie/PV/rs/sample_augmentation/PvShp"

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 调用裁剪函数
    clip_tif_by_features(TIFPath, shp_output_path, output_dir)