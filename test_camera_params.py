#!/usr/bin/env python2
# coding: utf-8

from pylab import *
import petanque

omx,omy = meshgrid(arange(-5,6),arange(-5,6))
nmx,nmy = petanque.project_grid(omx,omy,array((0,0)),array((4,0,0)),4)
petanque.display_grid(nmx,nmy,7)
nmx,nmy = petanque.project_grid(omx,omy,array((0,0)),array((4,pi/4,0)),4)
petanque.display_grid(nmx,nmy,7)
nmx,nmy = petanque.project_grid(omx,omy,array((0,0)),array((4,pi/4,.1)),4)
petanque.display_grid(nmx,nmy,7)
nmx,nmy = petanque.project_grid(omx,omy,array((-5,-5)),array((4,pi/4,.1)),4)
petanque.display_grid(nmx,nmy,7)
nmx,nmy = petanque.project_grid(omx,omy,array((0,0)),array((4,0,.1)),4)
petanque.display_grid(nmx,nmy,7)
nmx,nmy = petanque.project_grid(omx,omy,array((0,0)),array((10,0,.4)),4)
petanque.display_grid(nmx,nmy,7)

show()

