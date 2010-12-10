#!/usr/bin/env python
# coding: utf-8
# 
# all distance are in meters
# all angles are in radians

from pylab import *
import petanque
import scipy.optimize as opt
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

def estimate_boules(datas):

    def fonctionnelle(eboule,kk):
        distance = []
        for (cameraplan,camerasphere,camerafocal),nboules in datas:
            neboule = petanque.project_points(eboule.reshape(2,1),cameraplan,camerasphere,camerafocal)
            distance.append(sum(absolute(neboule-nboules[:,kk])))
        return sum(distance)

    eboules = array([opt.fmin(fonctionnelle,zeros(2),(kk,),disp=False) for kk in xrange(oboules.shape[1])]).transpose()
    return eboules

print "click points"
omx,omy = meshgrid(linspace(-1.5,1.5,7),linspace(-1.5,1.5,7))
display_grid(omx,omy,2)
title("click balls position")
#oboules = array([(0,0)]+ginput(7)).transpose()
oboules = array(ginput(3)).transpose()
close()

print "generating data"
datas = []
for theta in linspace(0,2*pi,10,endpoint=False):
    cameraplan = .3*randn(2)
    camerasphere = array((2.+random(),theta+pi/10*randn(),pi/180*(15.+random()*5.)))
    camerafocal = 0.05
    nboules = petanque.project_points(oboules,cameraplan,camerasphere,camerafocal)
    datas.append(((cameraplan,camerasphere,camerafocal),nboules))

print "estimating positions with fixed camera params"
eboules = estimate_boules(datas)
print "bias=%s [mm]" % (1e3*(eboules-oboules).mean(axis=1))
print "std=%s [mm]" % (1e3*(eboules-oboules).std(axis=1))

print "display results"
factor = display_grid(omx,omy,2)
plot(factor*oboules[0,:],factor*oboules[1,:],'go-')
plot(factor*eboules[0,:],factor*eboules[1,:],'r*-')
title('plan de la table')

for kk,((cameraplan,camerasphere,camerafocal),nboules) in enumerate(datas):
    neboules = petanque.project_points(eboules,cameraplan,camerasphere,camerafocal)
    nmx,nmy = project_grid(omx,omy,cameraplan,camerasphere,camerafocal)
    factor = display_grid(nmx,nmy,.05)
    plot(factor*nboules[0,:],factor*nboules[1,:],'go-')
    plot(factor*neboules[0,:],factor*neboules[1,:],'r*-')
    title("config %d" % kk)

show()
