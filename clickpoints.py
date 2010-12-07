#!/usr/bin/env python

from pylab import *
import os
import cPickle as pck

expertname = raw_input("enter expert name: ")

directory = "data"
colors = ["jaune","violette","rose","jaune orange","rouge","vert etoile","vert vagues"]
output = {}

for imagename in os.listdir(directory):
    image = imread(os.path.join(directory,imagename))
    figure()
    imshow(image)
    points = {}
    for color in colors:
        title("%s click %s" % (imagename,color))
        point = ginput(1)[0]
        points[color] = point

    close()
    output[imagename] = points

print output
pck.dump((output,expertname),open("points_%s.pck" % expertname,"wb"),-1)


