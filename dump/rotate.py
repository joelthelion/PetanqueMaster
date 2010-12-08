#!/usr/bin/env python2
# coding: utf-8

from matplotlib.pylab import *
import numpy
import numpy.linalg

def pl(ar,style="b-"):
    plot(ar[0,:],ar[1,:],style)

def rotate_and_scale(pts,angle,scale=1.):
    rot=numpy.array(((numpy.cos(angle),-numpy.sin(angle)),(numpy.sin(angle),numpy.cos(angle))))*scale
    return numpy.dot(rot,pts)

def estimate(pts,mv_pts):
    return dot(numpy.linalg.pinv(mv_pts.transpose()),pts.transpose()).transpose()

input=numpy.genfromtxt("pts.txt",delimiter=",").transpose()
moved=rotate_and_scale(input,0.2,1.5)
estimation=estimate(input,moved)
print estimation
compensated=numpy.dot(estimation,moved)
pl(input)
pl(moved,"r-")
pl(compensated,"g-")
show()
