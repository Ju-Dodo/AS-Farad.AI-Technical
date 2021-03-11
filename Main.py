import geopandas as gpd
import sqlalchemy
from PSQLConnect import initConn
from DistanceTo import DistanceTo


if __name__=='__main__':
    # open the connection to Google Cloud database
    sqlurl, sslrootcert, sslcert, sslkey = initConn("Templates/config.ini")
    engine = sqlalchemy.create_engine(sqlurl, connect_args={'sslrootcert':sslrootcert,'sslcert':sslcert,'sslkey':sslkey})
    conn = engine.connect()

    # Create GeoPandas dataframes for land registry and substation data
    sql_lr = 'select * from "Land_Reg".cambridge'
    sql_hv = 'select * from "hv_substation".cambridge'
    df_lr = gpd.GeoDataFrame.from_postgis(sql_lr,conn,geom_col='wkb_geometry')
    df_hv = gpd.GeoDataFrame.from_postgis(sql_hv,conn,geom_col='geom')

    # Create sub-dataframes to include only entries that meet the given criteria
    Addenbrookes_coords = (0.1407, 52.1751)
    subdf_lr = DistanceTo(df_lr, Addenbrookes_coords, geom_col='wkb_geometry', min_dist=200, max_dist=1000, min_area=2000)
    subdf_hv = DistanceTo(df_hv, Addenbrookes_coords, geom_col='geom', max_dist=2000)


    # Add a new column to the land registry sub-dataframe that includes the distance to the nearest substation
    nearest_substation = subdf_lr.wkb_geometry.to_crs('epsg:27700').apply(lambda row: subdf_hv.geom.to_crs('epsg:27700').distance(row)).min(axis=1)
    subdf_lr.loc[:,'Nearest_Substation']=nearest_substation

    # Sorts the new dataframe in ascending order of nearest substation
    subdf_lr = subdf_lr.sort_values(by=['Nearest_Substation'])

    # Uploads the new dataframe to Google Google Cloud Database
    subdf_lr.to_postgis("Addenbrookes_Charging",conn,if_exists='replace',schema='Land_Reg',index=False)

    # Closes the connection to the database
    conn.close()
