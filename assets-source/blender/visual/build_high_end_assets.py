"""Task05 High-End Art Pass. Blender 4.5; metric source -> Y-up GLB.
Reuse only low-level authoring helpers, not the previous low-detail assets.
"""
from pathlib import Path
base=Path(__file__).with_name('build_visual_assets.py').read_text().split('# Ships:')[0]
base=base.replace('b.segments=2','b.segments=1')
exec(base)
# Authored tileable PBR surfaces: base color, tangent normal and roughness.
textures={}
def surface(key,base,kind):
    n=1024;yy,xx=np.mgrid[0:n,0:n];u=xx/n;v=yy/n
    fine=RNG.normal(0,.007,(n,n));broad=np.sin(u*math.tau*7+np.sin(v*math.tau*3))*.018+np.sin(v*math.tau*11)*.009
    height=broad+fine
    if kind=='wood': height+=.018*np.sin(u*math.tau*75+np.sin(v*math.tau*2)*4)+.01*np.sin(u*math.tau*130);height-=((xx%128)<3)*.12
    if kind=='stone':
        course=yy//128;seam=((yy%128)<7)|(((xx+(course%2)*64)%256)<6);height-=seam*.11;height+=((xx//256+course*3)%5)*.007
    if kind=='cloth':height+=.009*np.cos(xx*math.pi*.5)+.009*np.cos(yy*math.pi*.5)
    if kind=='tile':height+=.035*np.cos(u*math.tau*8);height-=((yy%128)<4)*.04
    if kind=='ground':height+=np.sin(u*math.tau*37+v*11)*.013
    def save(suffix,rgb,space='sRGB'):
        rgba=np.ones((n,n,4),np.float32);rgba[:,:,:3]=rgb
        im=bpy.data.images.new(key+suffix,width=n,height=n,alpha=False);im.colorspace_settings.name=space;im.pixels.foreach_set(rgba.ravel());im.filepath_raw=str(OUT/f'textures/{key}{suffix}.png');im.file_format='PNG';im.save();textures[key+suffix]=im;return im
    color=np.clip(np.array(base)[None,None,:]+height[:,:,None],.01,.98)
    albedo=save('_color',color)
    gy,gx=np.gradient(height);normal=np.stack((-gx*9,-gy*9,np.ones_like(gx)),axis=-1);normal/=np.linalg.norm(normal,axis=-1)[:,:,None]
    normalim=save('_normal',normal*.5+.5,'Non-Color')
    rough=np.clip(.78+height*1.5,.35,.98);roughim=save('_roughness',np.repeat(rough[:,:,None],3,axis=-1),'Non-Color')
    material=bpy.data.materials.new(key+'_PBR');material.use_nodes=True;nodes=material.node_tree.nodes;links=material.node_tree.links;p=nodes.get('Principled BSDF')
    for im,socket in [(albedo,'Base Color'),(roughim,'Roughness')]:
        t=nodes.new('ShaderNodeTexImage');t.image=im;links.new(t.outputs['Color'],p.inputs[socket])
    t=nodes.new('ShaderNodeTexImage');t.image=normalim;norm=nodes.new('ShaderNodeNormalMap');norm.inputs['Strength'].default_value=.45;links.new(t.outputs['Color'],norm.inputs['Color']);links.new(norm.outputs['Normal'],p.inputs['Normal'])
    return material
for key,color,kind in [('wood',(.30,.205,.115),'wood'),('deck',(.52,.40,.25),'wood'),('wall',(.77,.70,.55),'wall'),('roof',(.43,.205,.12),'tile'),('stone',(.46,.44,.36),'stone'),('cloth',(.84,.80,.68),'cloth'),('ground',(.37,.40,.24),'ground')]:M[key]=surface('hero_'+key,color,kind)
M['ochre']=mat('ochre_limewash',(.55,.39,.23));M['leaf']=mat('leaf_deep',(.075,.18,.045));M['leaflight']=mat('leaf_sun',(.19,.30,.085));M['rope']=mat('hemp_rope',(.28,.22,.14));M['glass']=mat('recessed_glazing',(.06,.115,.12),.2,.25)
# Save compressed sources, retain independently editable parts, export by material.
oldfinish=finish
exec(base[base.index('def finish('):].replace('bpy.ops.wm.save_as_mainfile(filepath=str(source))','bpy.data.libraries.write(str(source), {bpy.context.scene}, fake_user=True, compress=True)'))

exec(Path(__file__).with_name('art05_surfaces.py').read_text())

