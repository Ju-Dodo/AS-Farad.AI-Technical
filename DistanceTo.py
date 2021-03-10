import pyproj
from shapely.geometry import Point
from shapely.ops import transform

# Create a transformation from epsg:4326 (lat,long) to epsg:27700 (UK Grid Co-ordinates)
project = pyproj.Transformer.from_crs('epsg:4326','epsg:27700', always_xy=True)

def DistanceTo(df_from,point_to,geom_col='geom', min_dist = 0, max_dist = 1000, min_area = None):
    """
    Creates a sub-dataframe that only includes entries in df_from that have an area>min_area and are within a range
    min_dist < distance to point_to < max_dist
    :param df_from: Geopandas dataframe to create sub-datafraome from
    :param point_to: (lat, long) co-ordinates of the comparison point
    :param geom_col: specifies the geometry column in df_from
    :param min_dist: minimum allowable distance from entries in df_from to point_to (units: m)
    :param max_dist: maximum allowable distance from entries in df_from to point_to (units: m)
    :param min_area: minimum allowable area for entries in df_from (units: m^2)
    :return: sub-dataframe copy of df_from with entries that lie within the allowable range
    """
    # transforms point_to into epsg:27700
    p_t = transform(project.transform, Point(point_to))

    # Creates the sub-dataframe that meets specified criteria
    if min_area is not None:
        sub_df = df_from[(df_from[geom_col].to_crs('epsg:27700').apply(lambda row: row.distance(p_t)) >= min_dist) &
                         (df_from[geom_col].to_crs('epsg:27700').apply(lambda row: row.distance(p_t)) < max_dist) &
                         (df_from.wkb_geometry.to_crs('epsg:27700').area>=min_area)]
    else:
        sub_df = df_from[(df_from[geom_col].to_crs('epsg:27700').apply(lambda row: row.distance(p_t)) >= min_dist) &
                         (df_from[geom_col].to_crs('epsg:27700').apply(lambda row: row.distance(p_t)) < max_dist)]

    return sub_df.copy()
