"""Conservative LOD1 preparation for repeated / over-budget modules, never the hero ship."""
import bpy,json,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];path=ROOT/'assets-source/blender/visual/manifest.json';manifest=json.loads(path.read_text())
for asset in ['building_governor','building_church','prop_palm','prop_palm_b','building_house_a','building_house_b','building_house_c','building_warehouse','building_warehouse_b','prop_tropical_tree','prop_tropical_tree_b']:
 a=manifest['assets'][asset];bpy.ops.wm.open_mainfile(filepath=str(ROOT/a['source']))
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH':continue
  if any(s in ob.name for s in ['shutter_louvre','flower_box','trunk_growth_ring','old_frond_scar']):
   bpy.data.objects.remove(ob,do_unlink=True);continue
  bpy.context.view_layer.objects.active=ob
  if 'roof_tiles' in ob.name:
   # At distance use the same roof envelope and paired tile material; decimating
   # thousands of disconnected curved tiles creates pinholes and aliasing.
   coords=[v.co for v in ob.data.vertices];x0=min(v.x for v in coords);x1=max(v.x for v in coords);y0=min(v.y for v in coords);y1=max(v.y for v in coords);low=min(v.z for v in coords);high=max(v.z for v in coords)
   material=ob.data.materials[0];d=bpy.data.meshes.new('LOD1_continuous_roof');d.from_pydata([(x0,y0,low),(x1,y0,low),(0,y0,high),(x0,y1,low),(x1,y1,low),(0,y1,high)],[],[(0,2,5,3),(2,1,4,5)]);d.materials.append(material);d.update();ob.data=d
   uv=d.uv_layers.new(name='MetricUV')
   for poly in d.polygons:
    for li in poly.loop_indices:
     v=d.vertices[d.loops[li].vertex_index].co;uv.data[li].uv=(v.x/4,v.y/4)
   continue
  if len(ob.data.polygons)>20:
   dec=ob.modifiers.new('LOD1_retain_outline','DECIMATE');dec.ratio=.48 if 'roof_tiles' in ob.name else .65
   bpy.ops.object.modifier_apply(modifier=dec.name)
 source=str(Path(a['source']).with_stem(asset+'_lod1'));url=a['url'].replace(asset+'.glb',asset+'_lod1.glb')
 bpy.data.libraries.write(str(ROOT/source),{bpy.context.scene},fake_user=True,compress=True)
 groups={}
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':groups.setdefault((ob.data.materials[0].name,ob.get('facadeOption',-1)),[]).append(ob)
 for (material_name,option),group in groups.items():
  bpy.ops.object.select_all(action='DESELECT')
  for ob in group:ob.select_set(True)
  bpy.context.view_layer.objects.active=group[0]
  if len(group)>1:bpy.ops.object.join()
  bpy.context.object.name=('facade_'+str(option) if option>=0 else 'base')+'__'+material_name
 tris=0
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':ob.data.calc_loop_triangles();tris+=len(ob.data.loop_triangles)
 bpy.ops.export_scene.gltf(filepath=str(ROOT/('public'+url)),export_format='GLB',export_yup=True,export_vertex_color='ACTIVE')
 manifest['assets'][asset+'_lod1']={**a,'source':source,'url':url,'triangles':tris,'lod':'LOD1','lodOf':asset,'status':'Task07 LOD1'}
for asset in list(manifest['assets'].values()):
 if 'lodOf' in asset:manifest['assets'][asset['lodOf']]['lod']='LOD0 + LOD1'
path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2));runpy.run_path(str(ROOT/'scripts/optimize_visual_glb.py'))