def arch(name,x,y,z,w,h,material='stone',depth=.3):
    # Solid masonry voussoir arch with open center; vertical jambs.
    r=w/2;cy=y+h-r
    cube(name+'_jamb',(x-r-.16,y+(h-r)/2,z),(.3,h-r,depth),material,.025)
    cube(name+'_jamb',(x+r+.16,y+(h-r)/2,z),(.3,h-r,depth),material,.025)
    vs=[];fs=[]
    for k in range(17):
        a=math.pi*k/16
        for dz in [-depth/2,depth/2]:
            for rr in [r,r+.32]:vs.append((x+rr*math.cos(a),cy+rr*math.sin(a),z+dz))
    for k in range(16):
        a=k*4;fs.extend([(a,a+4,a+5,a+1),(a+2,a+3,a+7,a+6),(a+1,a+5,a+7,a+3),(a,a+2,a+6,a+4)])
    mesh(name,vs,fs,material)

def window(x,y,z,arched=False):
    cube('window_recess',(x,y,z),(.95,1.7,.14),'glass',.04)
    for dx in [-.6,.6]:cube('moulded_frame',(x+dx,y,z-.09),(.14,2,.22),'stone',.025)
    for dy in [-.95,.95]:cube('window_lintel',(x,y+dy,z-.09),(1.4,.18,.3),'stone',.035)
    cube('mullion',(x,y,z-.11),(.065,1.8,.08),'deck')
    cube('transom',(x,y+.15,z-.11),(1.05,.065,.08),'deck')
    if arched:arch('window_arch',x,y-.8,z-.1,1,2)
    for side in [-1,1]:
        cube('shutter',(x+side*.87,y,z),(.4,1.8,.12),'waterblue',.03)
        for dy in np.linspace(-.7,.7,7):cube('shutter_louvre',(x+side*.87,y+dy,z-.08),(.38,.065,.08),'dark')

def tiled_roof(w,d,y,rise):
    vs=[];fs=[]
    # Individual curved barrel tiles, staggered courses, dimensional eaves.
    for side in [-1,1]:
        slope=math.hypot(w/2+.65,rise);courses=max(4,int(slope/.65));cols=int((d+1.2)/.38)
        for row in range(courses):
            for col in range(cols):
                z=-d/2-.6+(col+.5)*.38
                for end in [0,1]:
                    t=(row+end*1.1)/courses
                    for j in range(5):
                        a=math.pi*j/4
                        vs.append((side*((w/2+.65)*t),y+rise*(1-t)+math.sin(a)*.10+.05,z+math.cos(a)*.20))
                a0=len(vs)-10
                for j in range(4):fs.append((a0+j,a0+j+1,a0+j+6,a0+j+5))
    mesh('individual_barrel_roof_tiles',vs,fs,'roof')
    for side in [-1,1]:cube('thick_eave',(side*(w/2+.55),y-.12,0),(.3,.32,d+1.4),'wood',.05)
    rod('ridge_cap',(0,y+rise+.15,-d/2-.65),(0,y+rise+.15,d/2+.65),.21,'roof',16)
    mesh('gable_masonry',[(-w/2,y,-d/2),(w/2,y,-d/2),(0,y+rise,-d/2),(-w/2,y,d/2),(w/2,y,d/2),(0,y+rise,d/2)],[(0,1,2),(3,5,4)],'wall')

