"""Authored harbor micro-narrative modules. Pure render assets, no inventory entities."""
reset('prop_cargo_stack')
for x,z,y in [(-1,-.7,0),(1,-.7,0),(-1,1,0),(1,1,0),(0,0,1.6)]:
    cube('cargo_crate',(x,y+.75,z),(1.8,1.5,1.45),'wood',.055)
    for xx in [-.78,.78]:cube('iron_binding',(x+xx,y+.75,z),(.08,1.57,1.5),'iron',.018)
    for yy in [.14,1.36]:cube('crate_rim',(x,y+yy,z-.77),(1.8,.11,.15),'deck',.018)
    rod('cross_timber',(x-.7,y+.2,z-.82),(x+.7,y+1.3,z-.82),.09,'deck',8)
finish('prop_cargo_stack','props')
reset('prop_sacks')
for x,z,h in [(-.7,0,.6),(.6,.3,.6),(0,-.4,1.5)]:
    o=sphere('linen_cargo_sack',(x,h,z),(.62,.75,.49),'cloth',16,12)
    for v in o.data.vertices:v.co.x*=1+.1*math.sin(v.co.z*12)
    rod('tied_neck',(x,h+.6,z),(x,h+.9,z),.15,'rope',12)
    line('sack_tie',[(x+.19*math.cos(a),h+.65,z+.19*math.sin(a)) for a in np.linspace(0,math.tau,21)],.035,'rope')
finish('prop_sacks','props')
reset('prop_mooring')
rod('cast_iron_bollard',(0,0,0),(0,1.1,0),.3,'iron',20)
rod('horn',(-.7,.9,0),(.7,.9,0),.17,'iron',16)
for k in range(4):
    line('coiled_hemp',[(1.1+(.42+k*.10)*math.cos(a),.12+k*.035,(.42+k*.10)*math.sin(a)) for a in np.linspace(0,math.tau,49)],.044,'rope')
line('mooring_line',[(0,.65,0),(-.8,.3,1.8),(-1.1,-1,3),(-1.2,-2.5,4)],.055,'rope')
finish('prop_mooring','props')
reset('port_crane')
for x in [-1,1]:cube('crane_foot',(x,.2,0),(.6,.4,3),'stone',.05)
rod('timber_upright',(0,.3,0),(0,8,0),.30,'wood',16)
rod('loading_jib',(0,7,0),(0,7,-6),.25,'wood',16)
rod('diagonal_jib_brace',(0,2,0),(0,7,-5.5),.18,'wood',14)
line('lifting_rope',[(0,1,1),(0,8,0),(0,7,-6),(0,2,-6)],.06,'rope')
line('cargo_hook',[(0,2,-6),(.4,1.6,-6),(.3,1.2,-6),(-.1,1.15,-6),(-.3,1.4,-6)],.09,'iron')
rod('windlass',(-1.1,2,0),(1.1,2,0),.4,'wood',20)
finish('port_crane','ports')
reset('port_plaza')
for x in np.arange(-12,12,1.3):
    for z in np.arange(-10,10,1.3):cube('plaza_limestone',(float(x),.06,float(z)),(1.26,.15,1.26),'stone',.02)
for r,y in [(3.5,.25),(3.15,.55),(2.8,.75)]:
    line('octagonal_fountain_rim',[(r*math.cos(a),y,r*math.sin(a)) for a in np.linspace(0,math.tau,9)],.20,'stone')
rod('fountain_column',(0,0,0),(0,3.4,0),.32,'stone',24)
sphere('fountain_basin',(0,2.7,0),(1.7,.3,1.7),'stone',32,12)
for x in [-8,8]:
    cube('public_bench',(x,.9,0),(1,.18,4),'wood',.04)
    for z in [-1.5,1.5]:cube('bench_support',(x,.45,z),(.7,.9,.3),'iron',.03)
finish('port_plaza','ports')
reset('prop_grass')
vs=[];fs=[]
for k in range(90):
    a=RNG.uniform(0,math.tau);x=RNG.uniform(-1.8,1.8);z=RNG.uniform(-1.8,1.8);h=RNG.uniform(.25,.9);w=.04
    i=len(vs);vs.extend([(x-w,0,z),(x+w,0,z),(x+.18*math.cos(a),h,z+.18*math.sin(a))]);fs.append((i,i+1,i+2))
mesh('dry_grass_blades',vs,fs,'leaflight');finish('prop_grass','environment')
reset('port_pier_small')
for z in np.arange(-7,7,.36):cube('landing_plank',(0,1.45,float(z)),(4.6,.2,.34),'wood',.025)
for x in [-2,2]:
    for z in [-6,-2,2,6]:rod('landing_pile',(x,-3,z),(x,2,z),.22,'wood',14)
finish('port_pier_small','ports')
