from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import json,os
ROOT=Path(__file__).resolve().parents[2]
os.chdir(ROOT)
class Handler(SimpleHTTPRequestHandler):
 def do_POST(self):
  if self.path!='/save-benchmark':self.send_error(404);return
  size=int(self.headers.get('Content-Length','0'))
  if size>10000000:self.send_error(413);return
  try:
   data=json.loads(self.rfile.read(size));assert data.get('schema')=='drone-gpu-benchmark-v1'
   target=ROOT/'outputs/milestone-08-browser-results.json'
   if target.exists():
    import time
    target=ROOT/f'outputs/milestone-08-browser-results-{time.time_ns()}.json'
   target.write_text(json.dumps(data,indent=2));self.send_response(200);self.end_headers();self.wfile.write(str(target.name).encode())
  except Exception as e:self.send_error(400,str(e))
ThreadingHTTPServer(('127.0.0.1',8875),Handler).serve_forever()
