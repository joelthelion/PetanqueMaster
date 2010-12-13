__all__ = ["project_points","estimate_positions"]

from scipy import *
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
        if warn==1: print "WARNING: max function call reached"
        if warn==2: print "WARNING: max iteration reached"
        positions_estimated.append(estimation)
    positions_estimated = vstack((array(positions_estimated).transpose(),radius*ones(kballs)))
    return positions_estimated


estimate_positions = estimate_positions_without_radius
