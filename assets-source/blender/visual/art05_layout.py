"""District composition. Keep the authoritative docking origin clear."""
# Replace isolated lawn lots with contiguous merchant frontage and public space.
for p in manifest['havana']:
    if p['asset']=='building_governor':p.update(x=-51,z=98,y=4.2)
    if p['asset']=='building_house_a' and p['x']==-68 and p['z']==99:p.update(x=-62,z=118,y=terrain_height(-62,118))
    if p['asset']=='building_house_b' and p['x']==-68:p.update(x=-76,z=79,y=4.2)
# Three merchant/administrative modules and infill town homes.
for x,z,a,r in [(-47,75,'port_plaza',0),(-17,82,'building_merchant_a',0),(-100,64,'building_merchant_b',.08),(12,66,'building_harbor_office',0),(-107,94,'building_merchant_b',0),(-2,108,'building_house_b',.10),(-20,112,'building_house_c',-.07),(-90,114,'building_house_a',.08),(16,99,'building_house_c',-.15)]:
    # Replace overlapping previous simple lots.
    if a.startswith('building_'):
        manifest['havana'][:]=[p for p in manifest['havana'] if not (p['asset'].startswith('building_') and math.hypot(p['x']-x,p['z']-z)<10)]
    place(a,x,z,heading=r,y=4.2 if 38<z<100 else None)
# Cargo grouped around doors, not evenly spaced like decorative fence posts.
manifest['havana'][:]=[p for p in manifest['havana'] if p['asset'] not in ['prop_crate','prop_barrel']]
for x,z in [(-90,39),(-81,40),(-67,39),(-58,39),(-38,39),(-24,40),(-12,41),(-33,55),(-72,59)]:
    place('prop_cargo_stack',x,z,heading=.12*(x%4),y=4.2)
    place('prop_sacks',x+3,z+1,heading=x,y=4.2)
    for dx,dz in [(2,-2),(3.4,-2),(2.7,-.7)]:place('prop_barrel',x+dx,z+dz,shadow=False,y=4.2)
for x in [-20,-46,-72]:
    place('port_crane',x+2,28,y=1.95)
    for z in [8,19,28]:place('prop_mooring',x-3.2,z,y=1.98)
    place('prop_cargo_stack',x+1,22,y=1.98)
    place('prop_sacks',x-1,15,y=1.98)
place('port_pier_small',18,31,heading=.25,y=0)
for x,z in [(-10,82),(-24,91),(-83,72),(-91,70),(-34,60),(-49,61)]:place('prop_market_awning',x,z,heading=.05,y=4.2)
# Vegetation accents irregular rocky margins, leaving urban circulation readable.
for k in range(200):
    x=float(RNG.uniform(-129,45));z=float(RNG.uniform(26,152));h=terrain_height(x,z)
    if h>2.5 and (z>110 or x<-114 or x>30):place('prop_grass',x,z,heading=k,shadow=False,y=h+.05)
for k in range(32):
    a=k*2.399;x=-38+96*math.cos(a);z=78+72*math.sin(a);h=terrain_height(x,z)
    if h<4 and z>40:place('prop_rock',x,z,heading=a,shadow=True,y=h-.4)
for x,z in [(-110,121),(-88,131),(-70,128),(-40,140),(-11,128),(19,117)]:place('prop_rock',x,z,heading=x,y=terrain_height(x,z)-1)
# Infill: occupy leftover urban lots while keeping the plaza and two main streets open.
for row,z in enumerate([57,76,94,111]):
    for col,x in enumerate([-113,-96,-79,-61,-44,-27,-10,9,26]):
        if abs(x+35)<7 or abs(x+64)<6 or (abs(x+47)<16 and abs(z-75)<13):continue
        if terrain_height(x,z)<3:continue
        buildings=[p for p in manifest['havana'] if p['asset'].startswith('building_')]
        if any(abs(p['x']-x)<14 and abs(p['z']-z)<15 for p in buildings):continue
        place(['building_house_a','building_house_c','building_merchant_b'][(row+col)%3],x,z,heading=((col%3)-1)*.07)
# Keep the un-terraced summit geological instead of placing a house on its apex.
manifest['havana'][:]=[p for p in manifest['havana'] if not (p['asset']=='building_house_a' and p['x']==-62 and p['z']==118)]
for x,z in [(-61,118),(-65,119),(-69,119),(-73,120),(-64,123),(-69,124),(-74,124),(-78,121),(-77,116),(-71,115),(-66,114),(-59,122)]:
    place('prop_rock',x,z,heading=x*.37,y=terrain_height(x,z)-.7)
