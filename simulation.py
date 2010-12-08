#!/usr/bin/env python
# coding: utf-8

from pylab import *
import petanque
import scipy.optimize as opt
import scipy.linalg as lin

def display_grid(mx,my):
    figure()
    for ii in xrange(mx.shape[0]):
        plot(mx[ii,:],my[ii,:],'b-',alpha=.5)
    for jj in xrange(mx.shape[1]):
        plot(mx[:,jj],my[:,jj],'r-',alpha=.5)
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

def estimate_boules(datas):

    def fonctionnelle(eboule,kk):
        distance = []
        for (cameraplan,camerasphere,camerazoom),nboules in datas:
            neboule = petanque.project_points(eboule.reshape(2,1),cameraplan,camerasphere,camerazoom)
            distance.append(sum(absolute(neboule-nboules[:,kk])))
        return sum(distance)

    eboules = array([opt.fmin(fonctionnelle,zeros(2),(kk,),disp=False) for kk in xrange(oboules.shape[1])]).transpose()
    return eboules

print "click points"
omx,omy = meshgrid(arange(-5,6),arange(-5,6))
display_grid(omx,omy)
#oboules = array([(0,0)]+ginput(7)).transpose()
oboules = array(ginput(3)).transpose()
close()

print "generating data"
datas = []
for theta in linspace(0,2*pi,10,endpoint=False):
    cameraplan = 2*randn(2)
    camerasphere = array((20+randn()*8,theta,.1+random()*.3))
    camerazoom = 20.
    nboules = petanque.project_points(oboules,cameraplan,camerasphere,camerazoom)
    datas.append(((cameraplan,camerasphere,camerazoom),nboules))

print "estimating positions"
eboules = estimate_boules(datas)

print "display results"
display_grid(omx,omy)
plot(oboules[0,:],oboules[1,:],'go-')
plot(eboules[0,:],eboules[1,:],'r*-')
title('plan de la table')

for kk,((cameraplan,camerasphere,camerazoom),nboules) in enumerate(datas):
    neboules = petanque.project_points(eboules,cameraplan,camerasphere,camerazoom)
    nmx,nmy = project_grid(omx,omy,cameraplan,camerasphere,camerazoom)
    display_grid(nmx,nmy)
    plot(nboules[0,:],nboules[1,:],'go-')
    plot(neboules[0,:],neboules[1,:],'r*-')
    title("config %d" % kk)

show()
