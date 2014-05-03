"""
Based on:
http://stackoverflow.com/questions/7861196/check-if-a-geopoint-with-latitude-and-longitude-is-within-a-shapefile
"""
from osgeo import ogr
import sys

DATAPATH = '/home/kedo/Dropbox/CS 194-16/neighborhoods/'
drv = ogr.GetDriverByName('ESRI Shapefile') #We will load a shape file
#Get the contents of the shape file
ds_in = drv.Open(DATAPATH + 'sfneighborhoods.shp')
lyr_in = ds_in.GetLayer(0)    #Get the shape file's first layer

#Put the title of the field you are interested in here
idx_reg = lyr_in.GetLayerDefn().GetFieldIndex('NAME')

#If the latitude/longitude we're going to use is not in the projection
#of the shapefile, then we will get erroneous results.
#The following assumes that the latitude longitude is in WGS84
#This is identified by the number "4236", as in "EPSG:4326"
#We will create a transformation between this and the shapefile's
#project, whatever it may be
geo_ref = lyr_in.GetSpatialRef()
point_ref=ogr.osr.SpatialReference()
point_ref.ImportFromEPSG(4269)
ctran=ogr.osr.CoordinateTransformation(point_ref, geo_ref)

def get_neighborhood(lon=0.0, lat=0.0):
    #Transform incoming longitude/latitude to the shapefile's projection
    [lon,lat,z]=ctran.TransformPoint(lon,lat)

    #Create a point
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, lon, lat)

    #Set up a spatial filter such that the only features we see when we
    #loop through "lyr_in" are those which overlap the point defined above
    lyr_in.SetSpatialFilter(pt)

    #Loop through the overlapped features and display the field of interest
    for feat_in in lyr_in:
        # the first feature is what we want
        return feat_in.GetFieldAsString(idx_reg)

    # Our neighborhoods don't cover all the area of SF
    # (ie: Golden Gate Park isn't a neighborhood)
    # so we sometimes return None
    return None
