#!/usr/bin/env python

"""
This script loads site specific data from a datum file, specified via site_name, and visualises
it on google maps to check the setup is correct. (A google maps api key is required)

Checks include  - does the field match the site name?
                - do the map bounds (for gmapping) cover the field of interest?
                - is the gnss fence correct?
                - is the datum roughly near the center of the field of interest?
                

"""


import rospy

import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import utm
import gmplot 
import webbrowser
import os

from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Bool





class CheckSiteSetup():

    def __init__(self):



        self.site_datum = rospy.get_param("navsat_transform_node/datum")
        print 'site datum: ', self.site_datum


        self.api_key = rospy.get_param("~api_key")


        self.gnss_fence_coords = rospy.get_param("gnss_fence/gnss_fence_coords")


        if not (rospy.has_param('gmapping/xmin') and rospy.has_param('gmapping/xmax') and rospy.has_param('gmapping/ymin') and rospy.has_param('gmapping/ymax')):
            rospy.logwarn("No gmapping map size limits found on server, using defaults: xmin, ymin = -100 and xmax, ymax = 100 ")

        self.map_min_x = rospy.get_param("gmapping/xmin", -100)
        self.map_max_x = rospy.get_param("gmapping/xmax", 100)
        self.map_min_y = rospy.get_param("gmapping/ymin", -100)
        self.map_max_y = rospy.get_param("gmapping/ymax", 100)

        print 'map bounds: ', self.map_min_x, self.map_max_x, self.map_min_y, self.map_max_y

        # Check that we are in a single UTM zone
        self.error = False

        self.utm_zone_nums = []
        self.utm_zone_lets = []
        self.latitude_list = []
        self.longitude_list = []

        self.create_fence()

        self.visualise_site_on_google()



    def create_fence(self):
        print 'creating GNSS fence'
        print  self.gnss_fence_coords
        utm_coords = []

        for i in self.gnss_fence_coords:
            print i
            easting, northing, zone_num, zone_let = utm.from_latlon(i[0], i[1]) # TODO - Handle different zones
            utm_coords.append([easting, northing])
            self.utm_zone_nums.append(zone_num)
            self.utm_zone_lets.append(zone_let)
            self.latitude_list.append(i[0])
            self.longitude_list.append(i[1])

        print 'utm coords: ', utm_coords
        
        self.fence = Polygon(utm_coords)

        # Check entire field is in the same zone before continuing
        if not all(i == self.utm_zone_lets[0] for i in self.utm_zone_lets) and all(i == self.utm_zone_nums[0] for i in self.utm_zone_nums):
            rospy.logerr("The field crosses a utm zone!!! Zones are: %s %s ", self.utm_zone_nums, self.utm_zone_lets)



    def visualise_site_on_google(self):


        gmap = gmplot.GoogleMapPlotter(self.site_datum[0], 
                            self.site_datum[1], 18, apikey=self.api_key)  

        
        datum_utm_east, datum_utm_north, zone_num, zone_let = utm.from_latlon(self.site_datum[0], self.site_datum[1])

        map_min_lat, map_min_lon = utm.to_latlon(datum_utm_east+self.map_min_x, datum_utm_north+self.map_min_y, self.utm_zone_nums[0], self.utm_zone_lets[0])
        map_max_lat, map_max_lon = utm.to_latlon(datum_utm_east+self.map_max_x, datum_utm_north+self.map_max_y, self.utm_zone_nums[0], self.utm_zone_lets[0])

        gmap.polygon([map_max_lat, map_min_lat, map_min_lat, map_max_lat] , [map_min_lon, map_min_lon, map_max_lon, map_max_lon], color = 'cornflowerblue')


        gmap.polygon(self.latitude_list, self.longitude_list, color = 'red')
        x,y = self.fence.exterior.xy 
        lat = []
        lon = []
        for i in range(len(x)):
            lat_i, lon_i = utm.to_latlon(x[i], y[i], self.utm_zone_nums[0], self.utm_zone_lets[0])
            lat.append(lat_i)
            lon.append(lon_i)
        gmap.plot(lat, lon, 'red', edge_width=10)
        gmap.scatter( self.latitude_list, self.longitude_list, 'red', size = 5, marker = False) 
        gmap.marker(self.site_datum[0], self.site_datum[1], 'red')

        file_name = os.getenv("HOME") + '/gmap.html'
        gmap.draw(file_name) 
        webbrowser.open('file://' + os.path.realpath(file_name))




if __name__ == '__main__':
    rospy.init_node('check_site_setup')
    CheckSiteSetup()
    rospy.spin()
