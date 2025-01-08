'''
Descripttion: 
version: Shp基本处理
Author: Anchenry
Date: 2024-12-19 13:06:12
LastEditors: Anchenry
LastEditTime: 2024-12-19 17:06:14
'''
from osgeo import ogr

def readShapefile(SHPath):
    """
    Description: 读取指定路径的 Shapefile，并遍历其中的每个要素
    Parm: 文件的路径
    Return: 返回所有要素
    """

    driver = ogr.GetDriverByName('ESRI Shapefile')  # 获取 shapefile 驱动
    if driver is None:
        print("Shapefile driver not available.")
        return

    # 打开 shapefile 文件
    dataset = driver.Open(SHPath, 0)  # 只读
    if dataset is None:
        print(SHPath + "文件无法打开")
        return

    # 获取图层
    layer = dataset.GetLayer()

    # 遍历每个要素
    features = []
    for feature in layer:
        geometry = feature.GetGeometryRef()  # 获取要素的几何信息
        geom_type = geometry.GetGeometryType()  # 获取几何类型
        # 输出几何类型
        geom_type_str = ogr.GeometryTypeToName(geom_type)
        # print(f"Geometry Type: {geom_type_str}")
        
        # 获取属性信息
        attributes = {}
        for field in feature.keys():
            value = feature.GetField(field)
            attributes[field] = value

        # 将几何和属性信息作为字典存储
        features.append({
            'geometry': geometry.ExportToWkt(),
            'geometry_type': geom_type_str,
            'attributes': attributes
        })

    # 关闭数据集
    dataset = None
    return features


def featureExtent(feature):
    """
    Description: 获取要素的外包矩形
    """
    geometry = feature['geometry']
    geomwkt = ogr.CreateGeometryFromWkt(geometry)
    min_x, max_x, min_y, max_y = geomwkt.GetEnvelope()
    return (min_x, min_y, max_x, max_y)


def is_intersecting(extent, feature):
    """
    判断样本块与要素是否相交
    Parm:
        block: 样本块的边界 (min_x, min_y, max_x, max_y)
        feature: 要素的几何对象
    Return:
        如果相交，返回 True，否则返回 False
    """
    min_x, min_y, max_x, max_y = extent

    # 假设 feature 是一个形状对象（例如，polygon）
    feature_geometry = ogr.CreateGeometryFromWkt(feature['geometry'])  # 将 WKT 字符串转为几何对象

    # 创建样本块的矩形几何对象
    sample_geometry = ogr.Geometry(ogr.wkbPolygon)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(min_x, min_y)
    ring.AddPoint(max_x, min_y)
    ring.AddPoint(max_x, max_y)
    ring.AddPoint(min_x, max_y)
    ring.CloseRings()
    sample_geometry.AddGeometry(ring)

    # 判断相交
    return sample_geometry.Intersects(feature_geometry)

def is_contained(block, feature):
    """
    Description: 判断一个样本块是否完全包含在给定的要素内。
    Parm:
        block: 样本块的边界 (min_x, min_y, max_x, max_y)
        feature: 要素，假设为字典类型，包含几何对象，键为 'geometry'
    Return:
        True 如果样本块完全在要素内部，False 否则
    """
    # 从字典中提取几何对象
    feature_geometry = ogr.CreateGeometryFromWkt(feature['geometry']) 

    # 创建样本块的矩形（Polygon）对象
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(block[0], block[1])  # min_x, min_y
    ring.AddPoint(block[2], block[1])  # max_x, min_y
    ring.AddPoint(block[2], block[3])  # max_x, max_y
    ring.AddPoint(block[0], block[3])  # min_x, max_y
    ring.CloseRings()

    block_polygon = ogr.Geometry(ogr.wkbPolygon)
    block_polygon.AddGeometry(ring)

    # 判断样本块是否完全包含在要素内
    return block_polygon.Contains(feature_geometry)
