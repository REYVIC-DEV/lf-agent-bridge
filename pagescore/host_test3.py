import sys, json, os
sys.path.insert(0, '.')
import lf_api
CACHE = os.path.join(os.path.dirname(__file__), ".cache")
tok=open('.session_token').read().strip()
ACCT=open('.lf_account').read().strip()
HH={"account-id":ACCT,"version":"1","Origin":"https://app.lightfunnels.com","Referer":"https://app.lightfunnels.com/"}
D="/private/tmp/claude-501/-Users-randellbenedictcalilung-lf-agent-bridge/4f1bca35-d49f-4c0f-8d74-25bbe125fe3c/scratchpad/test3_hosted"
jobs=[("hero","hero.png","image/png"),("editorial","editorial.png","image/png"),
      ("prod1","prod1.png","image/png"),("prod2","prod2.png","image/png"),
      ("prod3","prod3.png","image/png"),("prod4","prod4.png","image/png"),
      ("prod5","prod5.png","image/png"),("launch","launch.gif","image/gif")]
m={}
for key,fn,ct in jobs:
    rec=lf_api.upload_local_image(tok, os.path.join(D,fn), extra_headers=HH, content_type=ct)
    m[key]=rec
    print("hosted",key,"->",rec["src"][:60])
# reuse cached logo + trustpilot images
logo=json.load(open(os.path.join(CACHE, "hlth_img_map.json")))["logo"]
t2=json.load(open(os.path.join(CACHE, "test2_img_map.json")))
m["logo"]=logo; m["tp_logo"]=t2["tp_logo"]; m["tp_small"]=t2["tp_small"]
json.dump(m, open("/tmp/test3_img_map.json","w"))
json.dump(m, open(os.path.join(CACHE, "test3_img_map.json"),"w"))
print("saved test3_img_map.json keys:", list(m.keys()))
