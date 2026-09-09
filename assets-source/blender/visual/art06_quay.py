"""A quay with a genuine central stair opening, not steps against a solid block."""
reset('port_quay')
for side in [-1,1]:cube('quay_side_abutment',(side*6.5,1.3,0),(5,2.6,10),'stone',.07)
cube('quay_rear_land',(0,1.3,2),(8,2.6,6),'stone',.05)
for k in range(11):
 y=.25+k*.235;z=-8+k*.65
 cube('open_quay_stair',(0,(y-2)/2,z),(8,y+2,.7),'stone',.025)
for x in [-6.5,6.5]:cube('quay_coping',(x,2.65,0),(5,.15,10),'stone',.035)
cube('quay_upper_landing',(0,2.65,2),(8,.15,6),'stone',.035)
finish('port_quay','ports')
