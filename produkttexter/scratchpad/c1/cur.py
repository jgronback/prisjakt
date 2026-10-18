import json,sys,os
H='/home/user/prisjakt/produkttexter'
B={n['handle']:n for n in json.load(open(H+'/backup_2026-10-18.json'))}
P={}
for f in sorted(os.listdir(H+'/proposals')):
    for p in json.load(open(H+'/proposals/'+f)):
        if p.get('descriptionHtml'): P[p['id']]=p
def cur(h):
    n=B[h]; p=P.get(n['id'])
    return (p['descriptionHtml'] if p else n['descriptionHtml']), n, p
if __name__=='__main__':
    for h in sys.argv[1:]:
        d,n,p=cur(h)
        print('=====',h,'| title:',n['title'],'| src:', 'proposal' if p else 'backup')
        print(d)
        for k in ('sp','sensor','obj','pitch','lrf','netd','det','forst'):
            print(k, (n.get(k) or {}).get('value') if n.get(k) else None)
        print('faq', (n.get('faq') or {}).get('value') if n.get('faq') else None)
        if p: print('proposal sp:', p.get('short_pitch'))
