import json,sys,re
B={}
for b in ['b08','b09','b10']:
    for x in json.load(open(f'batches/{b}.json')): B[x['handle']]=dict(x,batch=b)
    for p in json.load(open(f'proposals/{b}.json')):
        h=p['handle']
        if p.get('descriptionHtml'): B[h]['cur']=p['descriptionHtml']; B[h]['src']='prop'
        else: B[h]['cur']=B[h]['descriptionHtml']; B[h]['src']='orig'
        B[h]['prop_sp']=p.get('short_pitch')
json.dump(B,open('scratchpad/c5/cur.json','w'),ensure_ascii=False,indent=1)
