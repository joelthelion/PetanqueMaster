#!/usr/bin/env python
# coding: utf-8
# 
# all distance are in meters
# all angles are in radians

import petanque
from pylab import *
import scipy.linalg as lin

standard_ball_radius = .09
number_of_balls = 6
number_of_pictures = 8

def order_positions(positions):
    extracted = [ (kk,lin.norm(position)) for kk,position in enumerate(positions.transpose()) ]
    extracted.sort(key=lambda x: x[1])
    return [ tag for tag,distance in extracted ]

print "click points"
mx,my = meshgrid(linspace(-1.5,1.5,7),linspace(-1.5,1.5,7))
petanque.display_grid(mx,my,2)
title("click balls position")
positions_truth = array(ginput(number_of_balls)).transpose()
positions_truth = vstack((positions_truth,standard_ball_radius*ones(positions_truth.shape[1])))
order_truth = order_positions(positions_truth)
close()
print "clicked %d balls" % positions_truth.shape[1]

print "generating data"
datas = []
for theta in linspace(0,2*pi,number_of_pictures,endpoint=False):
    cameraplan = .3*randn(2)
    camerasphere = array((2.+random(),theta+pi/10*randn(),pi/180*(15.+random()*20)))
    camerafocal = 0.05
    projections_truth = petanque.project_points(positions_truth,cameraplan,camerasphere,camerafocal)
    datas.append(((cameraplan,camerasphere,camerafocal),projections_truth))

datas_noisy = [(params,projections+randn(projections.size).reshape(projections.shape)*.0005) for params,projections in datas]

print "estimating positions with fixed camera params"
positions_estimated = petanque.estimate_positions(datas,standard_ball_radius)
order_estimated = order_positions(positions_estimated)
print "bias=%s [mm]" % (1e3*(positions_estimated-positions_truth)[:2].mean(axis=1))
print "std=%s [mm]" % (1e3*(positions_estimated-positions_truth)[:2].std(axis=1))
if order_estimated==order_truth: print "ORDER PRESERVED!!!"

print "estimating positions with fixed camera params with noisy projections"
positions_estimated_noisy = petanque.estimate_positions(datas_noisy,standard_ball_radius)
order_estimated_noisy = order_positions(positions_estimated_noisy)
print "bias=%s [mm]" % (1e3*(positions_estimated_noisy-positions_truth)[:2].mean(axis=1))
print "std=%s [mm]" % (1e3*(positions_estimated_noisy-positions_truth)[:2].std(axis=1))
if order_estimated_noisy==order_truth: print "ORDER PRESERVED!!!"

print "display results"
factor = petanque.display_grid(mx,my,2)
petanque.display_projections(factor,positions_truth,"go","truth")
petanque.display_projections(factor,positions_estimated,"g*","est")
petanque.display_projections(factor,positions_estimated_noisy,"r*","est w/ noise")
legend()
title('plan de la table')

for kk,(((cameraplan,camerasphere,camerafocal),projections_truth),(params2,projections_noisy)) in enumerate(zip(datas,datas_noisy)):
    projections_estimated = petanque.project_points(positions_estimated,cameraplan,camerasphere,camerafocal)
    projections_estimated_noisy = petanque.project_points(positions_estimated_noisy,cameraplan,camerasphere,camerafocal)
    projections_mx,projections_my = petanque.project_grid(mx,my,cameraplan,camerasphere,camerafocal)
    factor = petanque.display_grid(projections_mx,projections_my,.05)
    petanque.display_projections(factor,projections_truth,'go',"truth")
    petanque.display_projections(factor,projections_estimated,'g*',"est")
    petanque.display_projections(factor,projections_noisy,'ro',"truth w/ noise")
    petanque.display_projections(factor,projections_estimated_noisy,'r*',"est w/ noise")
    legend()
    title(u"config %d plan=(%.2f,%.2f) r=%.2f theta=%.0f° phi=%.0f°" % (kk,cameraplan[0],cameraplan[1],camerasphere[0],180/pi*camerasphere[1],180/pi*camerasphere[2]))

show()
