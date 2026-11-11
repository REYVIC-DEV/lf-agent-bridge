import json,pathlib,copy,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[4]))
import lf_api
BASE=pathlib.Path('funnels/sof/scaling-or-failing');F='fun_RoOL_WXDCAxK4hEk0v5xX'
pairs=json.loads((BASE/'edits/slash-logo-replacements-2026-11-06.json').read_text())
pairs=[p for p in pairs if not p[0].startswith(('("s"','"Tazapay"'))]
pairs.append(('aria-label="Sponsor S"','aria-label="Slash"'))
slug='scaling-failing' if '--live' in sys.argv else 'sof-sponsor-test'
f=lf_api.get_funnel_steps('',F);s=next(x for x in f['steps'] if x['slug']==slug)
counts={a:0 for a,b in pairs}
def change(v):
 if isinstance(v,dict):return {k:change(x) for k,x in v.items()}
 if isinstance(v,list):return [change(x) for x in v]
 if isinstance(v,str):
  for a,b in pairs:counts[a]+=v.count(a);v=v.replace(a,b)
 return v
new=change({'body':s['body'],'settings':s['settings']})
for a,n in counts.items():
 if not n:raise RuntimeError('Expected match missing: '+a[:90])
step={k:s[k] for k in ('slug','title','type','visual')};step.update(id=s['uid'],**new)
lf_api.gql('', 'mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}',{'id':F,'node':{'steps':[step]}})
back=next(x for x in lf_api.get_funnel_steps('',F)['steps'] if x['slug']==slug)
assert back['body']==new['body'] and back['settings']==new['settings']
print('Saved and read-back verified:',slug,'replacement counts',list(counts.values()))
