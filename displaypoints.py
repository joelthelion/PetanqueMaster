#!/usr/bin/env python

from pylab import *
import cPickle as pck
import sys
import os

outputs = [ pck.load(open(pointsname,"rb")) for pointsname in sys.argv[1:] ]
print "experts=%s" % [ output[1] for output in outputs ]

directory = "data"

for kk,imagename in enumerate(os.listdir(directory)):
    print "%d -> %s" % (kk,imagename)
    image = imread(os.path.join(directory,imagename))
    figure()
    imshow(image)
    for points,expert in outputs:
        tabpoint = array(points[imagename].values())
        plot(tabpoint[:,0],tabpoint[:,1],label=expert)
    legend()

show()

