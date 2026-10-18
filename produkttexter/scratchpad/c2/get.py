import json,sys,os
H='/home/user/prisjakt/produkttexter'
b={n['handle']:n for n in json.load(open(H+'/backup_2026-10-18.json'))}
props={}
for f in sorted(os.listdir(H+'/proposals')):
    for p in json.load(open(H+'/proposals/'+f)):
        props[p['handle']]=p
def cur(h):
    p=props.get(h)
    if p and p.get('descriptionHtml'): return p['descriptionHtml']
    return b[h]['descriptionHtml']
if __name__=='__main__':
    for h in sys.argv[1:]:
        n=b[h]
        print('#####',h,n['id'],'|',n['title'])
        print({k:(v.get('value') if isinstance(v,dict) else v) for k,v in n.items() if k not in('descriptionHtml','title','handle','id','tags','updatedAt')})
        p=props.get(h,{})
        print('PROPOSAL other keys:',{k:v for k,v in p.items() if k not in('descriptionHtml','id','handle')})
        print(cur(h))
