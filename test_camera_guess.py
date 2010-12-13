#!/usr/bin/env python2
# coding: utf-8

from pylab import *
import petanque

camerafocal = 0.05
standard_ball_radius = .09
number_of_balls = 10
number_of_pictures = 1000

mx,my = meshgrid(linspace(-1.5,1.5,7),linspace(-1.5,1.5,7))
positions = .6*randn(2,number_of_balls)
positions = vstack((positions,standard_ball_radius*ones(positions.shape[1])))
factor = petanque.display_grid(mx,my,4)
petanque.display_projections(factor,positions,"ro",None)

distances = []
phis = []
for kk in xrange(number_of_pictures):
    cameraplan = .2*randn(2)
    camerasphere = array((1.5+random()*2,2*pi*random(),pi/180*(5.+random()*30)))
    projections = petanque.project_points(positions,cameraplan,camerasphere,camerafocal)

    distances.append((camerasphere[0],projections[2,:].mean()))
    phis.append((camerasphere[2],projections[2,:].std()/projections[2,:].mean()))

    #projections_mx,projections_my = petanque.project_grid(mx,my,cameraplan,camerasphere,camerafocal)
    #factor = petanque.display_grid(projections_mx,projections_my,.05)
    #petanque.display_projections(factor,projections,'ro',None)
    #title(u"config %d plan=(%.2f,%.2f) r=%.2f theta=%.0f° phi=%.0f°" % (kk,cameraplan[0],cameraplan[1],camerasphere[0],180/pi*camerasphere[1],180/pi*camerasphere[2]))

distances = array(distances)
xdistances = linspace(1.5,3.5,256)

figure()
plot(distances[:,0],1e3*distances[:,1],'+')
plot(xdistances,1e3*standard_ball_radius*camerafocal/xdistances,'-')
xlabel("camera distance [m]")
ylabel("mean balls size [cm]")

phis = array(phis)

figure()
plot(180/pi*phis[:,0],1e3*phis[:,1],'+')
xlabel(u"camera elevation [°]")
ylabel("std/mean balls size [na]")

show()
