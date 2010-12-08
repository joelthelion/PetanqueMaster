#!/usr/bin/env python2
# coding: utf-8

from pylab import *
import scipy.linalg as lin

def display_grid(mx,my):
    figure()
    for ii in xrange(mx.shape[0]):
        plot(mx[ii,:],my[ii,:],'b-')
    for jj in xrange(mx.shape[1]):
        plot(mx[:,jj],my[:,jj],'r-')
    text(mx[0,0],my[0,0],"O")
    text(mx[0,-1],my[0,-1],"ex")
    text(mx[-1,0],my[-1,0],"ey")
    axis("equal")
    ylim(-20,20)
    xlim(-20,20)

def cart_from_sphere(pointsphere):
    assert(pointsphere[0]>0)
    assert(pointsphere[2]>=0 and pointsphere[2]<=pi/2)
    return pointsphere[0]*array([sin(pointsphere[1])*sin(pointsphere[2]),-cos(pointsphere[1])*sin(pointsphere[2]),cos(pointsphere[2])])

def norm_cart_from_sphere(pointsphere):
    return cart_from_sphere((1,pointsphere[1],pointsphere[2]))

def project_point_internal(pointplan,cameraplan,cameraouter,rot):
    point = dot(rot,[pointplan[0]-cameraplan[0],pointplan[1]-cameraplan[1],0]-cameraouter)
    assert(point[2]<0)
    return -4.*point[:2]/point[2]

def project_point(pointplan,cameraplan,camerasphere):
    cameraouter = cart_from_sphere(camerasphere)
    cameraouter_norm = norm_cart_from_sphere(camerasphere)
    cameraup = cart_from_sphere([1,pi+camerasphere[1],pi/2-camerasphere[2]])
    assert(abs(dot(cameraouter_norm,cameraup))<10e-5)
    rot = array([cross(cameraup,cameraouter_norm),cameraup,cameraouter_norm])
    return project_point_internal(pointplan,cameraplan,cameraouter,rot)

def project_grid(mx,my,cameraplan,camerasphere):
    nmx = zeros(mx.shape)
    nmy = zeros(my.shape)
    for ii in xrange(mx.shape[0]):
        for jj in xrange(mx.shape[1]):
            nmx[ii,jj],nmy[ii,jj] = project_point((mx[ii,jj],my[ii,jj]),cameraplan,camerasphere)
    return nmx,nmy


omx,omy = meshgrid(arange(-5,6),arange(-5,6))
nmx,nmy = project_grid(omx,omy,array((0,0)),array((4,0,0)))
display_grid(nmx,nmy)
nmx,nmy = project_grid(omx,omy,array((0,0)),array((4,pi/4,0)))
display_grid(nmx,nmy)
nmx,nmy = project_grid(omx,omy,array((0,0)),array((4,pi/4,.1)))
display_grid(nmx,nmy)
nmx,nmy = project_grid(omx,omy,array((-5,-5)),array((4,pi/4,.1)))
display_grid(nmx,nmy)
nmx,nmy = project_grid(omx,omy,array((0,0)),array((4,0,.1)))
display_grid(nmx,nmy)
nmx,nmy = project_grid(omx,omy,array((0,0)),array((10,0,.4)))
display_grid(nmx,nmy)

show()

