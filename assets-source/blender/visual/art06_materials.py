"""Paired material families: all channels derive from one authored relief field.
No raster conversion of the previous atlas. Blender creates the source images.
"""
textures={}
material_specs={
 'wall':('Plaster',(.69,.65,.54),4,'plaster'), 'stone':('Stone',(.39,.40,.35),4,'stone'),
 'roof':('RoofTile',(.31,.14,.077),4,'tile'), 'wood':('WoodStructural',(.30,.205,.115),4,'wood'),
 'deck':('WoodDeck',(.38,.265,.145),4,'wood'), 'cloth':('SailCloth',(.72,.69,.58),4,'cloth'),
 'ground':('TerrainGrass',(.22,.27,.125),4,'grass'), 'dirt':('TerrainDirt',(.32,.265,.17),4,'soil'),
 'rock':('TerrainRock',(.36,.355,.30),4,'rock'), 'sand':('Sand',(.62,.575,.43),4,'sand')}
(OUT/'textures/art06').mkdir(parents=True,exist_ok=True)
for idx,(key,(family,color,metres,kind)) in enumerate(material_specs.items()):
 rng=np.random.default_rng(6000+idx);n=1024;yy,xx=np.mgrid[0:n,0:n];u=xx/n;v=yy/n
 micro=rng.normal(0,.0017,(n,n));mottle=np.sin(u*math.tau*3+np.sin(v*math.tau*2))*.5+np.sin(v*math.tau*7+u*13)*.23
 height=micro+mottle*.003;variation=mottle*.018;seam=np.zeros_like(u)
 if kind=='wood':
  # Eight 0.5m plank widths, staggered 2m joints; grain runs along V.
  column=xx//128;seam=np.maximum(np.exp(-((xx%128)/2)**2),np.exp(-((yy+column*211)%768/2)**2))
  grain=np.sin(u*math.tau*93+np.sin(v*math.tau*2)*1.7+np.sin(u*math.tau*7)*2)
  height+=grain*.0015-seam*.027;variation+=grain*.014-seam*.13+(column%3-1)*.018
 elif kind=='stone':
  row=yy//128;seam=np.maximum(np.exp(-((yy%128)/3)**2),np.exp(-(((xx+row%2*128)%256)/4)**2))
  height-=seam*.025;variation-=seam*.065;variation+=((xx//256+row*3)%5-2)*.012
 elif kind=='plaster':
  crack=np.exp(-(np.abs(np.sin(v*13+u*37+np.sin(v*21)*.4))/.021)**2)*np.exp(-((u-.35)/.14)**2)
  height-=crack*.012;variation-=crack*.045
 elif kind=='tile':
  height+=np.sin(u*math.tau*8)*.012;variation+=np.sin(v*math.tau*5+u*12)*.018
 elif kind=='cloth':
  height+=.0018*(np.cos(xx*math.pi*.5)+np.cos(yy*math.pi*.5));variation+=.012*np.sin(u*math.tau*4)*np.sin(v*math.tau*3)
 elif kind=='rock':
  strata=np.sin((v*5+u*.65)*math.tau);height+=strata*.016;variation+=strata*.025
 elif kind=='grass':variation+=.019*np.sin(u*math.tau*63+np.sin(v*math.tau*27)*3)
 albedo=np.clip(np.array(color)+variation[:,:,None],.015,.95)
 gy,gx=np.gradient(height);norm=np.stack((-gx*n/metres,-gy*n/metres,np.ones_like(gx)),axis=-1);norm/=np.linalg.norm(norm,axis=-1)[:,:,None]
 rough=np.clip((.88 if kind in ['plaster','grass','soil','sand'] else .77)+mottle*.045+seam*.10-height*.6,.55,.96)
 maps={}
 for suffix,rgb,space in [('color',albedo,'sRGB'),('normal',norm*.5+.5,'Non-Color'),('roughness',np.repeat(rough[:,:,None],3,axis=-1),'Non-Color')]:
  rgba=np.ones((n,n,4),np.float32);rgba[:,:,:3]=rgb
  im=bpy.data.images.new(f'{family}_{suffix}',width=n,height=n,alpha=False);im.colorspace_settings.name=space;im.pixels.foreach_set(rgba.ravel());im.filepath_raw=str(OUT/f'textures/art06/{family}_{suffix}.png');im.file_format='PNG';im.save();textures[f'{family}_{suffix}']=im;maps[suffix]=im
 m=bpy.data.materials.new('art06_'+family);m.use_nodes=True;nodes=m.node_tree.nodes;links=m.node_tree.links;p=nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.8
 uv=nodes.new('ShaderNodeUVMap');uv.uv_map='MetricUV'
 for suffix,socket in [('color','Base Color'),('roughness','Roughness')]:
  t=nodes.new('ShaderNodeTexImage');t.image=maps[suffix];links.new(uv.outputs['UV'],t.inputs['Vector']);links.new(t.outputs['Color'],p.inputs[socket])
 t=nodes.new('ShaderNodeTexImage');t.image=maps['normal'];links.new(uv.outputs['UV'],t.inputs['Vector']);nm=nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.55;links.new(t.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],p.inputs['Normal'])
 M[key]=m
M['ochre']=M['wall'];M['bark']=mat('art06_weathered_bark',(.12,.105,.071),.92)
M['leaf']=mat('art06_leaf_shade',(.035,.09,.018),.88);M['leaflight']=mat('art06_leaf_sun',(.095,.18,.043),.83)

def prepare_surfaces():
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  data=ob.data
  if 'TerrainUV' in data.uv_layers:continue
  while data.uv_layers:data.uv_layers.remove(data.uv_layers[0])
  uv=data.uv_layers.new(name='MetricUV')
  for poly in data.polygons:
   axis=max(range(3),key=lambda k:abs(poly.normal[k]));axes=[k for k in range(3) if k!=axis]
   # World-within-module coordinates keep neighboring components at the same phase.
   for li in poly.loop_indices:
    pt=ob.matrix_world@data.vertices[data.loops[li].vertex_index].co
    uv.data[li].uv=(pt[axes[0]]/4,pt[axes[1]]/4)
  if not data.color_attributes:
   ca=data.color_attributes.new(name='SurfaceTint',type='BYTE_COLOR',domain='CORNER');seed=sum(map(ord,ob.name))
   for poly in data.polygons:
    for li in poly.loop_indices:
     pt=ob.matrix_world@data.vertices[data.loops[li].vertex_index].co
     f=.95
     if 'roof_tiles' in ob.name:
      tile=(poly.index//4*37)%43;f=.78+tile/200
     elif 'stucco' in ob.name or 'plinth' in ob.name:
      # Subtle salt/damp at the wall foot, without painting every facade into ruins.
      f=.80+.18*min(1,max(0,(pt.z-.4)/2.1));f*=.96+.025*math.sin(pt.x*.75+pt.y*.45)
     tint=(1,.985,.965)
     if 'stucco' in ob.name:
      asset=bpy.context.collection.name
      tint=(1,.94,.79) if 'house_b' in asset else ((.88,.96,.86) if 'merchant_b' in asset else (1,.985,.965))
     ca.data[li].color=(f*tint[0],f*tint[1],f*tint[2],1)
  data.uv_layers.active_index=0
# Preserve independent source objects, export vertex color, never repack baked UVs.
finish_source=base[base.index('def finish('):].replace('bpy.ops.uv.smart_project(island_margin=.015);','')
finish_source=finish_source.replace("bpy.ops.object.mode_set(mode='OBJECT')","bpy.ops.object.mode_set(mode='OBJECT');prepare_surfaces()")
finish_source=finish_source.replace('export_yup=True)',"export_yup=True,export_vertex_color='ACTIVE')")
finish_source=finish_source.replace('bpy.ops.wm.save_as_mainfile(filepath=str(source))','bpy.data.libraries.write(str(source), {bpy.context.scene}, fake_user=True, compress=True)')
exec(finish_source)
