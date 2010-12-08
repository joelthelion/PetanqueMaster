#!/usr/bin/env python
# coding: utf-8

from pylab import *
import petanque

def display_grid(mx,my,boules=None):
    figure()
    for ii in xrange(mx.shape[0]):
        plot(mx[ii,:],my[ii,:],'b-',alpha=.5)
    for jj in xrange(mx.shape[1]):
        plot(mx[:,jj],my[:,jj],'r-',alpha=.5)
    if boules is not None:
        plot(boules[0,:],boules[1,:],'go-')
    text(mx[0,0],my[0,0],"O")
    text(mx[0,-1],my[0,-1],"ex")
    text(mx[-1,0],my[-1,0],"ey")
    axis("equal")
    ylim(-7,7)
    xlim(-7,7)

def project_grid(mx,my,cameraplan,camerasphere,zoom):
    nmx = zeros(mx.shape)
    nmy = zeros(my.shape)
    foo = petanque.project_points(vstack((mx.ravel(),my.ravel())),cameraplan,camerasphere,zoom)
    mx = foo[0,:].reshape(nmx.shape)
    my = foo[1,:].reshape(nmy.shape)
    return mx,my

omx,omy = meshgrid(arange(-5,6),arange(-5,6))
display_grid(omx,omy)
oboules = array([(0,0)]+ginput(7)).transpose()
close()

display_grid(omx,omy,oboules)
title('plan de la table')

nmx,nmy = project_grid(omx,omy,array((0,0)),array((22,.3,1)),20)
nboules = petanque.project_points(oboules,array((0,0)),array((22,.3,1)),20)
display_grid(nmx,nmy,nboules)

show()
