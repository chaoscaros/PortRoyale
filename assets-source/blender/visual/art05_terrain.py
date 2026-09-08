"""Bake a continuous terrain albedo in Blender; blend materials before glTF export.
Sampling a repeated atlas happens in shader space, avoiding per-triangle UV resets.
"""
terrain=o
# Source shader uses metric coordinates and height masks; destination UV covers the island.
data=o.data
for layer in list(data.uv_layers):data.uv_layers.remove(layer)
uv=data.uv_layers.new(name='TerrainUV')
for poly in data.polygons:
    poly.use_smooth=True
    for li in poly.loop_indices:
        p=data.vertices[data.loops[li].vertex_index].co
        uv.data[li].uv=((p.x+141)/209,(-p.y+7)/171)
for name in ['BeachMask','RockMask']:
    ca=data.color_attributes.new(name=name,type='FLOAT_COLOR',domain='CORNER')
    for poly in data.polygons:
        for li in poly.loop_indices:
            p=data.vertices[data.loops[li].vertex_index].co;h=p.z
            f=float(np.clip((h-1.3)/2.8,0,1)) if name=='BeachMask' else float(np.clip((h-13)/8,0,1))
            ca.data[li].color=(f,f,f,1)
m=bpy.data.materials.new('art05_terrain_bake');m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');l.new(em.outputs[0],out.inputs['Surface'])
geo=n.new('ShaderNodeNewGeometry');scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=.075;l.new(geo.outputs['Position'],scale.inputs[0])
fract=n.new('ShaderNodeVectorMath');fract.operation='FRACTION';l.new(scale.outputs[0],fract.inputs[0])
shrink=n.new('ShaderNodeVectorMath');shrink.operation='SCALE';shrink.inputs[3].default_value=.482;l.new(fract.outputs[0],shrink.inputs[0])
offset=n.new('ShaderNodeVectorMath');offset.operation='ADD';offset.inputs[1].default_value=(.509,.009,0);l.new(shrink.outputs[0],offset.inputs[0])
image=n.new('ShaderNodeTexImage');image.image=atlas;l.new(offset.outputs[0],image.inputs['Vector'])
green=n.new('ShaderNodeMixRGB');green.blend_type='MULTIPLY';green.inputs[0].default_value=1;green.inputs[2].default_value=(.57,.72,.41,1);l.new(image.outputs['Color'],green.inputs[1])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.43;noise.inputs['Detail'].default_value=3;l.new(geo.outputs['Position'],noise.inputs['Vector'])
sand=n.new('ShaderNodeMixRGB');sand.inputs[1].default_value=(.56,.48,.32,1);sand.inputs[2].default_value=(.72,.64,.48,1);l.new(noise.outputs['Fac'],sand.inputs[0])
beach=n.new('ShaderNodeVertexColor');beach.layer_name='BeachMask'
mix=n.new('ShaderNodeMixRGB');l.new(beach.outputs['Color'],mix.inputs[0]);l.new(sand.outputs[0],mix.inputs[1]);l.new(green.outputs[0],mix.inputs[2])
rock=n.new('ShaderNodeVertexColor');rock.layer_name='RockMask'
rockmix=n.new('ShaderNodeMixRGB');l.new(rock.outputs['Color'],rockmix.inputs[0]);l.new(mix.outputs[0],rockmix.inputs[1]);rockmix.inputs[2].default_value=(.27,.25,.20,1)
l.new(rockmix.outputs[0],em.inputs['Color']);data.materials.clear();data.materials.append(m)
baked=bpy.data.images.new('art05_terrain_color',width=2048,height=2048,alpha=False)
imageout=n.new('ShaderNodeTexImage');imageout.image=baked;n.active=imageout
bpy.context.scene.render.engine='CYCLES';bpy.context.scene.cycles.samples=1
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.ops.object.bake(type='EMIT',margin=8)
baked.filepath_raw=str(OUT/'textures/art05/terrain_color.png');baked.file_format='PNG';baked.save();textures['art05_terrain_color']=baked
material=M['ground'].copy();material.name='art05_baked_terrain_PBR'
if 'atlas_region' in material:del material['atlas_region']
p=material.node_tree.nodes.get('Principled BSDF');t=material.node_tree.nodes.new('ShaderNodeTexImage');t.image=baked
uvnode=material.node_tree.nodes.new('ShaderNodeUVMap');uvnode.uv_map='TerrainUV';material.node_tree.links.new(uvnode.outputs['UV'],t.inputs['Vector']);material.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color'])
data.materials.clear();data.materials.append(material)
while data.color_attributes:data.color_attributes.remove(data.color_attributes[0])
# Native bake is now the color authority; exporter must not multiply a height mask into it.
