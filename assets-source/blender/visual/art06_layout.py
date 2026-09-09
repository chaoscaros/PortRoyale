"""Purposeful city blocks and ecological planting; no random buildings on slopes."""
manifest['havana']=[]
def place(asset,x,z,heading=0,shadow=True,y=None):
 manifest['havana'].append(dict(asset=asset,x=x,y=terrain_height(x,z) if y is None else y,z=z,heading=heading,shadow=shadow))
place('port_civilworks',0,0,y=0)
for a,x,z,y,w,d,angle in PLOTS:place(a,x,z,heading=angle,y=y+.11)
for x in [-20,-46,-72]:place('port_pier',x,18,y=0)
for x in [-20,-46,-72,-90]:place('port_quay',x,39,y=1.45)
place('port_plaza',-46,78,y=6.5)
place('port_lighthouse',31,46,y=terrain_height(31,46))
place('port_pier_small',18,31,heading=.20,y=0)
# Leave center of the main pier as a clear transport corridor.
for x in [-20,-46,-72]:
 place('port_crane',x+2,27,y=1.95)
 for z in [8,21]:place('prop_mooring',x-3.2,z,y=1.98)
 for z in [16,23]:place('prop_cargo_stack',x+1.4,z,y=1.98)
 place('prop_sacks',x-1.6,13,y=1.98)
for x,z in [(-16,43),(-31,43),(-75,43),(-86,47),(-14,60)]:
 place('prop_cargo_stack',x,z,heading=.2,y=4.3);place('prop_sacks',x+3,z+.5,y=4.3)
 for dx in [-1,0,1]:place('prop_barrel',x+dx,z-2,shadow=False,y=4.3)
for x,z,y in [(-36,77,6.5),(-56,80,6.5),(-20,71,6.5),(-73,69,6.5)]:place('prop_market_awning',x,z,y=y)
for x,z,y in [(-46,53,4.3),(-68,62,4.4),(-30,70,6.3)]:place('prop_cart',x,z,y=y,heading=.3)
for x,z in [(-10,13),(-34,16),(-58,14)]:place('prop_skiff',x,z,heading=.2,shadow=False,y=0)
# Four authored silhouette languages, distributed by exposure and land use.
for i,(x,z) in enumerate([(-108,34),(-95,34),(-12,38),(18,48),(29,62),(-113,91),(-7,79),(-63,91)]):
 place('prop_palm' if i%3 else 'prop_palm_b',x,z,heading=i*.77,shadow=True)
rng=np.random.default_rng(6061)
for i in range(150):
 x=float(rng.uniform(-120,32));z=float(rng.uniform(97,151));h=terrain_height(x,z)
 slope=math.hypot(terrain_height(x+1,z)-terrain_height(x-1,z),terrain_height(x,z+1)-terrain_height(x,z-1))*.5
 if h<3 or slope>2.2 or in_town(x,z,3):continue
 # Gaps along the exposed spine, dense sheltered lower slopes, upright sparse trees above.
 if h>23 and i%3:continue
 place('prop_tropical_tree_b' if i%4==0 else 'prop_tropical_tree',x,z,heading=i*2.399,shadow=False)
for i in range(100):
 x=float(rng.uniform(-128,42));z=float(rng.uniform(30,153));h=terrain_height(x,z)
 if h<1.5 or in_town(x,z,1):continue
 if z<93 and -107<x<22:continue
 place('prop_bush' if i%5==0 else 'prop_grass',x,z,heading=i*1.43,shadow=False,y=h+.04)
# Small sheltered garden remnants soften unbuilt ground between retained blocks.
# Keep loading aprons and street centerlines clear; clumps taper rather than form hedges.
for garden,(cx,cz) in enumerate([(-61,52),(-5,51),(-91,74),(-34,115),(-85,135),(-2,134)]):
 for k,(dx,dz) in enumerate([(-1.7,.4),(.3,1.9),(1.8,-.6),(-.6,-1.8),(.8,.1)]):
  x=cx+dx;z=cz+dz
  if in_town(x,z,.25):continue
  place('prop_bush' if k<2 else 'prop_grass',x,z,heading=garden*1.23+k*2.399,shadow=False,y=terrain_height(x,z)+.02)
# Broken limestone bedding on exposed shoulders; no decorative rock ring around the island.
for i,(x,z) in enumerate([(-121,67),(-120,75),(-115,122),(-110,128),(-103,136),(-96,140),(-87,138),(-37,139),(-31,143),(-23,145),(17,136),(28,128),(35,88),(37,84),(28,34)]):
 place('prop_rock',x,z,heading=-.35+(i%3)*.17,y=terrain_height(x,z)-1.1)
manifest['site']={'plots':[dict(asset=a,x=x,z=z,y=y,width=w,depth=d,heading=h) for a,x,z,y,w,d,h in PLOTS], 'roads':[dict(start=a,end=b,width=w) for a,b,w in ROADS], 'materialMetresPerTile':4}
