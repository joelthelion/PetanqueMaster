__all__ = ["project_points"]

from scipy import *

def cart_from_sphere(pointsphere):
    assert(pointsphere[0]>0)
    assert(pointsphere[2]>=0 and pointsphere[2]<=pi/2)
    return pointsphere[0]*array([sin(pointsphere[1])*sin(pointsphere[2]),-cos(pointsphere[1])*sin(pointsphere[2]),cos(pointsphere[2])])

def norm_cart_from_sphere(pointsphere):
    return cart_from_sphere((1,pointsphere[1],pointsphere[2]))

def project_points(pointsplan,cameraplan,camerasphere,zoom):
    cameraouter = cart_from_sphere(camerasphere)
    cameraouter_norm = norm_cart_from_sphere(camerasphere)
    cameraup = cart_from_sphere([1,pi+camerasphere[1],pi/2-camerasphere[2]])
    assert(abs(dot(cameraouter_norm,cameraup))<10e-5)
    rot = array([cross(cameraup,cameraouter_norm),cameraup,cameraouter_norm])
    points = dot(rot,vstack([pointsplan[0,:]-cameraplan[0]-cameraouter[0],pointsplan[1,:]-cameraplan[1]-cameraouter[1],zeros(pointsplan.shape[1])-cameraouter[2]]))
    assert((points[2,:]<0).all())
    return -zoom*points[:2,:]/points[2,:]
