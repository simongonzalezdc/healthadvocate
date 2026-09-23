#!/usr/bin/env python3
"""Champion playground — one-file loopback chat page for the CEO.

Serves a dark chat UI at http://127.0.0.1:8936 and proxies /api/chat to the
champion lane (127.0.0.1:11434 -> nucbox Qwen3.8-27B via the self-healing
launchd tunnel). Loopback-only; synthetic/test content; single request at a
time (champion is single-slot).
"""
import json
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "http://127.0.0.1:11434/v1/chat/completions"
MODEL = "Qwen3.8-27B"

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Champion — Qwen3.8-27B</title>
<style>
:root{color-scheme:dark}
body{background:#0b0e14;color:#d7dce6;font:15px/1.5 -apple-system,sans-serif;margin:0;display:flex;flex-direction:column;height:100vh}
header{padding:14px 20px;border-bottom:1px solid #1d2330;font-weight:600}
header span{color:#4ade80;font-size:12px;margin-left:10px}
#badge{font-size:12px;font-weight:600;padding:3px 10px;border-radius:12px;margin-left:10px}
.bad-live{background:#0e2a1c;color:#4ade80;border:1px solid #14532d}
.bad-down{background:#2a0e0e;color:#f87171;border:1px solid #7f1d1d}
#chat{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:12px}
.msg{max-width:78%;padding:10px 14px;border-radius:12px;white-space:pre-wrap}
.you{align-self:flex-end;background:#1e3a5f}
.bot{align-self:flex-start;background:#161b26;border:1px solid #1d2330}
form{display:flex;gap:8px;padding:14px 20px;border-top:1px solid #1d2330}
input{flex:1;background:#11151f;color:#d7dce6;border:1px solid #2a3142;border-radius:10px;padding:10px 12px;font-size:15px}
button{background:#2563eb;color:#fff;border:0;border-radius:10px;padding:10px 18px;font-size:15px;cursor:pointer}
#status{font-size:12px;color:#8b93a7;padding:0 20px 8px}
</style></head><body>
<header>Champion lane <span>Qwen3.8-27B @ nucbox</span><span id="badge" class="bad-down">checking…</span></header>
<div id="chat"></div>
<div id="status"></div>
<form onsubmit="return send(event)"><input id="q" placeholder="Ask the champion anything…" autofocus><button>Send</button></form>
<script>
const chat=document.getElementById('chat'),statusEl=document.getElementById('status'),badge=document.getElementById('badge');
function add(t,cls){const d=document.createElement('div');d.className='msg '+cls;d.textContent=t;chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}
async function checkUp(){
  try{
    const c=new AbortController();const t=setTimeout(()=>c.abort(),5000);
    const r=await fetch('/api/models',{signal:c.signal});clearTimeout(t);
    const j=await r.json();const ok=j&&j.data&&j.data.length;
    badge.textContent=ok?('LIVE \u2014 '+j.data[0].id):'UPSTREAM EMPTY';
    badge.className=ok?'bad-live':'bad-down';
  }catch(e){
    badge.textContent='DOWN \u2014 tunnel/engine broken';
    badge.className='bad-down';
  }
}
async function send(e){
  e.preventDefault();
  const q=document.getElementById('q');
  const text=q.value.trim();
  if(!text)return false;
  q.value='';add(text,'you');
  const b=add('\u2026','bot');
  statusEl.textContent='champion is thinking (single-slot \u2014 one at a time)\u2026';
  try{
    const c=new AbortController();const t=setTimeout(()=>c.abort(),120000);
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text}),signal:c.signal});
    clearTimeout(t);
    const j=await r.json();
    b.textContent=j.reply||(j.error?('\u26a0 '+j.error):'(empty reply)');
    statusEl.textContent=j.took?('answered in '+j.took):'';
  }catch(err){
    b.textContent='\u26a0 request failed: '+(err.name==='AbortError'?'timed out after 120s':err)+'. If the badge says DOWN, the tunnel is broken.';
    statusEl.textContent='';
  }
  return false;
}
add('Champion is live. This page runs on your Mac and talks to the nucbox engine over the tunnel.','bot');
checkUp();setInterval(checkUp,10000);
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html")
        elif self.path == "/api/models":
            try:
                with urllib.request.urlopen("http://127.0.0.1:11434/v1/models", timeout=8) as r:
                    self._send(200, r.read())
            except Exception as exc:
                self._send(502, json.dumps({"error": f"tunnel upstream down: {exc}"}))
        else:
            self._send(404, '{"error":"not found"}')

    def do_POST(self):
        if self.path != "/api/chat":
            self._send(404, '{"error":"not found"}')
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            message = json.loads(self.rfile.read(length) or b"{}").get("message", "")
        except Exception:
            self._send(400, '{"error":"bad request"}')
            return
        payload = json.dumps({
            "model": MODEL,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 500,
            "temperature": 0.6,
        }).encode()
        req = urllib.request.Request(UPSTREAM, data=payload, headers={"Content-Type": "application/json"})
        import time
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                out = json.load(r)
            reply = out["choices"][0]["message"].get("content", "").strip()
            self._send(200, json.dumps({"reply": reply, "took": f"{round(time.time()-t0,1)}s"}))
        except Exception as exc:
            self._send(502, json.dumps({"error": f"upstream failed: {exc}"}))

    def log_message(self, *_):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8936), Handler).serve_forever()