def building(name,w,d,h,kind='home'):
    reset(name)
    for k in range(3):cube('stepped_stone_plinth',(0,.17+k*.23,0),(w+.9-k*.2,.24,d+.9-k*.2),'stone',.055)
    cube('stucco_volume',(0,h/2+.7,0),(w,h,d),'wall',.07)
    for y in [.8,4.4,h+.55]:cube('projecting_cornice',(0,y,0),(w+.38,.23,d+.38),'stone',.05)
    for x in [-w/2,w/2]:
        for z in [-d/2,d/2]:
            for y in np.arange(1,h,.65):cube('corner_quoin',(x,float(y),z),(.55,.45,.55),'stone',.035)
    for x in np.arange(-w/2+1.6,w/2-1,2.5):
        for y in [2.4,6.2] if h>7 else [2.7]:window(float(x),y,-d/2-.1,h>8)
        window(float(x),h-1.5,d/2+.1)
    for z in np.arange(-d/2+2,d/2,2.7):
        for side in [-1,1]:
            # Side walls also have substantial openings and stone surrounds.
            cube('side_window',(side*(w/2+.04),h-1.6,float(z)),(.12,1.6,1),'glass',.03)
            cube('side_sill',(side*(w/2+.1),h-2.45,float(z)),(.35,.2,1.3),'stone',.04)
    arch('main_portal',0,.7,-d/2-.3,1.8,3.2)
    cube('carved_double_door',(0,2,-d/2-.12),(1.7,2.6,.12),'wood',.03)
    if kind in ['hall','home']:
        by=4.5 if h>7 else 1.0
        cube('gallery_floor',(0,by,-d/2-1.5),(w+1,.27,2.7),'stone',.06)
        for x in np.arange(-w/2+.4,w/2,.55):rod('turned_balustrade',(float(x),by,-d/2-2.65),(float(x),by+1.05,-d/2-2.65),.055,'wood',10)
        for y in [by+.2,by+1.1]:cube('balcony_handrail',(0,y,-d/2-2.65),(w,.12,.14),'wood',.035)
        for x in np.arange(-w/2+.5,w/2,2.5):
            rod('gallery_column',(float(x),.65,-d/2-2.4),(float(x),by+.05,-d/2-2.4),.2,'stone',16)
            if kind=='hall':arch('arcade',float(x)+1.2,.65,-d/2-2.4,2.1,3.65)
    if kind=='warehouse':
        for x in [-w*.25,w*.25]:
            arch('warehouse_loading_arch',x,.7,-d/2-.35,2.8,4.1)
            cube('loading_door',(x,2.45,-d/2-.16),(2.6,3.5,.15),'wood',.04)
            line('awning_support',[(x-1.5,5,-d/2),(x-1.5,4,-d/2-2),(x+1.5,4,-d/2-2),(x+1.5,5,-d/2)],.08,'dark')
            mesh('loading_canvas',[(x-1.6,5,-d/2),(x+1.6,5,-d/2),(x+1.6,4,-d/2-2),(x-1.6,4,-d/2-2)],[(0,1,2,3)],'cloth')
    tiled_roof(w,d,h+.8,2.7 if kind!='hall' else 3.2)
    cube('chimney',(w*.25,h+2.4,d*.2),(.9,2.2,.9),'stone',.05)
    cube('chimney_cap',(w*.25,h+3.55,d*.2),(1.2,.22,1.2),'stone',.05)
    if kind=='church':
        tx=-w/2+1.2;tz=-d/2+1.2
        cube('bell_tower',(tx,11,tz),(4.7,22,4.7),'wall',.1)
        for y in [1,8,15,19,22]:cube('tower_cornice',(tx,y,tz),(5.2,.35,5.2),'stone',.08)
        for side in [-1,1]:
            arch('belfry_arch',tx,17,tz+side*2.4,2.3,4.4)
            cube('belfry_depth',(tx,19,tz+side*2.37),(2.25,3.7,.12),'glass')
        sphere('bell_dome',(tx,22,tz),(2.5,3,2.5),'roof',32,16)
        rod('cross',(tx,24.4,tz),(tx,27,tz),.09,'brass',12);rod('cross_arm',(tx-.65,26,tz),(tx+.65,26,tz),.09,'brass',12)
    if kind in ['merchant','office']:
        cube('projecting_shop_front',(0,2.7,-d/2-.5),(w-.8,4.1,.8),'ochre',.1)
        for x in np.arange(-w/2+1.5,w/2,2.7):
            window(float(x),2.8,-d/2-1)
            rod('arcade_post',(float(x),.6,-d/2-3),(float(x),4.9,-d/2-3),.14,'wood',12)
        cube('covered_loggia',(0,5,-d/2-2),(w+1,.27,4),'wood',.05)
        mesh('striped_loggia_canopy',[(-w/2,5.7,-d/2),(w/2,5.7,-d/2),(w/2,4.9,-d/2-3),(-w/2,4.9,-d/2-3)],[(0,1,2,3)],'cloth')
        cube('merchant_sign',(w*.2,4,-d/2-3.15),(3,.75,.15),'waterblue',.04)
    for x in [-w/2+.3,w/2-.3]:
        rod('rainwater_downpipe',(x,.8,-d/2-.25),(x,h+.7,-d/2-.25),.055,'iron',12)
    for x in np.arange(-w/2+1.6,w/2-1,2.5):
        cube('flower_box',(float(x),5.1,-d/2-.55),(1.1,.3,.45),'wood',.03)
    finish(name,'buildings')
