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

def to_cmplx(pts):
    return numpy.hstack(numpy.complex(x,y) for x,y in pts.transpose())

def herm(cmplx):
    return (numpy.conj(cmplx)).transpose()

def estimate_cmplx(pts,mv_pts):
    z_mv=to_cmplx(mv_pts)
    z=to_cmplx(pts)
    #z_mv* / (z_mv* . z_mv) is the more penrose pseudo-inverse of a vector
    r=numpy.conj(numpy.dot(z_mv/dot(z_mv,herm(z_mv)),herm(z)))
    #print r,numpy.abs(r),numpy.angle(r)
    s=numpy.abs(r)
    theta=numpy.angle(r)
    return s*numpy.array(((numpy.cos(theta),-numpy.sin(theta)),(numpy.sin(theta),numpy.cos(theta))))

input=numpy.genfromtxt("pts.txt",delimiter=",").transpose()
moved=rotate_and_scale(input,0.1,1.1)
estimation=estimate(input,moved)
cmplx_est=estimate_cmplx(input,moved)
print estimation
print cmplx_est
compensated=numpy.dot(estimation,moved)
cmplx_comp=numpy.dot(cmplx_est,moved)
pl(input)
pl(moved,"r-")
pl(compensated,"g-")
pl(cmplx_comp,"y-")
show()
