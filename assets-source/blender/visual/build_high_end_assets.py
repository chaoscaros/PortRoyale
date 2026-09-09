"""Task07 Hero Port Third Pass. Blender 4.5; metric source -> Y-up GLB.
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

exec(Path(__file__).with_name('art06_materials.py').read_text())

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
    for side in ([-1,1] if int(abs(x)*10)%3 else [1]):
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
                        vs.append((side*((w/2+.65)*t),y+rise*(1-t)+math.sin(a)*.14+.05+(.018*math.sin(col*13+row*7)),z+math.cos(a)*.20))
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
        facade_start=set(bpy.context.scene.objects)
        by=4.5 if h>7 else 1.0
        cube('gallery_floor',(0,by,-d/2-1.5),(w+1,.27,2.7),'stone',.06)
        for x in np.arange(-w/2+.4,w/2,.55):rod('turned_balustrade',(float(x),by,-d/2-2.65),(float(x),by+1.05,-d/2-2.65),.055,'wood',10)
        for y in [by+.2,by+1.1]:cube('balcony_handrail',(0,y,-d/2-2.65),(w,.12,.14),'wood',.035)
        for x in np.arange(-w/2+.5,w/2,2.5):
            rod('gallery_column',(float(x),.65,-d/2-2.4),(float(x),by+.05,-d/2-2.4),.2,'stone',16)
            if kind=='hall':arch('arcade',float(x)+1.2,.65,-d/2-2.4,2.1,3.65)
    if kind=='home':
        for ob in set(bpy.context.scene.objects)-facade_start:ob['facadeOption']=0
        facade_start=set(bpy.context.scene.objects)
        # Alternate shallow iron balcony and a lower shop awning, not a second full house.
        by=4.5 if h>7 else 1.0
        cube('compact_balcony',(w*.18,by,-d/2-.75),(w*.55,.19,1.3),'wood',.03)
        for x in np.linspace(-w*.09,w*.45,8):rod('iron_balcony_spindle',(x,by,-d/2-1.35),(x,by+.95,-d/2-1.35),.035,'iron',8)
        line('shaped_balcony_rail',[(-w*.09,by+1,-d/2-.9),(-w*.09,by+1,-d/2-1.4),(w*.45,by+1,-d/2-1.4),(w*.45,by+1,-d/2-.9)],.06,'iron')
        mesh('door_shade',[(-2,3.9,-d/2),(1.4,3.9,-d/2),(1.6,3.45,-d/2-1.8),(-2.1,3.45,-d/2-1.8)],[(0,1,2,3)],'cloth')
        for ob in set(bpy.context.scene.objects)-facade_start:ob['facadeOption']=1
    if kind=='warehouse':
        for x in [-w*.25,w*.25]:
            arch('warehouse_loading_arch',x,.7,-d/2-.35,2.8,4.1)
            cube('loading_door',(x,2.45,-d/2-.16),(2.6,3.5,.15),'wood',.04)
            line('awning_support',[(x-1.5,5,-d/2),(x-1.5,4,-d/2-2),(x+1.5,4,-d/2-2),(x+1.5,5,-d/2)],.08,'dark')
            mesh('loading_canvas',[(x-1.6,5,-d/2),(x+1.6,5,-d/2),(x+1.6,4,-d/2-2),(x-1.6,4,-d/2-2)],[(0,1,2,3)],'cloth')
    tiled_roof(w,d,h+.8,2.7 if kind!='hall' else 3.2)
    roof_mode=sum(map(ord,name))%4
    if roof_mode in [0,3]:
        cube('chimney',(w*.25,h+2.4,d*.2),(.9,2.2,.9),'stone',.05)
        cube('chimney_cap',(w*.25,h+3.55,d*.2),(1.2,.22,1.2),'stone',.05)
    elif roof_mode==1:
        cube('small_dormer',(w*.20,h+1.8,-d*.15),(1.6,1.5,1.9),'wall',.04)
        cube('dormer_shutter',(w*.20,h+1.8,-d*.15-1),(1.05,.85,.1),'waterblue',.03)
        cube('dormer_cap',(w*.20,h+2.62,-d*.15),(1.9,.18,2.1),'roof',.025)
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
# Bowed transom and quarter galleries follow a tapered historical stern envelope.
vs=[];fs=[];sections=24
for level in [0,1]:
 for k in range(sections+1):
  t=k/sections;x=(t*2-1)*(3.15 if level==0 else 2.7)
  vs.append((x,3.15+level*2.3,-14.7+.095*x*x+level*.22))
for k in range(sections):fs.append((k,k+1,k+sections+2,k+sections+1))
mesh('bowed_transom',vs,fs,'waterblue')
for side in [-1,1]:
 mesh('tapered_quarter_gallery',[(side*3.45,3.1,-10),(side*3.15,3.15,-13.8),(side*2.7,5.45,-13.8),(side*3.0,5.45,-10)],[(0,1,2,3)],'waterblue')
 for z in [-13.1,-12.2,-11.3]:
  x=side*(3.05+(z+13)*.085)
  cube('quarter_gallery_side_window',(x,4.35,z),(.1,.9,.56),'glass',.025)
  for dz in [-.36,.36]:rod('quarter_gallery_pillar',(x,3.75,z+dz),(x-side*.12,5,z+dz),.05,'brass',8)
 line('headrail_scroll',[(side*1.9,3.4,13),(side*1.2,4,16),(side*.4,4.5,19)],.09,'brass')
for x in [-2.15,-1.07,0,1.07,2.15]:
 z=-14.62+.095*x*x
 cube('stern_glazing',(x,4.35,z),(.76,1.1,.1),'glass',.02)
 for dx in [-.44,.44]:rod('stern_gilt_frame',(x+dx,3.7,z-.06),(x+dx,5,z-.06),.045,'brass',8)
 rod('window_crossbar',(x-.39,4.3,z-.07),(x+.39,4.3,z-.07),.025,'deck',6)
for y in [3.55,5.13]:line('bowed_stern_moulding',[(x,y,-14.8+.095*x*x) for x in np.linspace(-3.2,3.2,19)],.065,'brass')
outline=[(-3.2,5.65,-10),(3.2,5.65,-10)]+[(x,5.65,-15.3+.085*x*x) for x in np.linspace(3.2,-3.2,25)]
mesh('curved_quarterdeck_balcony',outline,[tuple(range(len(outline)))],'deck')
for x in np.linspace(-3.1,3.1,16):
 z=-15.25+.085*x*x
 rod('stern_balcony_baluster',(x,5.65,z),(x*.97,6.5,z+.1),.045,'wood',8)
line('swept_balcony_handrail',[(x,6.5,-15.15+.085*x*x) for x in np.linspace(-3.2,3.2,25)],.085,'wood')
for side in [-1,1]:line('quarterdeck_rail',[(side*3.2,6.1,-10),(side*3.15,6.5,-12),(side*3.1,6.5,-14.35)],.065,'wood')
for y in [-.8,.2,1.2]:rod('rudder_gudgeon',(0,y,-14.7),(0,y,-15.4),.22,'iron',10)
rod('rudder_stock',(0,-1.5,-15),(0,4,-15),.18,'iron',16);cube('rudder_blade',(0,-.65,-15.5),(.32,3,1.3),'wood',.05)
line('tiller_link',[(0,3.9,-15),(0,4.2,-13.8),(.65,4.2,-12.5)],.09,'wood')
rod('bowsprit',(0,3,14),(0,5,22),.19,'wood',20)
# Dense curved sails with edge ropes and authentic broad-seam construction.
def sail_point(name,corners,s,t):
    a=np.array(corners[0])*(1-s)+np.array(corners[1])*s
    b=np.array(corners[3])*(1-s)+np.array(corners[2])*s
    p=a*(1-t)+b*t
    seed=abs(corners[0][1]*.11+corners[0][2]*.17)
    fullness=(.72+.38*math.sin(seed))*math.sin(math.pi*s)**(.8+.2*math.sin(seed))*math.sin(math.pi*t)**.75*(.82+.28*s)
    p[0 if name=='forward_jib' else 2]+=fullness
    p[1]-=(.25+.16*math.sin(seed))*math.sin(math.pi*s)*(1-t)**2
    p[0]+=.14*math.sin(seed)*math.sin(math.pi*t)*math.sin(math.pi*s)
    return tuple(p)
def sail(name,corners,nu=30,nv=22):
    vs=[];fs=[]
    for j in range(nv+1):
        t=j/nv
        for i in range(nu+1):
            s=i/nu;vs.append(sail_point(name,corners,s,t))
    for j in range(nv):
        for i in range(nu):a=j*(nu+1)+i;fs.append((a,a+1,a+nu+2,a+nu+1))
    o=mesh(name,vs,fs,'cloth');sol=o.modifiers.new('sewn_edge_thickness','SOLIDIFY');sol.thickness=.025
    for p in o.data.polygons:p.use_smooth=True
    line('sail_bolt_rope',[sail_point(name,corners,s,0) for s in np.linspace(0,1,8)]+[sail_point(name,corners,1,t) for t in np.linspace(0,1,8)]+[sail_point(name,corners,s,1) for s in np.linspace(1,0,8)]+[sail_point(name,corners,0,t) for t in np.linspace(1,0,8)],.035,'rope')
    # Reinforced corners lie on the same surface; load-bearing sheets meet their tips.
    for cs,ct in [(0,0),(1,0),(0,1),(1,1)]:
        du=.065 if cs==0 else -.065;dv=.10 if ct==0 else -.10
        patch=[sail_point(name,corners,cs,ct),sail_point(name,corners,cs+du,ct),sail_point(name,corners,cs,ct+dv)]
        patch=[(x,y,z-.03) for x,y,z in patch]
        mesh('reinforced_sail_corner',patch,[(0,1,2)],'cloth')
    for cs in [0,1]:
        tip=sail_point(name,corners,cs,0)
        target=(max(-4,min(4,tip[0])),3.6,tip[2]-2.8)
        line('clew_sheet',[tip,target],.025,'rope')
    for i in range(1,10):
        s=i/12;a=np.array(corners[0])*(1-s)+np.array(corners[1])*s;b=np.array(corners[3])*(1-s)+np.array(corners[2])*s
        pts=[]
        for t in np.linspace(0,1,15):pts.append(sail_point(name,corners,s,t))
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
exec(Path(__file__).with_name('art06_quay.py').read_text())
reset('port_street');cube('paved_roadbed',(0,0,0),(8,.14,20),'stone',.03)
for x in [-4,4]:cube('street_curb',(x,.13,0),(.25,.24,20),'stone',.025)
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
exec(Path(__file__).with_name('art06_vegetation.py').read_text())
reset('prop_rock');vs=[];fs=[]
for k,(x,y,z,s) in enumerate([(-2,1,0,2.4),(1,1.5,.5,2.7),(0,.7,-2,1.5)]):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=1,location=coord((x,y,z)));o=bpy.context.object;o.scale=(s,s*.7,s*.65);o.data.materials.append(M['stone'])
    for v in o.data.vertices:v.co*=1+RNG.uniform(-.1,.1)
finish('prop_rock','environment')
exec(Path(__file__).with_name('art05_modules.py').read_text())
# A coastal peninsula with a scooped inlet, broad town terraces and craggy rear ridge.
exec(Path(__file__).with_name('art06_site.py').read_text())
exec(Path(__file__).with_name('art06_civilworks.py').read_text())
reset('island_visual_test');vs=[];fs=[];nx=161;nz=133
for z in np.linspace(-7,164,nz):
    for x in np.linspace(-141,68,nx):vs.append((float(x),terrain_height(x,z),float(z)))
for j in range(nz-1):
    for i in range(nx-1):a=j*nx+i;fs.extend([(a,a+nx,a+1),(a+1,a+nx,a+nx+1)])
o=mesh('eroded_peninsula',vs,fs,'ground')
exec(Path(__file__).with_name('art06_terrain.py').read_text())
finish('island_visual_test','environment')
exec(Path(__file__).with_name('art06_layout.py').read_text())
manifest['textures']=['/assets/'+str(Path(im.filepath_raw).relative_to(OUT)) for im in textures.values()]
manifest['quality']='Task07 Hero Port Third Pass; paired PBR, irregular civil works, facade combinations and ecological clusters'
(SRC/'visual/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('HERO_ASSET_REPORT',json.dumps({k:v['triangles'] for k,v in manifest['assets'].items()}))

import runpy
runpy.run_path(str(ROOT/"scripts/optimize_visual_glb.py"))

# Prepared native LOD1 levels are part of the reproducible delivery.
runpy.run_path(str(SRC/"visual/build_lod1.py"))