for args in [('building_house_a',9,9,8,'home'),('building_house_b',11,8,9,'home'),('building_house_c',8,12,6,'home'),('building_warehouse',19,12,7,'warehouse'),('building_warehouse_b',12,15,8,'warehouse'),('building_governor',20,14,10,'hall'),('building_church',13,20,12,'church'),('building_merchant_a',12,10,10,'merchant'),('building_merchant_b',10,13,8,'merchant'),('building_harbor_office',15,12,10,'office')]:building(*args)

# Hero brig, two masts and layered sail plan; waterline centered at origin.
reset('hero_brig')
zs=np.linspace(-15,16,97);widths=4.5*np.maximum(.015,np.sin((zs+17)/34*math.pi))**.45; widths[-1]=.035
vs=[];fs=[];segments=32
for z,w in zip(zs,widths):
    for k in range(segments+1):
        a=math.pi*k/segments;sheer=.6*(abs(z)/16)**2
        vs.append((-float(w)*math.cos(a),2.8+sheer-5.2*math.sin(a),float(z)))
for j in range(96):
    for k in range(segments):a=j*(segments+1)+k;fs.append((a,a+1,a+segments+2,a+segments+1))
fs+=[tuple(range(segments,-1,-1)),tuple(range(96*(segments+1),97*(segments+1)))]
o=mesh('sculpted_carvel_hull',vs,fs,'wood')
for p in o.data.polygons:p.use_smooth=True
outline=[(-float(w),2.65,float(z)) for w,z in zip(widths,zs)]+[(float(w),2.65,float(z)) for w,z in zip(reversed(widths),reversed(zs))]
mesh('deck_outline',outline,[tuple(range(len(outline)))],'deck')
for z in np.arange(-14.7,15.5,.34):
    w=float(np.interp(z,zs,widths));cube('caulked_deck_plank',(0,2.68,float(z)),(w*2-.16,.10,.318),'deck',.009)
for side in [-1,1]:
    for y in [.0,.7,1.4,2.25,2.95,3.65]:line('hull_wales',[(side*float(w),y+.6*(abs(z)/16)**2,float(z)) for w,z in zip(widths,zs)],.085,'dark' if y<2 else 'deck')
    for z in np.arange(-14,15,1.05):
        w=float(np.interp(z,zs,widths));rod('railing_stanchion',(side*w,2.9,z),(side*w,3.7,z),.065,'wood',12)
    for z in [-10,-6,-2,2,6,10]:
        w=float(np.interp(z,zs,widths));cube('framed_hull_port',(side*(w+.03),1.8,z),(.15,.7,1),'brass',.035);cube('port_inner',(side*(w+.12),1.8,z),(.1,.5,.74),'dark',.03)
mesh('tapered_stern_gallery',[(-3.55,2.8,-10),(3.55,2.8,-10),(3.1,2.8,-14.1),(-3.1,2.8,-14.1),(-3.1,5.45,-10.3),(3.1,5.45,-10.3),(2.7,5.45,-14.1),(-2.7,5.45,-14.1)],[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],'waterblue')
for side in [-1,1]:
    for z in np.arange(-13.8,-10,.65):
        cube('quarter_gallery_side_window',(side*3.22,4.5,float(z)),(.12,.85,.42),'glass',.035)
        rod('quarter_gallery_pillar',(side*3.28,3.6,float(z)),(side*2.95,5.3,float(z)),.045,'brass',12)
    line('headrail_scroll',[(side*1.9,3.4,13),(side*1.2,4.0,16),(side*.4,4.5,19)],.09,'brass')
for x in [-2.5,-1.25,0,1.25,2.5]:
    cube('stern_glazing',(x,4.5,-14.1),(.8,1,.09),'glass',.025)
    for dx in [-.5,.5]:cube('stern_gilt_frame',(x+dx,4.5,-14.2),(.08,1.25,.1),'brass',.01)
