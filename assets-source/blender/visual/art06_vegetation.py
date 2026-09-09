"""Four distinct plant silhouettes, built from curved fronds / directed branch sprays."""
for variant in [0,1]:
 name='prop_palm' if variant==0 else 'prop_palm_b';reset(name)
 height,lean,length,nfronds=(17,1.15,4.6,10) if variant==0 else (10.5,3.1,6.3,13)
 line('bent_fibrous_trunk',[(lean*t*t,height*t,.6*math.sin(t*2.5)) for t in np.linspace(0,1,15)],.23 if variant==0 else .3,'bark')
 for y in np.arange(.4,height,.65):
  t=y/height;line('old_frond_scar',[(lean*t*t+.245*math.cos(a),y,.6*math.sin(t*2.5)+.245*math.sin(a)) for a in np.linspace(0,math.tau,9)],.025,'bark')
 vs=[];fs=[]
 for k in range(nfronds):
  angle=k*2.399+variant*.3;reach=length*(.82+(k%4)*.1);droop=2.4+(k%3)*.6
  def frond(t):return(lean+math.cos(angle)*reach*t,height+2*math.sin(t*3)-droop*t,.4+math.sin(angle)*reach*t)
  line('arched_frond_rib',[frond(t) for t in np.linspace(0,1,13)],.026,'leaflight')
  for t in np.linspace(.12,.95,14):
   for side in [-1,1]:foliage_leaf(vs,fs,frond(t),angle+side*(.8+.35*t),1.2*math.sin(math.pi*t)**.5,.065,-.23)
 mesh('separated_feather_leaflets',vs,fs,'leaflight');finish(name,'environment')
for name,height,dense in [('prop_tropical_tree',10.5,True),('prop_tropical_tree_b',15,False),('prop_bush',2.1,True)]:
 reset(name);rng=np.random.default_rng(606+int(height));vs=[];fs=[]
 bend=1.1 if dense else -2.1
 line('tapered_wind_trunk',[(bend*t*t,height*.76*t,.7*math.sin(t*2)) for t in np.linspace(0,1,12)],height*.023,'bark')
 # Dense broad, low spreading tiers versus sparse upright, windward gaps.
 branches=6 if height<3 else (9 if dense else 6)
 for branch in range(branches):
  a=branch*2.399+rng.uniform(-.42,.42);reach=height*(.34 if dense else .23)*rng.uniform(.65,1.35)
  y=height*(.44+branch/branches*.43+rng.uniform(-.08,.08))
  tip=(bend*.6+math.cos(a)*reach,y,math.sin(a)*reach)
  elbow=(math.cos(a)*reach*.45,y-height*.12,math.sin(a)*reach*.35)
  line('forked_primary_branch',[(bend*.2,height*.34,0),elbow,tip],height*.012,'bark')
  for twig in range(3 if height<3 else (4 if dense else 3)):
   ta=a+(twig-1.5)*.55+rng.uniform(-.25,.25);tc=(tip[0]+math.cos(ta)*height*.13,tip[1]+(twig%2)*height*.09,tip[2]+math.sin(ta)*height*.13)
   rod('twig',tip,tc,height*.003,'bark',6)
   for i in range(18 if height<3 else (36 if dense else 27)):
    t=rng.random();lateral=rng.normal(0,height*.08)
    c=(tip[0]*(1-t)+tc[0]*t+math.sin(ta)*lateral,tc[1]+rng.normal(0,height*.036),tip[2]*(1-t)+tc[2]*t-math.cos(ta)*lateral)
    foliage_leaf(vs,fs,c,ta+rng.uniform(-1.4,1.4),height*.14,height*.042,rng.uniform(-.2,.16))
 o=mesh('directed_leaf_sprays',vs,fs,'leaf');ca=o.data.color_attributes.new(name='LeafColor',type='BYTE_COLOR',domain='CORNER')
 cm=M['leaf'].copy();cm.name='art06_canopy_'+name;node=cm.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='LeafColor';cm.node_tree.links.new(node.outputs['Color'],cm.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);o.data.materials.clear();o.data.materials.append(cm)
 shades=[(.03,.073,.018),(.065,.12,.033),(.048,.10,.028),(.082,.145,.045)]
 for poly in o.data.polygons:
  for li in poly.loop_indices:ca.data[li].color=(*shades[(poly.index//4)%4],1)
 finish(name,'environment')
