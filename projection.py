#!/usr/bin/env python2
# coding: utf-8

from pylab import *
import scipy.linalg as lin
import petanque

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

def project_grid(mx,my,cameraplan,camerasphere):
    nmx = zeros(mx.shape)
    nmy = zeros(my.shape)
    foo = petanque.project_points(vstack((mx.ravel(),my.ravel())),cameraplan,camerasphere)
    mx = foo[0,:].reshape(nmx.shape)
    my = foo[1,:].reshape(nmy.shape)
    return mx,my

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

