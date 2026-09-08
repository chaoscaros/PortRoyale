"""Deduplicate GLB embedded PNGs into a shared, content-addressed local texture library.
Only geometry stays in each binary. Source .blend files retain packed editable textures.
"""
import json,struct,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest_path=ROOT/'assets-source/blender/visual/manifest.json'
m=json.loads(manifest_path.read_text());shared=ROOT/'public/assets/textures/shared';shared.mkdir(parents=True,exist_ok=True)
for a in m['assets'].values():
    path=ROOT/('public'+a['url']);data=path.read_bytes();jsonlen=struct.unpack_from('<I',data,12)[0];g=json.loads(data[20:20+jsonlen]);binstart=20+jsonlen+8;binary=data[binstart:];images=g.get('images',[])
    removed=set()
    for im in images:
        if 'bufferView' not in im:continue
        idx=im.pop('bufferView');removed.add(idx);v=g['bufferViews'][idx];payload=binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']];digest=hashlib.sha256(payload).hexdigest()[:20];ext='png' if im.get('mimeType')=='image/png' else 'jpg';filename=f'{digest}.{ext}';(shared/filename).write_bytes(payload);im['uri']=f'../../textures/shared/{filename}'
    newbin=bytearray(binary)
    for im in images:
        if im.get("uri", "").startswith("/assets/textures/shared/"): im["uri"]="../../textures/shared/"+im["uri"].split("/")[-1]
    if removed:
        newbin=bytearray();newviews=[];mapping={}
        for idx,v in enumerate(g['bufferViews']):
            if idx in removed:continue
            while len(newbin)%4:newbin.append(0)
            offset=len(newbin);newbin.extend(binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]);mapping[idx]=len(newviews);newviews.append({**v,'byteOffset':offset})
        def remap(node):
            if isinstance(node,dict):
                for k,v in node.items():
                    if k=='bufferView':node[k]=mapping[v]
                    else:remap(v)
            elif isinstance(node,list):
                for v in node:remap(v)
        remap(g.get('accessors',[]));g['bufferViews']=newviews;g['buffers'][0]['byteLength']=len(newbin)
        while len(newbin)%4:newbin.append(0)
    encoded=json.dumps(g,separators=(',',':')).encode();encoded+=b' '*((-len(encoded))%4)
    out=struct.pack('<III',0x46546c67,2,12+8+len(encoded)+8+len(newbin))+struct.pack('<II',len(encoded),0x4e4f534a)+encoded+struct.pack('<II',len(newbin),0x004e4942)+newbin;path.write_bytes(out)
    a['textureUris']=sorted({'/assets/textures/shared/'+im['uri'].split('/')[-1] for im in images if 'uri' in im})
    name=Path(a['source']).stem
    a['category']=Path(a['source']).parent.name
    a['role']='Secondary' if name in {'prop_barrel','prop_crate','prop_skiff','prop_cart','prop_market_awning','prop_stone_wall','prop_bush','prop_rock'} else 'Hero'
    a['status']='新增正式模块' if name in {'building_house_c','building_warehouse_b','prop_stone_wall','port_quay','port_street','prop_cart','prop_market_awning','prop_palm_b','prop_rock'} else ('沿用次级' if name in {'prop_barrel','prop_crate','prop_skiff'} else '重制升级')
m['sharedTextures']=sorted({u for a in m['assets'].values() for u in a.get('textureUris',[])})
manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2))
print('Shared textures:',len(m['sharedTextures']),'GLB bytes:',sum((ROOT/('public'+a['url'])).stat().st_size for a in m['assets'].values()))
