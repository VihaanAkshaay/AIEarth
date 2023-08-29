import numpy as np
from PIL import Image, ImageDraw

##### Defining a mapping function #####

def mapGeoToPixel(raster_image,coords):
    '''
    The input is the raster image & coordinates are in latitude and longitute. 
    '''
    bounds = raster_image.bounds
    x_min = bounds[0]
    x_max = bounds[2]
    y_min = bounds[1]
    y_max = bounds[3]
    
    new_coords = []
    
    #Converting coords (origially in lat-long space to x-y space in picture)
    
    for coord in coords:
        #print(coord)
        x_coord = int((coord[0]-x_min)*(raster_image.width)/(x_max - x_min))
        y_coord = int((coord[1]-y_min)*(raster_image.height)/(y_max - y_min))   
        new_coords.append((x_coord,y_coord))
    
    return new_coords

##### Shapefile to binary_mask #####
def shapefileToBinarymask(raster_image, shapefile):

    # Define the dimensions of the segmentation map
    width = raster_image.width
    height = raster_image.height

    # Create an empty binary segmentation map
    seg_map = np.zeros((height, width), dtype=np.uint8)

    # Create an Image object to draw on
    seg_map_image = Image.fromarray(seg_map)
    draw = ImageDraw.Draw(seg_map_image)

    # Define the coordinates of the polygon vertices
    for i in range(len(shapefile.geometry)):
        #polygon_list_latlong = [(x, y) for x, y,_ in shapefile.geometry[i].exterior.coords]
        polygon_list_latlong = [(x, y) for x, y,_ in shapefile.geometry[i].exterior.coords]
        #print(i)
        polygon_list = mapGeoToPixel(raster_image,polygon_list_latlong)

        # Draw the polygon on the segmentation map
        draw.polygon(polygon_list, fill=1)
    
    #convert back to np.array
    seg_map = np.array(seg_map_image)

    return seg_map

#All changes are done to 'draw' and so, to 'seg_map_image'

##### Obtain raster image from raster file #####
def obtainRasterImageSingleBand(raster_image):
    
    band_id = 1
    band_raster = raster_image.read(band_id)
    band_raster_flipped = np.flip(band_raster, axis=0)

    return band_raster_flipped
