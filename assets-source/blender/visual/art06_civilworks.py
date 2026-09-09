"""Constructed ground: retained plots, graded streets and quay-to-pier ramps."""
reset('port_civilworks')
# Foundations are cut into prepared terrain, with exposed downhill retaining faces.
for name,x,z,y,w,d,heading in PLOTS:
 bottom=min(natural_height(x+sx*w/2,z+sz*d/2) for sx in [-1,1] for sz in [-1,1])-.6
 bottom=min(bottom,y-.6)
 cube('retained_plot_'+name,(x,(bottom+y)/2,z),(w,y-bottom,d),'stone',.06)
 cube('plot_coping_'+name,(x,y+.015,z),(w+.22,.18,d+.22),'stone',.025)
 # Road-facing steps and a low apron; facade remains the vertical focal point.
 for k in range(3):cube('door_approach',(x,y+.05+k*.12,z-d/2-.45+k*.3),(3.8,.15+k*.24,.34),'stone',.025)
 for side in [-1,1]:
  if y>6:
   cube('low_retaining_parapet',(x+side*w/2,y+.5,z),( .35,.8,d),'stone',.035)
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
  x0=ax+(bx-ax)*t0;z0=az+(bz-az)*t0;x1=ax+(bx-ax)*t1;z1=az+(bz-az)*t1
  mesh('graded_paving',[(x0+nx*width/2,y0,z0+nz*width/2),(x0-nx*width/2,y0,z0-nz*width/2),(x1-nx*width/2,y1,z1-nz*width/2),(x1+nx*width/2,y1,z1+nz*width/2)],[(0,1,2,3)],'stone')
  for side in [-1,1]:
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
