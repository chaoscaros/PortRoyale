"""Task05 atlas assignment and metric UV authoring, executed in Blender recipe scope.
The image is untouched: UV islands select an atlas quadrant. Geometry normals and
procedural micro-normal/roughness remain separate from generated albedo artwork.
"""
atlas=bpy.data.images.load(str(OUT/'textures/art05/surface_atlas.png'),check_existing=True)
textures['art05_surface_atlas']=atlas
for key,region in [('wall',(0,.5)),('wood',(.5,.5)),('deck',(.5,.5)),('stone',(0,0)),('ground',(.5,0))]:
    m=M[key];m.name='art05_'+key+'_atlas_PBR';m['atlas_region']=region
    p=m.node_tree.nodes.get('Principled BSDF');link=p.inputs['Base Color'].links[0];texnode=link.from_node;texnode.image=atlas
    uvnode=m.node_tree.nodes.new('ShaderNodeUVMap');uvnode.uv_map='AtlasUV';m.node_tree.links.new(uvnode.outputs['UV'],texnode.inputs['Vector'])
M['sand']=surface('art05_sand',(.66,.59,.44),'ground')
M['rock']=surface('art05_rock',(.32,.31,.27),'ground')
M['leaf']=mat('art05_leaf_shade',(.035,.095,.018),.83)
M['leaflight']=mat('art05_leaf_sun',(.11,.22,.035),.76)
M['ochre']=M['wall'].copy();M['ochre'].name='art05_ochre_stucco_PBR';M['ochre']['atlas_region']=(0,.5)

def prepare_surfaces():
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        data=ob.data
        if 'TerrainUV' in data.uv_layers:continue
        metric=data.uv_layers.active or data.uv_layers.new(name='MetricUV');metric.name='MetricUV'
        auv=data.uv_layers.get('AtlasUV') or data.uv_layers.new(name='AtlasUV')
        metric=data.uv_layers['MetricUV'];auv=data.uv_layers['AtlasUV']
        # Use physical-scale planar charts instead of packing the whole scene into one UV tile.
        for p in data.polygons:
            normal=p.normal;axis=max(range(3),key=lambda k:abs(normal[k]));axes=[k for k in range(3) if k!=axis]
            pts=[data.vertices[data.loops[li].vertex_index].co for li in p.loop_indices]
            mins=[min(v[k] for v in pts) for k in axes];spans=[max(v[k] for v in pts)-mn for k,mn in zip(axes,mins)]
            material=data.materials[p.material_index];region=material.get('atlas_region') if material else None
            for li,pt in zip(p.loop_indices,pts):
                metric.data[li].uv=(pt[axes[0]]/4,pt[axes[1]]/4)
                if region:
                    u=(pt[axes[0]]-mins[0])/max(spans[0],4);v=(pt[axes[1]]-mins[1])/max(spans[1],4)
                    auv.data[li].uv=(region[0]+.008+u*.484,region[1]+.008+v*.484)
        # Discrete authored color variation supports reused modules without extra materials.
        if not data.color_attributes:
            ca=data.color_attributes.new(name='SurfaceTint',type='FLOAT_COLOR',domain='CORNER')
            seed=sum(ord(c) for c in ob.name);factor=.88+(seed%17)*.007
            if 'stucco' in ob.name: tint=[(1,.94,.80),(.86,.91,.82),(.91,.83,.68)][seed%3]
            else:tint=(factor,factor,factor)
            for p in data.polygons:
                t=tint
                if 'roof_tiles' in ob.name:
                    f=.72+((p.index//4*37)%31)/100;t=(f,min(1,f*.93),min(1,f*.85))
                for li in p.loop_indices:ca.data[li].color=(*t,1)
        data.uv_layers.active_index=0

finish_source=base[base.index('def finish('):].replace('bpy.ops.uv.smart_project(island_margin=.015);','')
finish_source=finish_source.replace("bpy.ops.object.mode_set(mode='OBJECT')","bpy.ops.object.mode_set(mode='OBJECT');prepare_surfaces()")
finish_source=finish_source.replace("export_yup=True)","export_yup=True,export_vertex_color='ACTIVE')")
finish_source=finish_source.replace('bpy.ops.wm.save_as_mainfile(filepath=str(source))','bpy.data.libraries.write(str(source), {bpy.context.scene}, fake_user=True, compress=True)')
exec(finish_source)
