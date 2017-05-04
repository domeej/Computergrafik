from PIL import Image
import Camera

from Material import Material, CheckerboardMaterial
from Geometry import Ray, Vector, Sphere, Triangle, Plane


max_level = 3
BACKGROUND_COLOR = Vector((0, 0, 0))


def shade(hitpoint, hitobj, ray, objectlist, lightlist):
    """calculates the final color at the given hitpoint. recursive-depth is given by CONSTANT:max_level"""
    objcolor = hitobj.material.baseColorAt(hitpoint)
    amb_color = objcolor.scale(hitobj.material.amb)
    n = hitobj.normalAt(hitpoint)
    color = amb_color

    # fuer jede lichtquelle
    for light in lightlist:
        lightdir = light - hitpoint
        l = lightdir.normalized()
        shadowray = Ray(hitpoint, lightdir)
        shadow = False

        # fuer jedes objekt
        for object in objectlist:
            hitdist = object.intersectionParameter(shadowray)
            if hitdist and hitdist > 0:
                shadow = True

        difuse_factor = n.dot(l)


        if difuse_factor < 0: # diffuse nicht dunkler als schatten
            difuse_factor = 0
        lr = (l.scale(-1) - n.scale((2 * l.scale(-1).dot(n)))).normalized()
        specular_factor = lr.dot(ray.direction.scale(-1)) # specular anteil


        if specular_factor < 0:
            specular_factor = 0

        dif_color = objcolor.scale(hitobj.material.dif * difuse_factor) #diffuse anteil
        spec_color = objcolor.scale(hitobj.material.spec * specular_factor ** 18) #specular anteil

        if shadow == False:
            color += dif_color + spec_color

    ref_factor = hitobj.material.ref

    if ref_factor and ray.level <= max_level:
        dr = (ray.direction - n.scale((2 * ray.direction.dot(n)))).normalized()
        reflectionray = Ray(hitpoint, dr, ray.level + 1) # ray.level gibt rekursionstiefe des ray an
        reflectedcolor = traceRay(reflectionray, objectlist, lightlist)
        color = color.scale(1 - ref_factor) + reflectedcolor.scale(ref_factor)

    return color


def traceRay(ray, objectlist, lightlist, hitobj=None):
    """traces a ray shot into the scene to check it's collisions with objects"""
    maxdist = float('inf')
    color = BACKGROUND_COLOR

    for object in objectlist:
        hitdist = object.intersectionParameter(ray)
        if hitdist and hitdist > 0: # getroffen
            if hitdist < maxdist:
                maxdist = hitdist  # ermittle schnittpunkt welcher naeher an der camera liegt
                color = (int(hitdist), int(hitdist), int(hitdist))
                hitobj = object

    if hitobj:
        hitpoint = ray.pointAtParameter(maxdist - 0.01)
        color = shade(hitpoint, hitobj, ray, objectlist, lightlist)  # ermittle endgueltige Farbe am schnittpunkt

    return color

def renderScene(cam, objectlist, lightlist):
    """render the current Scene"""
    image = Image.new("RGB", (cam.wres, cam.hres))

    for x in range(cam.wres):
        for y in range(cam.hres):
            ray = cam.calcRay(x, y)
            color = traceRay(ray, objectlist, lightlist)
            image.putpixel((x, y), (int(color.x), int(color.y), int(color.z)))

    image.save(r"C:\Users\Domee\Desktop\raytracer.png")
    image.show()


def buildScene():
    """creates all the Objects in the Scene"""
    cam = Camera.Camera(Vector((0, 1.8, 10)), Vector((0, 3, 0)), Vector((0, 1, 0)), 45, 400, 400)
    lightlist = []
    lightlist.append(Vector((30, 30, 10)))

    objectlist = []
    plane = Plane(Vector((0, 0, 0)), Vector((0, 1, 0)), CheckerboardMaterial(0.1, 0.8, 1))
    sphere1 = Sphere(Vector((-1.5, 3, 0)), 1, Material(0.1, 0.8, 1, Vector((255, 0, 0)), 0.3))
    sphere2 = Sphere(Vector((1.5, 3, 0)), 1, Material(0.1, 0.8, 1, Vector((0, 255, 0)), 0.3))
    sphere3 = Sphere(Vector((0, 5.5, 0)), 1, Material(0.1, 0.8, 1, Vector((0, 0, 255)), 0.3))
    triangle = Triangle(Vector((-1.5, 3, 0)), Vector((1.5, 3, 0)), Vector((0, 5.5, 0)), Material(0.1, 0.8, 1, Vector((255, 255, 0))))
    objectlist.append(plane)
    objectlist.append(sphere1)
    objectlist.append(sphere2)
    objectlist.append(sphere3)
    objectlist.append(triangle)

    renderScene(cam, objectlist, lightlist)


if __name__ == '__main__':
    buildScene()