for y in [3.65,5.2]:cube('stern_moulding',(0,y,-14.2),(7,.11,.15),'brass',.025)
cube('raised_quarterdeck',(0,5.65,-12),(6.2,.2,4.5),'deck',.1)
rod('rudder_stock',(0,-1.5,-15),(0,4,-15),.18,'iron',16);cube('rudder_blade',(0,-.65,-15.5),(.32,3,1.3),'wood',.05)
rod('bowsprit',(0,3,14),(0,5,22),.19,'wood',20)
# Dense curved sails with edge ropes and authentic broad-seam construction.
def sail(name,corners,nu=32,nv=24):
    vs=[];fs=[]
    for j in range(nv+1):
        t=j/nv
        for i in range(nu+1):
            s=i/nu;a=np.array(corners[0])*(1-s)+np.array(corners[1])*s;b=np.array(corners[3])*(1-s)+np.array(corners[2])*s;p=a*(1-t)+b*t;p[2]+=.85*math.sin(math.pi*s)*math.sin(math.pi*t);vs.append(tuple(p))
    for j in range(nv):
        for i in range(nu):a=j*(nu+1)+i;fs.append((a,a+1,a+nu+2,a+nu+1))
    o=mesh(name,vs,fs,'cloth');sol=o.modifiers.new('sewn_edge_thickness','SOLIDIFY');sol.thickness=.025
    for p in o.data.polygons:p.use_smooth=True
    line('sail_bolt_rope',corners+[corners[0]],.035,'rope')
    for i in range(1,12):
        s=i/12;a=np.array(corners[0])*(1-s)+np.array(corners[1])*s;b=np.array(corners[3])*(1-s)+np.array(corners[2])*s
        pts=[]
        for t in np.linspace(0,1,15):p=a*(1-t)+b*t;p[2]+=.87*math.sin(math.pi*s)*math.sin(math.pi*t);pts.append(tuple(p))
        line('canvas_broad_seam',pts,.012,'rope')
for z,height in [(5,28),(-5,31)]:
    rod('lower_mast',(0,1,z),(0,height*.7,z),.31,'wood',24);rod('topmast',(0,height*.63,z),(0,height,z),.16,'wood',20)
    rod('mast_band',(0,height*.63,z),(0,height*.63+.2,z),.38,'iron',20)
    for y,half,span in [(7,6.8,7),(15,5.5,6.5),(23,3.6,4)]:
        if y>height-2:continue
        rod('square_yard',(-half,y+span,z),(half,y+span,z),.12,'wood',20)
        sail('bellying_square_sail',[(-half+.2,y,z),(half-.2,y,z),(half-.6,y+span-.2,z),(-half+.6,y+span-.2,z)])
    for side in [-1,1]:
        for dz in [-2,-.9,.3,1.5]:line('shroud',[(side*4.2,3.5,z+dz),(0,height*.7,z)],.035,'rope')
        for y in np.arange(4,19,.65):
            f=(y-3.5)/(height*.7-3.5);xx=side*4.2*(1-f);line('ratline',[(xx,y,z-2*(1-f)),(xx,y,z+1.5*(1-f))],.018,'rope')
    line('forestay',[(0,height,z),(0,5,22)],.035,'rope')
sail('forward_jib',[(.05,6,7),(.05,5.5,21),(.05,23,5),(.05,23,5)],24,20)
for x in [-2,2]:
    cube('deck_hatch',(x,2.9,-1),(2,.25,3),'dark',.03)
    for z in np.arange(-2.4,.5,.25):cube('hatch_grating',(x,3.08,float(z)),(1.9,.06,.075),'deck')
rod('capstan',(0,2.7,10),(0,3.8,10),.45,'wood',20)
for a in np.linspace(0,math.tau,6,endpoint=False):rod('capstan_handle',(0,3.6,10),(1.4*math.cos(a),3.6,10+1.4*math.sin(a)),.065,'wood',10)
line('anchor_cable',[(1,3,13),(1.8,1.4,14),(2,-.2,13)],.10,'rope')
finish('sloop','ships')

# Piers, seawall, quay and street modules.
reset('port_pier')
for x in [-4,4]:
    for z in np.arange(-14,15,3):
        rod('heavy_pile',(x,-4,z),(x,2.8,z),.35,'wood',16)
        rod('cross_brace',(x,-1,z),(x,1.6,z+2.6),.15,'dark',10)
for z in np.arange(-15,15,.4):cube('weathered_deck_board',(0,1.8,float(z)),(9,.28,.37),'wood',.028)
for x in [-3.5,3.5]:cube('long_bearer',(x,1.25,0),(.35,.65,31),'dark',.04)
for x,z in [(-3,-12),(3,-12),(-3,9),(3,9)]:
    rod('bollard',(x,1.9,z),(x,2.7,z),.22,'iron',16);rod('bollard_horn',(x-.5,2.6,z),(x+.5,2.6,z),.12,'iron',12)
