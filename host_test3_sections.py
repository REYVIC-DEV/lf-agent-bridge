import json, os, lf_api
tok=open('.session_token').read().strip()
ACCT=open('.lf_account').read().strip()
HH={"account-id":ACCT,"version":"1","Origin":"https://app.lightfunnels.com","Referer":"https://app.lightfunnels.com/"}
D="/private/tmp/claude-501/-Users-randellbenedictcalilung-lf-agent-bridge/4f1bca35-d49f-4c0f-8d74-25bbe125fe3c/scratchpad/test3_hosted"
jobs=[("sec1","sec1.png","image/png"),("sec2","sec2.png","image/png"),("sec3","sec3.png","image/png"),
      ("sec4","sec4.png","image/png"),("sec5","sec5.png","image/png"),("sec6","sec6.jpg","image/jpeg")]
m=json.load(open("/tmp/test3_img_map.json"))
for key,fn,ct in jobs:
    rec=lf_api.upload_local_image(tok, os.path.join(D,fn), extra_headers=HH, content_type=ct)
    m[key]=rec
    print("hosted",key)
json.dump(m, open("/tmp/test3_img_map.json","w"))
json.dump(m, open(".cache/test3_img_map.json","w"))
print("map keys:", list(m.keys()))
