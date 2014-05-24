from color import *
from core import *
from vector import *
import logging
import inspect
import sys

_current_module = sys.modules[__name__]
logger = logging.getLogger(__name__)

class Color(SCAD_Primitive):
    SCAD_Name = "color"

    Aliases = {
        # red
        'red': '_color.r',
        'r': '_color.r',
        'R': '_color.r',
        # green
        'green': '_color.g',
        'g': '_color.g',
        'G': '_color.g',
        # blue
        'blue': '_color.b',
        'b': '_color.b',
        'B': '_color.b',
        # alpha
        'alpha': '_color.a',
        'a': '_color.a',
        'A': '_color.a',
        # color
        'color': '_color.color',
    }
    Defaults = {
        "_color": {"type": VectorColor, "default": lambda: VectorColor()},
    }
    def process_args(self, args):
        return VectorColor(args).namespace

class Projection(SCAD_Primitive):
    SCAD_Name = "projection"
    Defaults = {
        "cut": {"type": bool, "default": False}
    }

class Union(SCAD_Primitive):
    SCAD_Name = "union"

class Difference(SCAD_Primitive):
    SCAD_Name = "difference"

class Intersection(SCAD_Primitive):
    SCAD_Name = "intersection"

class Minowski(SCAD_Primitive):
    SCAD_Name = "minowski"

class Hull(SCAD_Primitive):
    SCAD_Name = "hull"

class Render(SCAD_Primitive):
    SCAD_Name = "render"

class Rotate(Vector3D_SCAD_Primitive):
    SCAD_Name = "rotate"

class Translate(Vector3D_SCAD_Primitive):
    SCAD_Name = "translate"

class Polyhedron(Vector3D_SCAD_Primitive):
    SCAD_Name = "polyhedron"
    Defaults = {
        "points": {"type": ListVector3D, "cast": lambda x: ListVector3D(*x)},
        "faces": {"type": ListVector3D, "cast": lambda x: ListVector3D(*x)},
        "convexity": {"type": int, "default": None},
    }
    def get_scad_args(self):
        pts = [list(i) for i in self.points]
        faces = [list(i) for i in self.faces]
        args = [("points", pts), ("faces", faces)]
        if self.convexity != None:
            args.append(("convexity", self.convexity))
        return args

class Cube(SCAD_Primitive):
    SCAD_Name = "cube"
    Aliases = {
        'x': 'size.x',
        'y': 'size.y',
        'z': 'size.z',
    }
    Defaults = {
        "size": {"type": Vector3D, "default": lambda: Vector3D(1.0, 1.0, 1.0)},
        "center": {"type": bool, "default": False},
    }

    def get_scad_args(self):
        return [self.size, ("center", self.center)]

    def get_size(self):
        return self["size"]

    def set_size(self, size):
        if type(size) in (int, float):
            size = [size] * 3
        self["size"] = Vector3D(size)
    size = property(get_size, set_size)

    def process_args(self, args):
        ret = {}
        if args:
            ret["size"] = args[0] if (len(args) == 1) else args
        return ret

class Cylinder(SCAD_Primitive):
    SCAD_Name = "cylinder"
    Aliases = {
        'fn': 'resolution.fn',
        'fa': 'resolution.fa',
        'fs': 'resolution.fs',
        'radius': 'radius_1',
        'r': 'radius_1',
        'r1': 'radius_1',
        'r2': 'radius_2',
        'diameter': 'diameter_1',
        'd': 'diameter_1',
        'd1': 'diameter_1',
        'd2': 'diameter_2',
        'h': 'height',
    }
    Defaults = {
        "radius_1": {"type": float, "default": 1.0},
        "radius_2": {"type": float, "default": None},
        "center": {"type": bool, "default": False},
        "resolution": {"type": RadialResolution, "default": lambda: RadialResolution()},
        "height": {"type": float, "default": 1.0},
    }

    def get_scad_args(self):
        scad = []
        if not self.r2:
            scad.append(("r", self.radius_1))
        else:
            scad.append(("r1", self.radius_1))
            scad.append(("r2", self.radius_2))
        scad.append(("h", self.height))
        scad.append(("center", self.center))
        scad += self.resolution.get_scad_args()
        return scad

    def get_diamater_1(self):
        return self.radius_1 * 2
    def set_diamater_1(self, dia):
        self.radius_1 = dia / 2.0
    diameter_1 = property(get_diamater_1, set_diamater_1)

    def get_diamater_2(self):
        return self.radius_2 * 2
    def set_diamater_2(self, dia):
        self.radius_2 = dia / 2.0
    diameter_2 = property(get_diamater_2, set_diamater_2)

class Sphere(SCAD_Primitive):
    SCAD_Name = "sphere"
    Aliases = {
        'fn': 'resolution.fn',
        'fa': 'resolution.fa',
        'fs': 'resolution.fs',
        'r': 'radius',
        'd': 'diameter',
    }
    Defaults = {
        "radius": {"type": float, "default": 1.0},
        "center": {"type": bool, "default": False},
        "resolution": {"type": RadialResolution, "default": lambda: RadialResolution()},
    }

    def get_scad_args(self):
        scad = []
        scad.append(("r", self.radius))
        scad.append(("center", self.center))
        scad += self.resolution.get_scad_args()
        return scad

    def get_diamater(self):
        return self.radius * 2
    def set_diamater(self, dia):
        self.radius = dia / 2.0
    diameter = property(get_diamater, set_diamater)

#
# auto generate __all__
#

__all__ = [name for (name, obj) in globals().items() if (inspect.getmodule(obj) == _current_module) and inspect.isclass(obj) and issubclass(obj, SCAD_Primitive)]