finish('port_pier','ports')
reset('port_lighthouse')
for y,r in [(0,3.8),(.5,3.6),(1,3.3)]:rod('stepped_foundation',(0,y,0),(0,y+.5,0),r,'stone',48)
bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=2.7,radius2=1.75,depth=14,location=coord((0,8,0)));bpy.context.object.data.materials.append(M['wall'])
for y in [2,7,13,15]:rod('stone_belt',(0,y,0),(0,y+.3,0),2.85 if y<7 else 2.3,'stone',48)
rod('lantern_glass',(0,15.3,0),(0,18.3,0),1.5,'glass',32)
for a in np.linspace(0,math.tau,12,endpoint=False):
    rod('lantern_frame',(1.52*math.cos(a),15.3,1.52*math.sin(a)),(1.52*math.cos(a),18.3,1.52*math.sin(a)),.06,'brass',10)
    rod('gallery_railing',(2.2*math.cos(a),15.3,2.2*math.sin(a)),(2.2*math.cos(a),16.2,2.2*math.sin(a)),.04,'iron',10)
line('gallery_ring',[(2.2*math.cos(a),16.2,2.2*math.sin(a)) for a in np.linspace(0,math.tau,65)],.06,'iron')
sphere('copper_roof',(0,18.3,0),(1.8,1.3,1.8),'waterblue',32,16);arch('lighthouse_door',0,1,-2.65,1.1,2.6);finish('port_lighthouse','ports')
reset('prop_stone_wall')
for row in range(4):
    for col in range(10):cube('limestone_block',(-7.5+col*1.5+(row%2)*.2,row*.48+.24,0),(1.47,.46,.95),'stone',.06)
cube('wall_cap',(0,2.05,0),(16,.25,1.25),'stone',.05);finish('prop_stone_wall','props')
reset('port_quay');cube('quay_masonry',(0,1.3,0),(18,2.6,10),'stone',.08)
for x in np.arange(-9,9,1.5):
    for z in np.arange(-5,5,1):cube('quay_paver',(float(x)+.7,2.65,float(z)+.45),(1.44,.13,.92),'stone',.025)
for k in range(5):cube('quay_stair',(0,.25+k*.25,-8+k*.65),(8,.5+k*.5,.68),'stone',.025)
finish('port_quay','ports')
reset('port_street')
for x in np.arange(-4,4,.8):
    for z in np.arange(-10,10,.65):cube('cobblestone',(float(x),.05,float(z)),(.76,.14,.61),'stone',.035)
finish('port_street','ports')
# Preserve smaller useful props from previous kit by regenerating their authored sections.
prop_section=Path(__file__).with_name('build_visual_assets.py').read_text().split("reset('prop_barrel')")[1].split("reset('prop_palm')")[0]
exec("reset('prop_barrel')"+prop_section)
reset('prop_cart');cube('cart_bed',(0,1.1,0),(1.8,.18,3),'wood',.04)
for x in [-.9,.9]:
    for y in [1.4,1.8,2.2]:cube('cart_side',(x,y,0),(.1,.25,3),'wood',.025)
    line('wagon_wheel',[(x*1.3,.75+.7*math.sin(a),.7*math.cos(a)) for a in np.linspace(0,math.tau,33)],.08,'iron')
    for a in np.linspace(0,math.tau,12,endpoint=False):rod('wheel_spoke',(x*1.3,.75,0),(x*1.3,.75+.65*math.sin(a),.65*math.cos(a)),.045,'wood')
    rod('cart_shaft',(x,1,-1.5),(x,.8,-3.6),.09,'wood')
finish('prop_cart','props')
reset('prop_market_awning')
for x in [-2,2]:
    for z in [-1.4,1.4]:rod('market_post',(x,0,z),(x,3.4,z),.075,'wood',12)
mesh('striped_sunshade',[(-2.2,3.1,-1.6),(2.2,3.1,-1.6),(2.2,3.5,0),(-2.2,3.5,0),(-2.2,3.1,1.6),(2.2,3.1,1.6)],[(0,1,2,3),(3,2,5,4)],'cloth')
cube('stall_counter',(0,1,0),(3.8,.18,2),'wood',.04);finish('prop_market_awning','props')
# Leaf geometry instead of spherical canopy. Each blade has a raised midrib.
def foliage_leaf(vs,fs,center,a,length,width,tilt=0):
    x,y,z=center;dx,dz=math.cos(a),math.sin(a);nx,nz=-dz,dx;i=len(vs)
    vs.extend([(x,y,z),(x+dx*length*.45+nx*width,y+tilt+.07,z+dz*length*.45+nz*width),(x+dx*length,y+tilt*.6,z+dz*length),(x+dx*length*.45-nx*width,y+tilt+.07,z+dz*length*.45-nz*width),(x+dx*length*.5,y+tilt+.15,z+dz*length*.5)])
    fs.extend([(i,i+1,i+4),(i+1,i+2,i+4),(i+2,i+3,i+4),(i+3,i,i+4)])
