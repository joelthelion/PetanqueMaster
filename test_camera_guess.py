#!/usr/bin/env python2
# coding: utf-8

from pylab import *
import petanque

camerafocal = 0.05
standard_ball_radius = .09
number_of_balls = 3
number_of_pictures = 1000

mx,my = meshgrid(linspace(-1.5,1.5,7),linspace(-1.5,1.5,7))
positions = .6*randn(2,number_of_balls)
positions = vstack((positions,standard_ball_radius*ones(positions.shape[1])))
factor = petanque.display_grid(mx,my,4)
petanque.display_projections(factor,positions,"ro",None)

def guess_camera_params(projections):
    (ar,br) = polyfit(projections[1,:],projections[2,:],1)
    distance = standard_ball_radius*camerafocal/br
    elevation = arctan(-ar/br*camerafocal)
    return (distance,elevation)

distances = []
phis = []
for kk in xrange(number_of_pictures):
    cameraplan = .9*randn(2)
    camerasphere = array((1.5+random()*3,2*pi*random(),pi/180*(random()*30)))
    projections = petanque.project_points(positions,cameraplan,camerasphere,camerafocal)

    params = guess_camera_params(projections)
    distances.append((camerasphere[0],params[0]))
    phis.append((camerasphere[2],params[1]))

    #centera = projections[:2,:].mean(axis=1)
    #centerb = petanque.project_points(positions.mean(axis=1).reshape((3,1)),cameraplan,camerasphere,camerafocal)
    #figure()
    #(ar,br) = polyfit(projections[1,:],projections[2,:],1)
    #plot(projections[1,:],projections[2,:],'+')
    #print br,projections[2,:].mean()
    #xs = linspace(-.05,.05,50)
    #plot(xs,polyval((ar,br),xs))
    #plot(xs,ar*xs+br,':')

    #projections_mx,projections_my = petanque.project_grid(mx,my,cameraplan,camerasphere,camerafocal)
    #factor = petanque.display_grid(projections_mx,projections_my,.05)
    #petanque.display_projections(factor,projections,'ro',None)
    #title(u"config %d plan=(%.2f,%.2f) r=%.2f theta=%.0f° phi=%.0f°" % (kk,cameraplan[0],cameraplan[1],camerasphere[0],180/pi*camerasphere[1],180/pi*camerasphere[2]))

print "distance guess"
distances = array(distances)
xdistances = linspace(.5,3.5,256)
print "bias=%s [mm]" % (1e3*(distances[:,0]-distances[:,1]).mean())
print "std=%s [mm]" % (1e3*(distances[:,0]-distances[:,1]).std())

figure()
plot(distances[:,0],distances[:,1],'+')
plot(xdistances,xdistances,'-')
xlabel("camera distance [m]")
ylabel("guessed distance [m]")

print "elevation guess"
phis = array(phis)
xphis = linspace(0,35,256)*pi/180
print u"bias=%s [°]" % (180/pi*(phis[:,0]-phis[:,1]).mean())
print u"std=%s [°]" % (180/pi*(phis[:,0]-phis[:,1]).std())

figure()
plot(180/pi*phis[:,0],180/pi*phis[:,1],'+')
plot(180/pi*xphis,180/pi*xphis,'-')
xlabel(u"camera elevation [°]")
ylabel(u"guessed elevation [°]")

show()
