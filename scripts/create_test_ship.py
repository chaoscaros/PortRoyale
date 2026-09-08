"""Run: Blender --background --python scripts/create_test_ship.py"""
import bpy
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    return m
wood = material('warm_oak', (.23,.12,.055))
canvas = material('ivory_canvas', (.89,.82,.63))
gold = material('bow_gold', (.8,.43,.12))

def mesh(name, vertices, faces, mat):
    data=bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces);data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj
# Blender +Z up, -Y forward. Waterline pivot at origin; 20m hull.
mesh('ship_test_hull', [(-3,8,0),(3,8,0),(4,-5,0),(0,-12,0),(-4,-5,0),(-2,7,-2),(2,7,-2),(2,-5,-2),(0,-10,-2),(-2,-5,-2)], [(0,4,3,2,1),(5,6,7,8,9),(0,1,6,5),(1,2,7,6),(2,3,8,7),(3,4,9,8),(4,0,5,9)],wood)
for name,loc,scale,mat in [('mast',(0,0,6),(.25,.25,7),wood),('boom',(0,0,10),(5,.18,.18),wood),('bow_tip',(0,-11.5,.5),(.3,.3,.5),gold)]:
    bpy.ops.mesh.primitive_cube_add(size=2,location=loc)
    obj=bpy.context.object;obj.name=name;obj.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    obj.data.materials.append(mat)
mesh('sail', [(-4.8,0,10),(4.8,0,10),(3.8,-.8,3),(-3.8,-.8,3),(0,-1.5,6)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],canvas)
# Named empties make the coordinate test unambiguous.
for name,loc in [('axis_forward',(0,-10,0)),('axis_up',(0,0,10)),('axis_right',(10,0,0))]:
    obj=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(obj);obj.location=loc
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets-source/blender/ships/ship_test.blend'))
bpy.ops.export_scene.gltf(filepath=str(ROOT/'public/assets/models/ship_test.glb'),export_format='GLB',export_yup=True)