for variant in [0,1]:
    reset('prop_palm');height=12+variant*2;lean=1.8+variant
    line('tapered_curving_trunk',[(lean*(t**1.7),height*t,.35*math.sin(t*2)) for t in np.linspace(0,1,24)],.24,'wood')
    for y in np.arange(.3,height,.28):
        t=y/height;line('trunk_growth_ring',[(lean*t**1.7+.255*math.cos(a),y,.35*math.sin(t*2)+.255*math.sin(a)) for a in np.linspace(0,math.tau,13)],.022,'deck')
    vs=[];fs=[]
    for k in range(15):
        a=k*math.tau/15+variant*.2;length=5+RNG.random()*2
        pts=[]
        for t in np.linspace(0,1,22):pts.append((lean+math.cos(a)*length*t,height+2.1*math.sin(t*3)-2.8*t,.32+math.sin(a)*length*t))
        line('frond_midstem',pts,.035,'leaflight')
        for t in np.linspace(.08,.97,25):
            c=(lean+math.cos(a)*length*t,height+2.1*math.sin(t*3)-2.8*t,.32+math.sin(a)*length*t)
            for side in [-1,1]:foliage_leaf(vs,fs,c,a+side*1.05,1.15*math.sin(math.pi*t)**.5,.08,-.24)
    mesh('individual_palm_leaflets',vs,fs,'leaflight');finish('prop_palm' if variant==0 else 'prop_palm_b','environment')
