"""Same-process local HTTP + installed Chromium validation, no deployment."""
import functools, hashlib, http.server, json, pathlib, threading, time
from playwright.sync_api import sync_playwright

BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parent
OUT=BASE/'raw'/'viewer_qa'
OUT.mkdir(parents=True,exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

handler=functools.partial(Handler,directory=str(ROOT))
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/demo/index.html'
report={'flow':'Load actual saved-state replay, select every record, inspect recorded end, play/seek, toggle overlays, reset camera, and inspect desktop/mobile.',
        'browser':'Installed Chromium on dot cloud execution computer, controlled by Python Playwright.',
        'fallback_reason':'Cua cloud-browser localhost navigation and cross-call shell check returned ERR_CONNECTION_REFUSED; same-process HTTP server is reachable.',
        'url':url,'checks':[],'console':[],'page_errors':[],'network_failures':[],'screenshots':[]}
try:
  with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    page.on('console',lambda m:report['console'].append({'type':m.type,'text':m.text}))
    page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
    page.on('requestfailed',lambda r:report['network_failures'].append({'url':r.url,'error':r.failure}))
    page.goto(url,wait_until='networkidle')
    page.wait_for_selector('main[aria-busy="false"]',timeout=20000)
    report['title']=page.title()
    report['body_text']=page.locator('body').inner_text()
    report['checks'].append({'id':'identity','pass':'Wake approximation evidence' in report['title']})
    report['checks'].append({'id':'canvas','pass':page.locator('canvas').count()==1})
    report['checks'].append({'id':'load_error_hidden','pass':not page.locator('#load-error').is_visible()})
    report['replay_evidence']=page.evaluate('window.replayEvidence')
    page.screenshot(path=str(OUT/'desktop_initial.png'),full_page=True);report['screenshots'].append('desktop_initial.png')
    index=json.loads((ROOT/'results/boids/index.json').read_text())
    options=page.locator('#trial option').all_text_contents();report['options']=options
    runs=[]
    for i,rid in enumerate(options):
      page.locator('#trial').select_option(str(i));page.locator('#outcome').click()
      data=json.loads((ROOT/'results/boids'/f'{rid}.json').read_text())
      observed={'id':rid,'clock':page.locator('#clock').inner_text(),'badge':page.locator('#badge').inner_text(),
                'status':page.locator('#status').inner_text(),'raw_href':page.locator('#raw').get_attribute('href')}
      observed['pass']=observed['clock']==f"{data['metrics']['end']:.3f} s" and observed['raw_href'].endswith(f'{rid}.json')
      runs.append(observed)
    report['record_selections']=runs
    pruned=next(i for i,x in enumerate(options) if x.endswith('-pruned'))
    page.locator('#trial').select_option(str(pruned));page.locator('#frame').press('Home')
    before=page.locator('#clock').inner_text();page.locator('#play').click();page.wait_for_timeout(700);page.locator('#play').click()
    after=page.locator('#clock').inner_text();report['checks'].append({'id':'play_advances','before':before,'after':after,'pass':before!=after})
    page.locator('#frame').press('End');report['checks'].append({'id':'seek_end','pass':page.locator('#clock').inner_text()=='1.000 s'})
    for cid in ['wakes','trails','overlay']:
      page.locator('#'+cid).uncheck();unchecked=not page.locator('#'+cid).is_checked()
      page.locator('#'+cid).check();checked=page.locator('#'+cid).is_checked()
      report['checks'].append({'id':cid+'_toggle','pass':unchecked and checked})
    page.locator('#camera').click();page.screenshot(path=str(OUT/'desktop_pruned_end.png'),full_page=True);report['screenshots'].append('desktop_pruned_end.png')
    page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(100)
    dims=page.evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth})')
    report['checks'].append({'id':'mobile_no_horizontal_overflow','pass':dims['scrollWidth']<=dims['width'],'dimensions':dims})
    page.screenshot(path=str(OUT/'mobile.png'),full_page=True);report['screenshots'].append('mobile.png')
    report['checks'].append({'id':'runtime_errors','pass':not report['page_errors']})
    browser.close()
except Exception as e:
  report['blocker']=str(e)
finally:
  server.shutdown();server.server_close()
  report['source_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'demo/index.html',ROOT/'demo/app.js',ROOT/'results/boids/index.json']}
  (OUT/'report.json').write_text(json.dumps(report,indent=2))
  print(json.dumps({k:v for k,v in report.items() if k not in ['body_text','console']},indent=2))
