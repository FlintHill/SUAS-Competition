import ImgProcessingCLI.Runtime.TimeOps as TimeOps
import ImgProcessingCLI.Runtime.GPSOperations as GPSOperations
from math import sqrt
import numpy

class TargetCrop(object):

    def __init__(self, parent_img, crop_img, geo_stamps, crop_loc, ppsi):
        '''
        parent_img: the full sized image from which the crop is cropped
        crop_img: duh
        parent_geo_loc: the latitude and longitude, as a tuple, of the center of the parent image
        crop_loc: the location of the crop in pixels relative to the center of the parent image as a tuple
        ppsi: The pixels per square inch of the camera at the flying altitude
        '''
        self.parent_img = parent_img
        self.crop_img = crop_img
        self.init_time_taken()
        self.init_parent_geo_lat_lon(geo_stamps)
        self.crop_loc = crop_loc
        self.crop_delta = numpy.array([self.crop_loc[0] - (self.parent_img.size[0]//2), (self.parent_img.size[1]//2) - self.crop_loc[1]])
        self.init_gps_of_crop(ppsi)



    def init_time_taken(self):
        try:
            self.second_img_taken = TimeOps.get_second_img_taken(self.parent_img)
        except:
            print("Image has no exif!")
            self.second_img_taken = -1

    def init_parent_geo_lat_lon(self, geo_stamps):
        self.parent_geo_lat_lon = geo_stamps.get_closest_geo_stamp_to_second(self.second_img_taken)

    def init_gps_of_crop(self, ppsi):
        '''ppsi has to be square-rooted because it is the pixels per square inch'''
        self.crop_gps_lat_lon =  GPSOperations.inverse_haversine(numpy.array([0,0]), self.crop_delta * (1.0/(12.0 * sqrt(float(ppsi)))), self.parent_geo_lat_lon)

    def get_crop_img(self):
        return self.crop_img

    def get_crop_gps_lat_lon(self):
        return self.crop_gps_lat_lon

    def __str__(self):
        out_str = "Target crop taken at second: {}, at parent geo location: {}, with target geolocation of: {}, with pixel location relative to center: {}"
        return out_str.format(str(self.second_img_taken), str(self.parent_geo_lat_lon), str(self.crop_gps_lat_lon), str(self.crop_delta))
