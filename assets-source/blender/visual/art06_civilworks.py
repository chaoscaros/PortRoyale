"""Constructed ground: retained plots, graded streets and quay-to-pier ramps."""
reset('port_civilworks')
# Tight structural pads and irregular fill replace identical full-lot slabs.
for plot,(name,x,z,y,w,d,heading) in enumerate(PLOTS):
 bounds={'building_warehouse':(20,15),'building_warehouse_b':(13,18),'building_governor':(21,17),'building_church':(14,23),'building_harbor_office':(16,16),'building_merchant_a':(13,14),'building_merchant_b':(11,17),'building_house_a':(10,12),'building_house_b':(12,11),'building_house_c':(9,15)}
 bw,bd=bounds[name];front=z-bd/2-.25
 bottom=min(natural_height(x+sx*bw/2,z+sz*bd/2) for sx in [-1,1] for sz in [-1,1])-.4
 bottom=min(bottom,y-.6)
 cube('embedded_structural_pad_'+name,(x,(bottom+y)/2,z),(bw,y-bottom,bd),'stone',.06)
 # Only downhill edges need masonry; staggered breaks reveal the infill behind.
 for side in [-1,1]:
  for seg in range(3):
   ez=z+(seg-1)*d*.27;ex=x+side*(w/2-.4)
   exposed=y-natural_height(ex,ez)
   if exposed<1.1 or (plot+seg)%4==0:continue
   top=y+.12+(seg%2)*.18;foot=max(y-2.8,natural_height(ex,ez)-.25)
   cube('half_buried_retaining_segment',(ex,(top+foot)/2,ez),(.6,top-foot,d*.22),'stone',.055)
 # Worn, staggered entrance slabs reach the road-facing facade.
 for k in range(3):cube('door_approach',(x+.08*math.sin(plot+k),y+.06+k*.08,front-.55+k*.34),(3.7-k*.12,.16,.38),'stone',.04)
 # Local rubble is embedded along exposed fill, not sprinkled over roads.
 for k in range(5):
  rx=x+w/2+.3+.7*math.sin(k*3.1+plot);rz=z+(k-2)*d*.18
  if any(road_sample(rx,rz,a,b)[0]<rw/2+1 for a,b,rw in ROADS):continue
  cube('embedded_fill_stone',(rx,terrain_height(rx,rz)-.12,rz),(.45+.2*(k%2),.35,.65),'rock',.08)
# Joined paving strips follow the surveyed road grade; foot of main axis is a cargo ramp.
for idx,(a,b,width) in enumerate(ROADS):
 ax,az,ay=a;bx,bz,by=b;length=math.hypot(bx-ax,bz-az);nx,nz=-(bz-az)/length,(bx-ax)/length
 if abs(by-ay)>2.5 and length<8:
  steps=16
 else:steps=max(1,int(length/1.5))
 for k in range(steps):
  t0=k/steps;t1=(k+1)/steps
  y0=ay+(by-ay)*t0+.08;y1=ay+(by-ay)*t1+.08
  if abs(by-ay)>2.5 and length<8:y0=y1
  x0,z0,_,nx,nz,half0=road_frame(a,b,width,t0);x1,z1,_,_,_,half1=road_frame(a,b,width,t1)
  mesh('graded_paving',[(x0+nx*half0,y0,z0+nz*half0),(x0-nx*half0,y0,z0-nz*half0),(x1-nx*half1,y1,z1-nz*half1),(x1+nx*half1,y1,z1+nz*half1)],[(0,1,2,3)],'stone' if width>=6 else 'dirt')
  for side in [-1,1]:
   if width<6 and k%3:continue
   rod('street_edge_stone',(x0+nx*(width/2+.08)*side,y0+.08,z0+nz*(width/2+.08)*side),(x1+nx*(width/2+.08)*side,y1+.08,z1+nz*(width/2+.08)*side),.12,'stone',6)
 # Cut-bank base beneath each graded strip, visible only where terrain recedes.
# Other two loading piers meet the quay through masonry abutments and short timber ramps.
for x in [-20,-72]:
 cube('quay_abutment',(x,1.8,34),(10,3.6,4),'stone',.08)
 for k in range(9):cube('quay_landing_steps',(x,2.04+k*.24,32.3+k*.42),(8,.24,.46),'stone',.025)
 for side in [-1,1]:rod('landing_bearer',(x+side*4,1.4,30),(x+side*4,3.8,36),.18,'wood',8)
for x in [-33,-59]:
 cube('continuous_quay_infill',(x,2.8,39),(8,2.8,10),'stone',.06)
finish('port_civilworks','ports')