RNG=np.random.default_rng(4804)
for name,height,count in [('prop_tropical_tree',11,2100),('prop_tropical_tree_b',14,2450),('prop_bush',2.8,340)]:
    reset(name);rod('tapered_trunk',(0,0,0),(.4,height*.65,0),height*.032,'wood',16);vs=[];fs=[]
    for i in range(count):
        cluster=i%7;angle=cluster*2.399;cx=math.cos(angle)*height*.20;cz=math.sin(angle)*height*.20;cy=height*(.60+(cluster%3)*.105);a=RNG.uniform(0,math.tau);rad=RNG.uniform(.1,1)**.5*height*.24;y=cy+RNG.uniform(-.17,.17)*height;c=(cx+math.cos(a)*rad,y,cz+math.sin(a)*rad)
        if i%30==0:rod('branch',(.3,height*.4,0),c,.06,'wood',8)
        foliage_leaf(vs,fs,c,a+RNG.uniform(-1,1),height*.12,height*.038,RNG.uniform(-.15,.15))
    o=mesh('branch_leaf_clusters',vs,fs,'leaf')
    cm=M['leaf'].copy();node=cm.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='LeafColor';cm.node_tree.links.new(node.outputs['Color'],cm.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);o.data.materials.clear();o.data.materials.append(cm)
    ca=o.data.color_attributes.new(name='LeafColor',type='FLOAT_COLOR',domain='CORNER')
    shades=[(.025,.065,.015),(.045,.12,.023),(.085,.18,.038),(.06,.145,.031)]
    for poly in o.data.polygons:
        c=shades[(poly.index//4)%4]
        for li in poly.loop_indices:ca.data[li].color=(*c,1)
    finish(name,'environment')
reset('prop_rock');vs=[];fs=[]
for k,(x,y,z,s) in enumerate([(-2,1,0,2.4),(1,1.5,.5,2.7),(0,.7,-2,1.5)]):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=1,location=coord((x,y,z)));o=bpy.context.object;o.scale=(s,s*.7,s*.65);o.data.materials.append(M['stone'])
    for v in o.data.vertices:v.co*=1+RNG.uniform(-.1,.1)
finish('prop_rock','environment')
exec(Path(__file__).with_name('art05_modules.py').read_text())
# A coastal peninsula with a scooped inlet, broad town terraces and craggy rear ridge.
def terrain_height(x,z):
    r=math.sqrt(((x+38)/94)**2+((z-78)/77)**2)
    r+=.035*math.sin(x*.12)+.025*math.sin(z*.17+x*.055)
    bay=math.exp(-((x-14)/31)**2-((z-20)/27)**2)*7
    coast=np.clip((1-r)*30,-5,4.2)-bay
    ridge=27*math.exp(-((x+75)/28)**2-((z-119)/22)**2)+18*math.exp(-((x+8)/24)**2-((z-128)/21)**2)
    h=float(coast+max(0,1-r)*ridge*2)
    terrace=min(x+108,34-x,z-38,98-z);b=np.clip(terrace/7,0,1)
    h=h*(1-b)+4.2*b
    if -112<x<5 and z<39: h=min(h, (z-32)*.75)
    h+=max(0,min(1,(z-102)/14))*(1.2*math.sin(x*.23+z*.17)+.6*math.sin(z*.6-x*.3))
    return max(-5,h)
reset('island_visual_test');vs=[];fs=[];nx=161;nz=133
for z in np.linspace(-7,164,nz):
    for x in np.linspace(-141,68,nx):vs.append((float(x),terrain_height(x,z),float(z)))
for j in range(nz-1):
    for i in range(nx-1):a=j*nx+i;fs.extend([(a,a+nx,a+1),(a+1,a+nx,a+nx+1)])
o=mesh('eroded_peninsula',vs,fs,'ground')
exec(Path(__file__).with_name('art05_terrain.py').read_text())
finish('island_visual_test','environment')
manifest['havana']=[]
def place(asset,x,z,heading=0,shadow=True,y=None):manifest['havana'].append({'asset':asset,'x':x,'y':terrain_height(x,z) if y is None else y,'z':z,'heading':heading,'shadow':shadow})
# Harbor mouth stays at the authoritative port origin (ship docking location).
for x in [-20,-46,-72]:place('port_pier',x,18,y=0)
for x in [-18,-36,-54,-72,-90]:place('port_quay',x,39,y=1.45)
for x in [-11,-37,-63,-89]:place('prop_stone_wall',x,45,y=3.9)
for x,z,asset in [(-22,51,'building_warehouse'),(-51,52,'building_warehouse'),(-83,54,'building_warehouse_b'),(-49,86,'building_governor'),(-87,89,'building_church')]:place(asset,x,z)
for x,z,asset in [(-7,73,'building_house_a'),(-23,75,'building_house_b'),(-7,93,'building_house_c'),(-23,96,'building_house_a'),(-68,78,'building_house_b'),(-107,76,'building_house_a'),(-108,99,'building_house_c'),(-68,99,'building_house_a'),(14,63,'building_house_b'),(14,85,'building_house_c')]:place(asset,x,z)
for x in [-35,-64]:
    for z in [56,76,96]:place('port_street',x,z,y=4.25)
for x in [-88,-68,-48,-28,-8]:place('port_street',x,65,heading=math.pi/2,y=4.25)
place('port_lighthouse',31,44)
for x,z in [(-102,40),(-83,39),(-58,37),(-31,37),(-7,47),(8,52),(26,65),(30,86),(-113,62),(-108,112),(-61,114),(-28,111),(-9,116)]:place('prop_palm' if x%2 else 'prop_palm_b',x,z,shadow=True)
for i in range(48):
    x=float(RNG.uniform(-123,41));z=float(RNG.uniform(109,148));h=terrain_height(x,z)
    if h>3:place('prop_tropical_tree' if i%3 else 'prop_tropical_tree_b',x,z,heading=float(RNG.uniform(0,6)),shadow=False)
for i in range(55):
    x=float(RNG.uniform(-125,42));z=float(RNG.uniform(30,149));h=terrain_height(x,z)
    if h>1 and (z>107 or x<-113 or x>29):place('prop_bush',x,z,shadow=False)
for x,z in [(-123,63),(-119,84),(-120,111),(-109,127),(-85,136),(-47,149),(4,136),(32,119),(45,91),(42,64),(29,36),(-110,30)]:place('prop_rock',x,z,heading=x,shadow=True,y=max(-.5,terrain_height(x,z)-.4))
for i in range(24):place('prop_barrel' if i%3 else 'prop_crate',-91+(i%12)*6,34+(i//12)*5,shadow=False,y=4.2)
for x,z in [(-40,62),(-62,62),(-17,64)]:place('prop_market_awning',x,z)
for x,z in [(-76,40),(-32,41),(-6,64)]:place('prop_cart',x,z)
for x,z in [(-11,13),(-34,16),(-58,14)]:place('prop_skiff',x,z,heading=.2,shadow=False,y=0)
exec(Path(__file__).with_name('art05_layout.py').read_text())
manifest['textures']=['/assets/'+str(Path(im.filepath_raw).relative_to(OUT)) for im in textures.values()]
manifest['quality']='Task05 High-End Art Pass; generated original albedo atlas, metric UVs, modular city districts; LOD0'
(SRC/'visual/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('HERO_ASSET_REPORT',json.dumps({k:v['triangles'] for k,v in manifest['assets'].items()}))

import runpy
runpy.run_path(str(ROOT/"scripts/optimize_visual_glb.py"))
