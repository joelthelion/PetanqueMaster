__all__ = ["project_points","estimate_positions","display_grid","display_projections","project_grid"]

from pylab import *
import scipy.optimize as opt

def cart_from_sphere(pointsphere):
    assert(pointsphere[0]>0)
    assert(pointsphere[2]>=0 and pointsphere[2]<=pi/2)
    return pointsphere[0]*array([sin(pointsphere[1])*sin(pointsphere[2]),-cos(pointsphere[1])*sin(pointsphere[2]),cos(pointsphere[2])])

def norm_cart_from_sphere(pointsphere):
    return cart_from_sphere((1,pointsphere[1],pointsphere[2]))

def project_points(pointsplan,cameraplan,camerasphere,camerafocal):
    assert(pointsplan.shape[0]==3)
    assert(cameraplan.size==2)
    assert(camerasphere.size==3)
    assert(camerafocal>0)
    cameraouter = cart_from_sphere(camerasphere)
    cameraouter_norm = norm_cart_from_sphere(camerasphere)
    cameraup = cart_from_sphere([1,pi+camerasphere[1],pi/2-camerasphere[2]])
    assert(abs(dot(cameraouter_norm,cameraup))<10e-5)
    rot = array([cross(cameraup,cameraouter_norm),cameraup,cameraouter_norm])
    points = dot(rot,vstack([pointsplan[0,:]-cameraplan[0]-cameraouter[0],pointsplan[1,:]-cameraplan[1]-cameraouter[1],zeros(pointsplan.shape[1])-cameraouter[2]]))
    assert((points[2,:]<0).all())
    result = -camerafocal * vstack((points[:2,:]/points[2,:],pointsplan[2,:]/points[2,:]))
    return result

#TODO test other metric
def estimate_positions_without_radius(datas,radius):
    kballs = datas[0][1].shape[1]
    def fonctionnelle(position,kk):
        distance = 0
        for (cameraplan,camerasphere,camerafocal),projections_measure in datas:
            projections = project_points(array([[position[0],position[1],0]]).transpose(),cameraplan,camerasphere,camerafocal)
            distance += absolute(projections[:2]-projections_measure[:2,kk]).mean()
            #distance += square(projections-projections_measure[:,kk]).mean()
        return distance/len(datas)
    positions_estimated = []
    for kk in xrange(kballs):
        estimation,fopt,niter,ncall,warn = opt.fmin(fonctionnelle,zeros(2),(kk,),ftol=0,disp=True,maxfun=1000,full_output=True)
        if warn==1: print "WARNING: max function call reached (%d calls)" % ncall
        if warn==2: print "WARNING: max iteration reached (%d iters)" % niter
        positions_estimated.append(estimation)
    positions_estimated = vstack((array(positions_estimated).transpose(),radius*ones(kballs)))
    return positions_estimated

estimate_positions = estimate_positions_without_radius

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

def display_projections(factor,positions,style,label):
    for position in positions.transpose():
        gca().add_patch(Circle(factor*position[:2],factor*position[2],fill=True,alpha=.2))
    plot()
    plot(factor*positions[0,:],factor*positions[1,:],style,label=label)

def project_grid(mx,my,cameraplan,camerasphere,zoom):
    nmx = zeros(mx.shape)
    nmy = zeros(my.shape)
    foo = project_points(vstack((mx.ravel(),my.ravel(),zeros(mx.size))),cameraplan,camerasphere,zoom)
    mx = foo[0,:].reshape(nmx.shape)
    my = foo[1,:].reshape(nmy.shape)
    return mx,my

