"""Self-created visual kit. Run with Blender --background --python <this file>.
Coordinates in helpers use runtime (x, height, forward); mapped to Blender (x,-forward,height).
Every exported module has editable objects and materials in its own .blend.
"""
import bpy, math, json
import numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'public/assets'
SRC=ROOT/'assets-source/blender'
RNG=np.random.default_rng(1701)
manifest={'assets':{},'havana':[]}

def tex(name,base,kind):
    n=1024;y,x=np.mgrid[0:n,0:n];noise=RNG.normal(0,.025,(n,n))
    if kind=='wood':
        noise+=.04*np.sin(x*.12+np.sin(y*.024)*2)+.022*np.sin(x*.61+y*.008)
        noise-=((x%128)<3)*.17
        noise-=((y%512)<2)*.09
    if kind=='cloth':noise+=.018*np.sin(x*math.pi)+.018*np.cos(y*math.pi)
    pixels=np.ones((n,n,4),dtype=np.float32)
    for i,c in enumerate(base):pixels[:,:,i]=np.clip(c+noise,0,1)
    image=bpy.data.images.new(name,width=n,height=n,alpha=True)
    image.pixels.foreach_set(pixels.ravel());image.filepath_raw=str(OUT/f'textures/{name}.png');image.file_format='PNG';image.save()
    return image
textures={'wood':tex('timber',(0.42,.26,.13),'wood'),'cloth':tex('sail_canvas',(.88,.83,.70),'cloth'),'wall':tex('lime_plaster',(.82,.77,.63),'wall')}

def mat(name,color,rough=.75,metal=0,texture=None):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    if texture:
        t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=textures[texture];m.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color'])
    return m
M={ 'wood':mat('timber_PBR',(.42,.26,.13),texture='wood'),'dark':mat('dark_oak',(.15,.085,.039)), 'deck':mat('sunlit_deck',(.53,.37,.19)), 'cloth':mat('ivory_canvas_PBR',(.88,.83,.70),texture='cloth'), 'iron':mat('aged_iron',(.12,.15,.14),.5,.65),'brass':mat('aged_brass',(.48,.31,.12),.4,.65),'wall':mat('lime_plaster_PBR',(.82,.77,.63),texture='wall'),'ochre':mat('ochre_plaster',(.64,.43,.23)),'roof':mat('terracotta',(.47,.16,.075)), 'rooflight':mat('sunlit_terracotta',(.62,.25,.12)), 'stone':mat('warm_limestone',(.37,.39,.30)), 'sand':mat('warm_sand',(.73,.65,.44)), 'grass':mat('tropical_grass',(.28,.37,.13)), 'leaf':mat('palm_leaf',(.13,.30,.07)), 'leaflight':mat('sunlit_leaf',(.29,.42,.10)), 'waterblue':mat('paint_navy',(.045,.15,.20)), 'glass':mat('dark_window',(.045,.075,.065),.4)}

def coord(p):return (p[0],-p[2],p[1])
def reset(name):
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
    bpy.context.collection.name=name

def mesh(name,verts,faces,material):
    d=bpy.data.meshes.new(name);d.from_pydata([coord(p) for p in verts],[],faces);d.update()
    o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.data.materials.append(M[material]);return o

