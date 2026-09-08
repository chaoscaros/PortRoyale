"""Re-export editable catalogued sources after Blender art edits; preserves source objects.
Run from Blender --background --python; runtime primitives merge by material.
"""
from pathlib import Path
import bpy,json,runpy
ROOT=Path(__file__).resolve().parents[3]
manifest_path=ROOT/'assets-source/blender/visual/manifest.json'
m=json.loads(manifest_path.read_text())
for name,a in m['assets'].items():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['source']))
    groups={}
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH':groups.setdefault(ob.data.materials[0].name,[]).append(ob)
    for group in groups.values():
        bpy.ops.object.select_all(action='DESELECT')
        for ob in group:ob.select_set(True)
        bpy.context.view_layer.objects.active=group[0]
        if len(group)>1:bpy.ops.object.join()
    count=0
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH':ob.data.calc_loop_triangles();count+=len(ob.data.loop_triangles)
    a['triangles']=count
    bpy.ops.export_scene.gltf(filepath=str(ROOT/('public'+a['url'])),export_format='GLB',export_yup=True,export_vertex_color='ACTIVE')
manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2))
runpy.run_path(str(ROOT/'scripts/optimize_visual_glb.py'))
