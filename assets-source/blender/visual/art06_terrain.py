"""Native Blender surface bake: one UV for matched color, relief and roughness."""
terrain=o;data=o.data
while data.uv_layers:data.uv_layers.remove(data.uv_layers[0])
uv=data.uv_layers.new(name='TerrainUV')
for poly in data.polygons:
 poly.use_smooth=True
 for li in poly.loop_indices:
  p=data.vertices[data.loops[li].vertex_index].co;uv.data[li].uv=((p.x+141)/209,(-p.y+7)/171)
for name in ['BeachMask','RockMask','DirtMask']:
 ca=data.color_attributes.new(name=name,type='FLOAT_COLOR',domain='CORNER')
 for poly in data.polygons:
  for li in poly.loop_indices:
   pt=data.vertices[data.loops[li].vertex_index].co;x,z,h=pt.x,-pt.y,pt.z
   if name=='BeachMask':f=smooth(.3,3.8,h)
   elif name=='RockMask':
    slope=math.hypot(terrain_height(x+.5,z)-terrain_height(x-.5,z),terrain_height(x,z+.5)-terrain_height(x,z-.5))
    f=max(smooth(.8,1.7,slope),smooth(18,27,h)*.65)*smooth(103,120,z)
   else:f=.82 if in_town(x,z,4) else .14+.13*math.sin(x*.13+z*.08)
   ca.data[li].color=(f,f,f,1)
m=bpy.data.materials.new('art06_terrain_bake');m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');l.new(em.outputs[0],out.inputs['Surface'])
geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],sep.inputs[0]);combine=n.new('ShaderNodeCombineXYZ');l.new(sep.outputs['X'],combine.inputs['X']);l.new(sep.outputs['Y'],combine.inputs['Y'])
scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=.25;l.new(combine.outputs[0],scale.inputs[0])
def image_tex(family,suffix):
 t=n.new('ShaderNodeTexImage');t.image=textures[family+'_'+suffix];l.new(scale.outputs[0],t.inputs['Vector']);return t.outputs['Color']
def attr(name):
 t=n.new('ShaderNodeVertexColor');t.layer_name=name;return t.outputs['Color']
def mix(a,b,f):
 t=n.new('ShaderNodeMixRGB');l.new(a,t.inputs[1]);l.new(b,t.inputs[2]);l.new(f,t.inputs[0]);return t.outputs[0]
beach,rock,dirt=attr('BeachMask'),attr('RockMask'),attr('DirtMask')
# World-space moisture patches avoid aliasing a tiny grass tile into a checkerboard.
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.055;noise.inputs['Detail'].default_value=4;noise.inputs['Roughness'].default_value=.7;l.new(geo.outputs['Position'],noise.inputs['Vector'])
patch=n.new('ShaderNodeMixRGB');patch.inputs[1].default_value=(.16,.215,.073,1);patch.inputs[2].default_value=(.28,.30,.13,1);l.new(noise.outputs['Fac'],patch.inputs[0])
grass=n.new('ShaderNodeMixRGB');grass.inputs[0].default_value=.12;l.new(patch.outputs[0],grass.inputs[1]);l.new(image_tex('TerrainGrass','color'),grass.inputs[2])
color=mix(grass.outputs[0],image_tex('TerrainDirt','color'),dirt)
color=mix(image_tex('Sand','color'),color,beach);color=mix(color,image_tex('TerrainRock','color'),rock)
# Wet-sand band is part of the baked surface, preserving the coast's elevation logic.
wet=n.new('ShaderNodeMixRGB');wet.blend_type='MULTIPLY';wet.inputs[2].default_value=(.65,.68,.62,1);wet.inputs[0].default_value=.16;l.new(color,wet.inputs[1]);color=wet.outputs[0]
rough=mix(image_tex('TerrainGrass','roughness'),image_tex('TerrainRock','roughness'),rock)
normal=mix(image_tex('TerrainGrass','normal'),image_tex('TerrainRock','normal'),rock)
data.materials.clear();data.materials.append(m)
bpy.context.scene.render.engine='CYCLES';bpy.context.scene.cycles.samples=1
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
maps={}
for suffix,output in [('color',color),('normal',normal),('roughness',rough)]:
 l.new(output,em.inputs['Color'])
 im=bpy.data.images.new('HarborTerrain_'+suffix,width=2048,height=2048,alpha=False)
 if suffix!='color':im.colorspace_settings.name='Non-Color'
 target=n.new('ShaderNodeTexImage');target.image=im;n.active=target
 bpy.ops.object.bake(type='EMIT',margin=8)
 im.filepath_raw=str(OUT/f'textures/art06/HarborTerrain_{suffix}.png');im.file_format='PNG';im.save();textures['HarborTerrain_'+suffix]=im;maps[suffix]=im
material=bpy.data.materials.new('art06_HarborTerrain');material.use_nodes=True;n=material.node_tree.nodes;l=material.node_tree.links;p=n.get('Principled BSDF');uvn=n.new('ShaderNodeUVMap');uvn.uv_map='TerrainUV'
for suffix,socket in [('color','Base Color'),('roughness','Roughness')]:
 t=n.new('ShaderNodeTexImage');t.image=maps[suffix];l.new(uvn.outputs[0],t.inputs['Vector']);l.new(t.outputs['Color'],p.inputs[socket])
t=n.new('ShaderNodeTexImage');t.image=maps['normal'];l.new(uvn.outputs[0],t.inputs['Vector']);nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.10;l.new(t.outputs['Color'],nm.inputs[1]);l.new(nm.outputs[0],p.inputs['Normal'])
data.materials.clear();data.materials.append(material)
while data.color_attributes:data.color_attributes.remove(data.color_attributes[0])
# The water samples the same authored ground heights, rather than an unrelated island equation.
nsize=256;rgba=np.ones((nsize,nsize,4),np.float32)
for row in range(nsize):
 for col in range(nsize):
  h=terrain_height(-141+(col+.5)/nsize*209,-7+(row+.5)/nsize*171)
  rgba[row,col,:3]=clamp((h+8)/48)
im=bpy.data.images.new('HarborDepth',width=nsize,height=nsize,alpha=False);im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(rgba.ravel());im.filepath_raw=str(OUT/'textures/art06/HarborDepth.png');im.file_format='PNG';im.save();textures['HarborDepth']=im
