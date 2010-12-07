#!/usr/bin/env python

from pylab import *
import cPickle as pck
import sys
import os

colors = ["jaune","violette","rose","jaune orange","rouge","vert etoile","vert vagues"]
directory = "data"
meanoutput = {}

outputs = [ pck.load(open(pointsname,"rb")) for pointsname in sys.argv[1:] ]
experts = [ output[1] for output in outputs ]
print "experts=%s" % experts

distances = {}
for expert in experts:
    distances[expert] = 0.

for kk,imagename in enumerate(os.listdir(directory)):
    print "%d -> %s" % (kk,imagename)
    image = imread(os.path.join(directory,imagename))
    figure()
    imshow(image)

    meanpoints = None
    for points,expert in outputs:
        tabpoints = array([points[imagename][color] for color in colors])
        if meanpoints is None:
            meanpoints = zeros(tabpoints.shape)
        plot(tabpoints[:,0],tabpoints[:,1],'o-',label=expert)
        meanpoints += tabpoints
    meanpoints/=len(outputs)
    plot(meanpoints[:,0],meanpoints[:,1],'+--',label="mean")
    legend()

    for points,expert in outputs:
        tabpoints = array([points[imagename][color] for color in colors])
        distances[expert] += absolute(tabpoints-meanpoints).sum()

    points = {}
    for color,point in zip(colors,meanpoints):
        points[color] = point.tolist()
    meanoutput[imagename] = points

print "distances=%s" % distances
show()
pck.dump((meanoutput,"%s" % experts),open("meanpoints.pck","wb"),-1)

