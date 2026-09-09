"""Deterministic port civil plan; metres, rendering-only, shared by terrain and placement."""
import math

def clamp(v,a=0,b=1):return min(b,max(a,v))
def smooth(a,b,v):
 t=clamp((v-a)/(b-a));return t*t*(3-2*t)
# One datum per constructed plot. Footprints include galleries and approach aprons.
PLOTS=[
 ('building_warehouse',-23,53,4.2,23,19,.035),('building_warehouse_b',-76,53,4.2,17,22,0),
 ('building_harbor_office',12,62,4.2,20,19,.03),
 ('building_merchant_a',-24,78,6.4,17,18,-.055),('building_merchant_b',-70,76,6.4,15,21,0),
 ('building_governor',-46,103,10.4,26,23,0),('building_church',-91,99,10.4,20,28,.05),
 ('building_house_a',-109,72,4.2,14,17,.10),('building_house_c',-109,111,12.5,13,19,-.08),
 ('building_house_b',-77,124,15.0,16,16,.12),('building_house_a',-51,129,16.4,14,17,-.06),
 ('building_house_c',-19,107,11.8,13,19,.05),('building_house_b',4,93,8.0,16,16,-.08),
 ('building_house_a',5,119,14.2,14,17,.1),('building_merchant_b',-103,47,4.2,15,21,.04),
]
# Centerlines include explicit grades, forming a continuous pedestrian/cargo network.
ROADS=[((-46,32,1.95),(-46,43,4.2),9),((-46,43,4.2),(-46,60,4.2),9),
 ((-46,60,4.2),(-46,72,6.4),8),((-46,72,6.4),(-46,87,6.4),8),
 ((-46,87,6.4),(-46,91,10.4),10),
 ((-112,64,4.2),(-46,64,4.95),6),((-46,64,4.95),(20,64,4.2),6),
 ((-46,84,6.4),(-83,84,10.4),6),
 ((-33,86,6.4),(-9,90,8),5),((-9,90,8),(-9,119,14.2),5),
 ((-61,92,10.4),(-63,119,15),5),((-63,119,15),(-49,120,16.4),5),
 ((-63,119,15),(-96,122,12.5),4)]

def natural_height(x,z):
 r=math.hypot((x+38)/94,(z-78)/77)+.035*math.sin(x*.12)+.025*math.sin(z*.17+x*.055)
 coast=clamp((1-r)*30,-5,4.2)-math.exp(-((x-14)/31)**2-((z-20)/27)**2)*7
 # Oblique limestone ridge: broad shoulder, two saddles, stepped bedding and one ravine.
 axis=z-130-(x+45)*.14
 mass=17*math.exp(-((x+51)/79)**4-(axis/28)**2)
 saddle=3*math.exp(-((x+29)/15)**2-((z-130)/30)**2)
 ravine=3*math.exp(-((x+106+(z-114)*.55)/5)**2)*smooth(103,122,z)
 bedding=.65*math.sin((z-x*.22)*.5)+.65*math.sin(x*.19+z*.12)
 h=coast+smooth(92,119,z)*max(0,mass-saddle-ravine+bedding)*smooth(0,.28,1-r)
 if -112<x<5 and z<39:h=min(h,(z-32)*.75)
 return max(-5,h)

def road_frame(a,b,width,t):
 dx,dz=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dz);nx,nz=-dz/length,dx/length
 bend=0 if width>=8 else math.sin(math.pi*t)*(.6+.35*math.sin(a[0]))
 x=a[0]+dx*t+nx*bend;z=a[1]+dz*t+nz*bend
 half=width/2*(1+(.035 if width>=8 else .14)*math.sin(t*math.pi*2+a[0]*.13))
 return x,z,a[2]+(b[2]-a[2])*t,nx,nz,half

def road_sample(x,z,a,b):
 dx,dz=b[0]-a[0],b[1]-a[1];t=clamp(((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz))
 width=next((w for aa,bb,w in ROADS if aa==a and bb==b),8)
 px,pz,y,_,_,_=road_frame(a,b,width,t)
 return math.hypot(x-px,z-pz),y

def terrain_height(x,z):
 h=natural_height(x,z)
 for _,px,pz,y,w,d,_ in PLOTS+[('plaza',-46,78,6.4,23,18,0)]:
  # Preserve the structural footprint; break the outer fill into irregular shoulders.
  edge=max(abs(x-px)-w/2,abs(z-pz)-d/2)
  feather=3.8+1.8*math.sin(x*.19+z*.11)+.9*math.sin(z*.43-x*.15)
  blend=smooth(-.1,max(1.5,feather),edge)
  h=h*blend+y*(1-blend)
 for a,b,w in ROADS:
  distance,y=road_sample(x,z,a,b);f=1-smooth(w/2,w/2+2,distance)
  h=h*(1-f)+(y-.14)*f
 return h

def in_town(x,z,margin=2):
 return any(abs(x-px)<w/2+margin and abs(z-pz)<d/2+margin for _,px,pz,_,w,d,_ in PLOTS) or any(road_sample(x,z,a,b)[0]<w/2+margin for a,b,w in ROADS) or (abs(x+46)<16 and abs(z-78)<13)
