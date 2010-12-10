#!/usr/bin/env python
# coding: utf-8
# 
# all distance are in meters
# all angles are in radians

import petanque
from pylab import *
import scipy.linalg as lin

def display_grid(mx,my,limit):
    factor = 1
    unit = "[m]"
    if limit<1:
        factor = 100
        unit = "[cm]"
    figure()
    for ii in xrange(mx.shape[0]):
        plot(factor*mx[ii,:],factor*my[ii,:],'b-',alpha=.5)
    for jj in xrange(mx.shape[1]):
        plot(factor*mx[:,jj],factor*my[:,jj],'r-',alpha=.5)
    text(factor*mx[0,0],factor*my[0,0],"O")
    text(factor*mx[0,-1],factor*my[0,-1],"ex")
    text(factor*mx[-1,0],factor*my[-1,0],"ey")
    axis("equal")
    ylim(-factor*limit,factor*limit)
    xlim(-factor*limit,factor*limit)
    xlabel("x %s" % unit)
    ylabel("y %s" % unit)
    return factor

def project_grid(mx,my,cameraplan,camerasphere,zoom):
    nmx = zeros(mx.shape)
    nmy = zeros(my.shape)
    foo = petanque.project_points(vstack((mx.ravel(),my.ravel())),cameraplan,camerasphere,zoom)
    mx = foo[0,:].reshape(nmx.shape)
    my = foo[1,:].reshape(nmy.shape)
    return mx,my

def order_positions(positions):
    extracted = [ (kk,lin.norm(position)) for kk,position in enumerate(positions.transpose()) ]
    extracted.sort(key=lambda x: x[1])
    return [ tag for tag,distance in extracted ]

print "click points"
mx,my = meshgrid(linspace(-1.5,1.5,7),linspace(-1.5,1.5,7))
display_grid(mx,my,2)
title("click balls position")
positions_truth = array(ginput(-1)).transpose()
order_truth = order_positions(positions_truth)
close()
print "clicked %d balls" % positions_truth.shape[1]

print "generating data"
datas = []
for theta in linspace(0,2*pi,10,endpoint=False):
    cameraplan = .3*randn(2)
    camerasphere = array((2.+random(),theta+pi/10*randn(),pi/180*(15.+random()*20)))
    camerafocal = 0.05
    projections_truth = petanque.project_points(positions_truth,cameraplan,camerasphere,camerafocal)
    datas.append(((cameraplan,camerasphere,camerafocal),projections_truth))

datas_noisy = [(params,projections+randn(projections.size).reshape(projections.shape)*.001) for params,projections in datas]

print "estimating positions with fixed camera params"
positions_estimated = petanque.estimate_positions(datas)
order_estimated = order_positions(positions_estimated)
print "bias=%s [mm]" % (1e3*(positions_estimated-positions_truth).mean(axis=1))
print "std=%s [mm]" % (1e3*(positions_estimated-positions_truth).std(axis=1))
if order_estimated==order_truth: print "ORDER PRESERVED!!!"

print "estimating positions with fixed camera params with noisy projections"
positions_estimated_noisy = petanque.estimate_positions(datas_noisy)
order_estimated_noisy = order_positions(positions_estimated_noisy)
print "bias=%s [mm]" % (1e3*(positions_estimated_noisy-positions_truth).mean(axis=1))
print "std=%s [mm]" % (1e3*(positions_estimated_noisy-positions_truth).std(axis=1))
if order_estimated_noisy==order_truth: print "ORDER PRESERVED!!!"

print "display results"
factor = display_grid(mx,my,2)
plot(factor*positions_truth[0,:],factor*positions_truth[1,:],'go',label="truth")
plot(factor*positions_estimated[0,:],factor*positions_estimated[1,:],'g*',label="est")
plot(factor*positions_estimated_noisy[0,:],factor*positions_estimated_noisy[1,:],'r*',label="est/noise")
legend()
title('plan de la table')

for kk,(((cameraplan,camerasphere,camerafocal),projections_truth),(params2,projections_noisy)) in enumerate(zip(datas,datas_noisy)):
    projections_estimated = petanque.project_points(positions_estimated,cameraplan,camerasphere,camerafocal)
    projections_estimated_noisy = petanque.project_points(positions_estimated_noisy,cameraplan,camerasphere,camerafocal)
    projections_mx,projections_my = project_grid(mx,my,cameraplan,camerasphere,camerafocal)
    factor = display_grid(projections_mx,projections_my,.05)
    plot(factor*projections_truth[0,:],factor*projections_truth[1,:],'go',label="truth")
    plot(factor*projections_estimated[0,:],factor*projections_estimated[1,:],'g*',label="est")
    plot(factor*projections_noisy[0,:],factor*projections_noisy[1,:],'ro',label="noise")
    plot(factor*projections_estimated_noisy[0,:],factor*projections_estimated_noisy[1,:],'r*',label="est/noise")
    legend()
    title(u"config %d plan=(%.2f,%.2f) r=%.2f theta=%.0f° phi=%.0f°" % (kk,cameraplan[0],cameraplan[1],camerasphere[0],180/pi*camerasphere[1],180/pi*camerasphere[2]))

show()
