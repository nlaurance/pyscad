# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
import math
import json
import os
from solid import *
import logging
import operator

logger = logging.getLogger(__name__)

python = new_openscad_class_str("polyhedron", [], ["faces", "triangles", "points"])
exec python

def subtract_vector(v1, v2):
    return [operator.sub(*args) for args in zip(v1, v2)]

def tetrahedron(height, center=False):
    edge = height / math.sqrt(2.0/3.0)
    points = [
        [0, 0, 0],
        [math.cos(math.radians(15)) * edge, math.sin(math.radians(15)) * edge, 0],
        [math.cos(math.radians(75)) * edge, math.sin(math.radians(75)) * edge, 0],
        [height / 2.0, height / 2.0, height],
    ]
    faces = [[0, 1, 2], [1, 0, 3], [0, 2, 3], [2, 1, 3]]
    if center:
        cv = (height / 2.0, height / 2.0, height / 2.0)
        points = [subtract_vector(vv, cv) for vv in points]
    return polyhedron(points=list(points), faces=list(faces))

def pyramid(name, height, width=None, depth=None, center=False):
    if width == None:
        width = height
    if depth == None:
        depth = width
    msg = "Pyramid [%s]: height=%.4f width=%.4f, depth: %.4f" % (name, height, width, depth)
    logger.debug(msg)
    points = [
        [0, 0, 0],
        [width, depth, 0],
        [width, 0, 0],
        [0, depth, 0],
        [width / 2, depth / 2, height],
    ]
    faces = [[0, 2, 1], [0, 1, 3], [2, 0, 4], [0, 3, 4], [3, 1, 4], [1, 2, 4]]
    if center:
        cv = (height / 2, width / 2, depth / 2)
        points = [subtract_vector(vv, cv) for vv in points]
    return polyhedron(points=list(points), faces=list(faces))

def tube(name, height, outer_dia, inner_dia, segments=None):
    msg = "Tube [%s]: Dia: inner=%.4f outer=%.4f, Height: %.4f" % (name, inner_dia, outer_dia, height)
    logger.debug(msg)
    return difference() (
        cylinder(h=height, r=outer_dia / 2.0, segments=segments),
        cylinder(h=height, r=inner_dia / 2.0, segments=segments)
    )

def tube2(name, height, outer_dia1, inner_dia1, outer_dia2, inner_dia2, segments=None):
    msg = "Tube2 [%s]: Dia1: inner=%.4f outer=%.4f, Dia2: inner=%.4f outer=%.4f, Height: %.4f" % (name, inner_dia1, outer_dia1, inner_dia2, outer_dia2, height)
    logger.debug(msg)
    return difference() (
        cylinder(h=height, r1=outer_dia1 / 2.0, r2=outer_dia2 / 2.0, segments=segments),
        cylinder(h=height, r1=inner_dia1 / 2.0, r2=inner_dia2 / 2.0, segments=segments),
    )

def get_midpoint(points):
    return [sum(pts) / 2.0 for pts in zip(*points)]

def render_crosshairs(length=25, width=1, height=1, rad=2):
    scad = \
        union()([
            # red
            rotate([0, 90, 0])( 
                translate([0, -width, -length/ 2.0 + width])( color([1, 0, 0])( cube([width, height, length]) ) ),
                translate([rad / 4.0, rad / 4.0 - width, length / 2.0])( color([1, 0, 0])( sphere(rad) ) ),
            ), 
            # green
            rotate([-90, 0, 0])( 
                translate([0, 0, -length / 2.0])( color([0, 1, 0])( cube([width, height, length]) ) ), 
                translate([rad / 4.0, rad / 4.0, length / 2.0])( color([0, 1, 0])( sphere(rad) ) ),
            ), 
            # blue
            rotate([0, 0, -90])( 
                translate([0, 0, -length/ 2.0])( color([0, 0, 1])( cube([width, height, length]) ) ),
                translate([rad / 4.0,  rad / 4.0, length / 2.0])( color([0, 0, 1])( sphere(rad) ) ),
            ), 
        ])
    return scad

def save_json(obj, json_fn, lazy=True):
    if os.path.exists(json_fn) and lazy:
        return
    msg = "saving %s" % json_fn
    logger.info(msg)
    with open(json_fn, 'w') as fh:
        json.dump(obj, fh, sort_keys=True, indent=4, separators=(',', ': '))

def load_json(json_fn):
    msg = "loading %s" % json_fn
    logger.info(msg)
    with open(json_fn) as fh:
        content = fh.read()
    content = str.join('', [line.strip() for line in content.split('\n')])
    obj = json.loads(content)
    return obj

def save_stl(openscad, scadfn, stlfn, lazy=True):
    if os.path.exists(stlfn) and lazy:
        return
    cmd = "%s -m make -o %s %s" % (openscad, stlfn, scadfn)
    msg = "executing '%s'" % cmd
    logger.info(msg)
    os.system(cmd)

def save_dxf(openscad, scadfn, dxffn, lazy=True):
    if os.path.exists(dxffn) and lazy:
        return
    cmd = "%s -m make -o %s %s" % (openscad, dxffn, scadfn)
    msg = "executing '%s'" % cmd
    logger.info(msg)
    os.system(cmd)

def save_png(openscad, scadfn, pngfn, lazy=True, make=True):
    if os.path.exists(pngfn) and lazy:
        return
    cmd = [openscad]
    if make:
        cmd.append("-m make")
    cmd.append("-o %s %s" % (pngfn, scadfn))
    cmd = str.join(' ', cmd)
    msg = "executing '%s'" % cmd
    logger.info(msg)
    os.system(cmd)

def save_scad(scad, scadfn, lazy=True):
    if os.path.exists(scadfn) and lazy:
        return
    msg = "saving %s" % scadfn
    logger.info(msg)
    scad = scad_render(scad)
    f = open(scadfn, 'w')
    f.write(scad)
    f.close()

def in2mm(inches):
    return inches / 0.0393701

def mm2in(mm):
    return mm * 0.0393701

def default(func):
    def _default(self, *args, **kwargs):
        if func.func_name in self and self[func.func_name] != None:
            return self[func.func_name]
        return func(self, *args, **kwargs)
    return property(_default)

class cproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

_parts = []
def scan_parts():
    if not _parts:
        from . import parts
        for name in dir(parts):
            if name in ["Root", "Part"]:
                continue
            thing = getattr(parts, name, None)
            try:
                if issubclass(thing, parts.RockitPart):
                    _parts.append(thing)
            except TypeError:
                continue
    return _parts

# scan for rocket parts
def get_part(name):
    parts = scan_parts()
    for part in parts:
        if name in part.names:
            return part
    raise KeyError, "Unknown rocket part: %s" % name

# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

# http://stackoverflow.com/questions/1724693/find-a-file-in-python
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
