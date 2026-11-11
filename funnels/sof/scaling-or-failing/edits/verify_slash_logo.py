import pathlib,json,sys
from playwright.sync_api import sync_playwright
slug=sys.argv[1] if len(sys.argv)>1 else 'sof-sponsor-test'
out=pathlib.Path('funnels/sof/scaling-or-failing/assets/slash-2026-11-06')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='C:/Users/Joshua Reyes/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe')
 for width in (1440,390):
  page=b.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
  page.goto('https://www.scalingorfailing.com/event/'+slug+'?preview=true&slash=20261106',wait_until='networkidle',timeout=90000)
  page.wait_for_timeout(1500)
  assert page.locator('#sof-logo-s image').count()==1,'new logo asset missing'
  logo=page.locator('.sof-splate--s svg');logo.scroll_into_view_if_needed()
  page.wait_for_timeout(1800);box=logo.bounding_box();assert box['width']>70 and box['width']/box['height']>2.8,box
  page.locator('.sof-sponsors').screenshot(path=str(out/(slug+'-'+str(width)+'.png')))
  print(slug,width,'sponsor cross',box['width'],box['height'],'marquee',page.locator('.sof-marq-logo--s').first.bounding_box())
  page.close()
 b.close()