def cube(name,p,size,material,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=coord(p));o=bpy.context.object;o.name=name;o.scale=(size[0],size[2],size[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(M[material])
    if bevel:
        b=o.modifiers.new('edge_softness','BEVEL');b.width=bevel;b.segments=2
        o.modifiers.new('weighted_normals','WEIGHTED_NORMAL')
    return o

def rod(name,a,b,r,material,vertices=10):
    av,bv=Vector(coord(a)),Vector(coord(b));v=bv-av
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=v.length,location=(av+bv)/2)
    o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(M[material]);return o

def line(name,points,r,material):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=1;c.bevel_depth=r;c.bevel_resolution=1
    spline=c.splines.new('POLY');spline.points.add(len(points)-1)
    for p,q in zip(spline.points,points):p.co=(*coord(q),1)
    o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(M[material]);return o

def sphere(name,p,scale,material,segments=16,rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,radius=1,location=coord(p));o=bpy.context.object;o.name=name;o.scale=(scale[0],scale[2],scale[1]);o.data.materials.append(M[material]);
    for poly in o.data.polygons:poly.use_smooth=True
    return o

def finish(name,category):
    # Convert bevels/curves and group by material: reusable meshes suitable for GPU instances.
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.convert(target='MESH')
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH':
            bpy.context.view_layer.objects.active=o;o.select_set(True)
            bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.uv.smart_project(island_margin=.015);bpy.ops.object.mode_set(mode='OBJECT')
    # Keep objects individually editable in .blend. Exporter shares identical materials.
    source=SRC/category/f'{name}.blend';source.parent.mkdir(parents=True,exist_ok=True)
    for image in textures.values():
        image.pack()
    bpy.ops.wm.save_as_mainfile(filepath=str(source))
    url=OUT/'models'/category/f'{name}.glb';url.parent.mkdir(parents=True,exist_ok=True)
    # Join by material only for runtime output to reduce draw calls.
    groups={}
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH':groups.setdefault(o.data.materials[0].name,[]).append(o)
    for group in groups.values():
        bpy.ops.object.select_all(action='DESELECT')
        for o in group:o.select_set(True)
        bpy.context.view_layer.objects.active=group[0]
        if len(group)>1:bpy.ops.object.join()
    tris=0;mins=[1e9]*3;maxs=[-1e9]*3
    for o in bpy.context.scene.objects:
        if o.type=='MESH':
            o.data.calc_loop_triangles();tris+=len(o.data.loop_triangles)
            for v in o.data.vertices:
                p=o.matrix_world@v.co;runtime=(p.x,p.z,-p.y)
                for i,n in enumerate(runtime):mins[i]=min(mins[i],n);maxs[i]=max(maxs[i],n)
    bpy.ops.export_scene.gltf(filepath=str(url),export_format='GLB',export_yup=True)
    all_materials=sorted({m.name for o in bpy.context.scene.objects if o.type=='MESH' for m in o.data.materials})
    manifest['assets'][name]={'url':'/assets/models/'+category+'/'+name+'.glb','source':str(source.relative_to(ROOT)),'triangles':tris,'materials':all_materials,'bounds':{'min':mins,'max':maxs},'lod':'LOD0 only','author':'Self-created'}

# Ships: a shaped 24m coastal sloop with gaff mainsail and jib.
reset('ship_sloop')
zs=[-11,-9,-6,-3,0,3,6,9,12];widths=[1.7,2.8,3.2,3.35,3.35,3.1,2.6,1.7,.06]
verts=[]
for z,w in zip(zs,widths):
    for k in range(13):
        a=math.pi*k/12;verts.append((-w*math.cos(a),2-4*math.sin(a),z))
faces=[]
for j in range(len(zs)-1):
    for k in range(12):a=j*13+k;faces.append((a,a+1,a+14,a+13))
faces.extend([tuple(range(12,-1,-1)),tuple(range(104,117))]);mesh('carvel_hull',verts,faces,'wood')
# Continuous capped deck following real hull outline.
outline=[(-w,1.72,z) for w,z in zip(widths,zs)]+[(w,1.72,z) for w,z in zip(reversed(widths),reversed(zs))]
mesh('fitted_deck',outline,[tuple(range(len(outline)))],'deck')
for z in np.arange(-10.5,11.5,.5):
    w=float(np.interp(z,zs,widths));cube('deck_plank',(0,1.77,float(z)),(max(.1,w*2-.25),.06,.47),'deck')
for side in [-1,1]:
    for h in [1.1,2.05,2.65]:line('hull_strake',[(side*w,h,z) for w,z in zip(widths,zs)],.09,'dark' if h<2 else 'deck')
    for z in range(-10,11,2):
        w=float(np.interp(z,zs,widths));rod('stanchion',(side*w,1.9,z),(side*w,2.65,z),.075,'dark',8)
    for z in [-6,-2,2,6]:cube('gunport_trim',(side*(float(np.interp(z,zs,widths))+.035),.9,z),(.12,.55,.7),'iron',.03)
cube('quarterdeck',(0,2.4,-8),(5,.24,4),'deck',.1);cube('stern_cabin',(0,2.3,-8.5),(3.3,1.6,2.8),'waterblue',.12)
for x in [-1,0,1]:cube('stern_window',(x,2.7,-9.93),(.55,.55,.05),'glass')
rod('mainmast',(0,-.5,.4),(0,22,.1),.23,'wood',16)
rod('bowsprit',(0,2,10),(0,3.2,16),.13,'wood')
rod('boom',(0,5,.1),(0,5,-9.3),.10,'wood')
rod('gaff',(0,17,.1),(0,20,-7.5),.105,'wood')
# Curved cloth grids, deliberate belly in x.
def sail(name,corners,nu,nv):
    vs=[];fs=[]
    for j in range(nv+1):
        t=j/nv
        for i in range(nu+1):
            s=i/nu;a=np.array(corners[0])*(1-s)+np.array(corners[1])*s;b=np.array(corners[3])*(1-s)+np.array(corners[2])*s;p=a*(1-t)+b*t;p[0]+=.65*math.sin(math.pi*s)*math.sin(math.pi*t);vs.append(tuple(p))
    for j in range(nv):
        for i in range(nu):a=j*(nu+1)+i;fs.append((a,a+1,a+nu+2,a+nu+1))
    o=mesh(name,vs,fs,'cloth');sol=o.modifiers.new('cloth_thickness','SOLIDIFY');sol.thickness=.018
    for p in o.data.polygons:p.use_smooth=True
sail('gaff_mainsail',[(.06,5.3,-.25),(.06,5.3,-9),(.06,19.7,-7.35),(.06,16.8,-.25)],14,20)
sail('triangular_jib',[(.08,4.4,1),(.08,3.5,14.9),(.08,20.4,.5),(.08,20.4,.45)],12,16)
for z in [-1,-3,-5,-7]:line('canvas_seam',[(.08,5.35,z),(.6,11,z*.93),(.08,17-z*.35,z*.8)],.018,'sand')
for side in [-1,1]:
    for z in [-5,0,4]:line('standing_rigging',[(side*3,2.6,z),(0,21,.2)],.035,'dark')
line('forestay',[(0,22,.1),(0,3.2,16)],.035,'dark');line('backstay',[(0,22,.1),(0,3,-10)],.035,'dark')
rod('rudder',(0,-1.4,-11),(0,2,-11.5),.25,'dark');cube('rudder_blade',(0,-.7,-11.5),(.24,2,1),'dark')
rod('helm_post',(0,2.6,-7),(0,3.6,-7),.14,'wood')
line('helm_wheel',[(.65*math.cos(a),3.4+.65*math.sin(a),-7) for a in np.linspace(0,2*math.pi,25)],.06,'wood')
for a in np.linspace(0,2*math.pi,8,endpoint=False):rod('helm_spoke',(0,3.4,-7),(.8*math.cos(a),3.4+.8*math.sin(a),-7),.045,'brass')
finish('sloop','ships')

# Modular colonial architecture, each with ground-center pivot.
def house(name,w,d,h,variant='wall',two=False):
    reset(name);cube('stone_footing',(0,.25,0),(w+.5,.5,d+.5),'stone',.1);cube('lime_walls',(0,h/2+.4,0),(w,h,d),variant,.1)
    y=h+.4;rise=2.2
    mesh('pitched_roof',[(-w/2-.6,y,-d/2-.6),(w/2+.6,y,-d/2-.6),(w/2+.6,y,d/2+.6),(-w/2-.6,y,d/2+.6),(0,y+rise,-d/2-.6),(0,y+rise,d/2+.6)],[(0,1,4),(3,5,2),(0,4,5,3),(4,1,2,5)],'roof')
    # Visible tile ridges, column rhythm, doors, shutters, balconies.
    for side in [-1,1]:
        for z in np.arange(-d/2-.5,d/2+.5,.55):line('tile_ridge',[(side*(w/2+.6),y+.06,float(z)),(0,y+rise+.06,float(z))],.08,'rooflight')
    for x in np.arange(-w/2+1,w/2,2):
        for wy in ([2,h-1.25] if two else [h*.57]):
            cube('window_inset',(float(x),wy,-d/2-.045),(.8,1.1,.09),'glass');cube('wood_shutter',(float(x)-.57,wy,-d/2-.14),(.25,1.2,.16),'waterblue')
            cube('window_sill',(float(x),wy-.65,-d/2-.18),(1.25,.15,.4),'stone')
    cube('door_frame',(0,1.5,-d/2-.1),(1.45,2.4,.2),'stone');cube('door',(0,1.45,-d/2-.22),(1.1,2.1,.08),'dark')
    if two:
        cube('balcony',(0,h*.52,-d/2-.95),(w-.8,.18,1.8),'wood')
        for x in np.arange(-w/2+.4,w/2-.2,.65):rod('baluster',(float(x),h*.52,-d/2-1.65),(float(x),h*.52+1,-d/2-1.65),.04,'wood',6)
        cube('balcony_rail',(0,h*.52+1,-d/2-1.65),(w-.6,.1,.1),'wood')
    finish(name,'buildings')
house('building_house_a',7,7,5)
house('building_house_b',8,8,8,'ochre',True)
house('building_warehouse',14,10,6)
house('building_governor',13,11,9,'wall',True)
reset('building_church');cube('church_base',(0,.25,0),(11,.5,16),'stone',.1);cube('nave',(0,4.5,0),(10,8,15),'wall',.12)
mesh('church_roof',[(-5.6,8.5,-8),(5.6,8.5,-8),(5.6,8.5,8),(-5.6,8.5,8),(0,12,-8),(0,12,8)],[(0,1,4),(3,5,2),(0,4,5,3),(4,1,2,5)],'roof')
cube('bell_tower',(-4,8,-6),(4,16,4),'ochre',.12)
for z in [-8.05,-3.95]:cube('bell_arch',(-4,13,z),(1.8,2.4,.12),'glass')
rod('bell',(-4,13,-6),(-4,12.5,-6),.55,'brass',16)
mesh('tower_cap',[(-6.5,16,-8.5),(-1.5,16,-8.5),(-1.5,16,-3.5),(-6.5,16,-3.5),(-4,19,-6)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],'roof')
cube('church_portal',(0,2.6,-7.55),(2.5,4.4,.2),'dark');rod('cross_v',(0,12,-8),(0,14.5,-8),.1,'stone');rod('cross_h',(-.8,13.6,-8),(.8,13.6,-8),.1,'stone');finish('building_church','buildings')
reset('port_lighthouse')
for y,r in [(.4,3),(1,2.4),(5,1.9),(9,1.5)]:rod('tower',(0,max(0,y-3),0),(0,y+1,0),r,'wall',16)
rod('gallery',(0,10,0),(0,10.4,0),2.3,'stone',16);rod('lantern',(0,10.5,0),(0,12.5,0),1.15,'glass',12)
for a in np.linspace(0,2*math.pi,8,endpoint=False):rod('gallery_post',(2*math.cos(a),10.4,2*math.sin(a)),(2*math.cos(a),11.3,2*math.sin(a)),.05,'iron')
rod('cap',(0,12.5,0),(0,13,0),1.5,'roof',12);finish('port_lighthouse','ports')
reset('port_pier')
for x in [-3.4,3.4]:
    for z in [-10,-5,0,5,10]:rod('timber_pile',(x,-3,z),(x,2.3,z),.24,'wood',10)
for z in np.arange(-11,11,.55):cube('pier_plank',(0,1.35,float(z)),(8,.3,.51),'wood',.025)
for x in [-3,3]:cube('bearer',(x,.95,0),(.3,.5,23),'dark')
finish('port_pier','ports')
reset('prop_barrel')
vs=[]
for y,r in [(0,.45),(.1,.52),(.65,.6),(1.2,.52),(1.3,.45)]:
    for a in np.linspace(0,2*math.pi,16,endpoint=False):vs.append((r*math.cos(a),y,r*math.sin(a)))
fs=[]
for j in range(4):
    for i in range(16):a=j*16+i;b=j*16+(i+1)%16;fs.append((a,b,b+16,a+16))
fs.extend([tuple(range(15,-1,-1)),tuple(range(64,80))]);mesh('staves',vs,fs,'wood')
for y in [.15,.45,.95,1.18]:line('iron_hoop',[(.56*math.cos(a),y,.56*math.sin(a)) for a in np.linspace(0,2*math.pi,33)],.035,'iron')
finish('prop_barrel','props')
reset('prop_crate');cube('crate',(0,.65,0),(1.3,1.3,1.3),'wood',.04)
for x in [-.5,.5]:
    for z in [-.68,.68]:cube('crate_brace',(x,.65,z),(.13,1.4,.08),'deck')
finish('prop_crate','props')
reset('prop_skiff');sphere('skiff_hull',(0,.4,0),(1.05,.65,3),'wood');cube('skiff_interior',(0,.8,0),(1.35,.2,4.6),'dark')
for z in [-1.5,0,1.5]:cube('thwart',(0,1,z),(1.6,.12,.35),'deck')
rod('oar',(-.7,1,-1),(1.8,1,2.5),.055,'wood');finish('prop_skiff','props')
reset('prop_palm');line('curved_trunk',[(0,0,0),(.2,3,0),(.6,6,.1),(1,9,.3)],.24,'wood')
for i in range(10):
    a=i*math.tau/10;points=[]
    for j in range(9):
        t=j/8;points.append((1+math.cos(a)*6*t,9+math.sin(t*math.pi)*1.5-t*2,.3+math.sin(a)*6*t))
    vs=[]
    for j,p in enumerate(points):
        w=.75*math.sin(math.pi*j/8);vs.extend([(p[0]-math.sin(a)*w,p[1],p[2]+math.cos(a)*w),(p[0],p[1]+.12,p[2]),(p[0]+math.sin(a)*w,p[1],p[2]-math.cos(a)*w)])
    fs=[]
    for j in range(8):a0=j*3;fs.extend([(a0,a0+3,a0+4,a0+1),(a0+1,a0+4,a0+5,a0+2)])
    mesh('palm_frond',vs,fs,'leaf' if i%2 else 'leaflight')
finish('prop_palm','environment')
reset('prop_tropical_tree');rod('trunk',(0,0,0),(0,7,0),.35,'wood')
for x,y,z in [(-2,6,0),(2,6,1),(0,8,0),(0,6,-2)]:sphere('canopy',(x,y,z),(3,2.5,3),'leaflight' if x else 'leaf',12,8)
finish('prop_tropical_tree','environment')
reset('prop_bush')
for x,y,z in [(-.7,.7,0),(.7,.8,.2),(0,1.3,0)]:sphere('bush',(x,y,z),(1.2,1,1.1),'leaf',12,6)
finish('prop_bush','environment')

# Island: metric mesh, 4 terrain layers, irregular coast and raised interior.
def terrain_height(x,z):
    dx=(x+40)/70;dz=(z-64)/50;r=math.sqrt(dx*dx+dz*dz)
    r+=.025*math.sin(x*.12)*math.sin(z*.14)
    if r>1.12:return -3
    coast=max(-3,min(3.1,(1-r)*28))
    hills=31*math.exp(-((x+68)/22)**2-((z-86)/20)**2)+10*math.exp(-((x+10)/18)**2-((z-93)/18)**2)
    height=coast+max(0,1-r)*hills*2
    # Flat town terrace, blended into irregular beach and highlands.
    edge=min(x+94,20-x,z-27,75-z)
    blend=max(0,min(1,edge/5))
    return height*(1-blend)+3.1*blend
reset('island_visual_test');vs=[];fs=[];cols=[]
for j,z in enumerate(np.linspace(7,122,70)):
    for i,x in enumerate(np.linspace(-120,42,96)):
        h=terrain_height(float(x),float(z));vs.append((float(x),h,float(z)));cols.append(h)
for j in range(69):
    for i in range(95):a=j*96+i;fs.extend([(a,a+96,a+1),(a+1,a+96,a+97)])
o=mesh('layered_terrain',vs,fs,'sand')
terrain_mat=mat('terrain_vertex_PBR',(1,1,1),.95)
color_node=terrain_mat.node_tree.nodes.new('ShaderNodeVertexColor');color_node.layer_name='TerrainColor'
terrain_mat.node_tree.links.new(color_node.outputs['Color'],terrain_mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
o.data.materials.clear();o.data.materials.append(terrain_mat)
colors=o.data.color_attributes.new(name='TerrainColor',type='FLOAT_COLOR',domain='CORNER')
for poly in o.data.polygons:
    poly.use_smooth=True
    for loop_i in poly.loop_indices:
        vi=o.data.loops[loop_i].vertex_index;h=cols[vi];x,y,z=vs[vi]
        grass=max(0,min(1,(h-1.8)/1.5));rock=max(0,min(1,(h-16)/9))
        base=np.array((.67,.59,.39))*(1-grass)+np.array((.21,.31,.085))*grass
        base=base*(1-rock)+np.array((.34,.36,.27))*rock
        grain=.95+.05*math.sin(x*.63)*math.cos(z*.49)
        colors.data[loop_i].color=(*list(base*grain),1)
finish('island_visual_test','environment')
# Declarative placement is renderer data, not a city simulation.
def place(asset,x,z,heading=0,shadow=True,y=None):
    manifest['havana'].append({'asset':asset,'x':x,'y':terrain_height(x,z) if y is None else y,'z':z,'heading':heading,'shadow':shadow})
place('port_pier',-12,15,y=0);place('port_pier',-31,15,y=0)
place('building_warehouse',-9,37);place('building_warehouse',-30,35)
place('building_governor',-35,58);place('building_church',-62,59)
for asset,x,z in [('building_house_a',-49,35),('building_house_b',-65,36),('building_house_a',-81,45),('building_house_b',-11,57),('building_house_a',8,49),('building_house_a',-78,65)]:place(asset,x,z)
place('port_lighthouse',-83,34)
for x,z in [(-90,60),(-81,78),(-55,78),(-45,78),(-18,77),(-3,69),(10,60),(-46,25),(-28,24),(-5,24),(9,37)]:place('prop_palm',x,z,shadow=False)
for x,z in [(-93,70),(-70,90),(-58,95),(-38,91),(-25,94),(-6,87),(-82,86),(-45,96)]:place('prop_tropical_tree',x,z,shadow=False)
for i in range(30):
    x=float(RNG.uniform(-90,15));z=float(RNG.uniform(55,106))
    if terrain_height(x,z)>3:place('prop_bush',x,z,shadow=False)
for i in range(12):place('prop_barrel' if i%2 else 'prop_crate',-32+i*2,28,shadow=False)
place('prop_skiff',9,10,heading=.3,shadow=False,y=0);place('prop_skiff',-27,11,heading=-.2,shadow=False,y=0)
manifest['textures']=['/assets/textures/timber.png','/assets/textures/sail_canvas.png','/assets/textures/lime_plaster.png']
(SRC/'visual/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('VISUAL_ASSET_REPORT',json.dumps({k:v['triangles'] for k,v in manifest['assets'].items()}))
