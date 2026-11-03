import os,sys,subprocess,json,time,hashlib
from pathlib import Path
base=Path(__file__).parent
label,cwd,mode,promptfile=sys.argv[1:5]
env=os.environ.copy()
env['PATH']=str(base/'tools/claude-runtime/node_modules/.bin')+';'+str(base/'tools')+';C:/Program Files/Git/bin;C:/Program Files/Git/usr/bin;'+env['PATH']
env['CLAUDE_CODE_GIT_BASH_PATH']='C:/Program Files/Git/bin/bash.exe'
env['PYTHONUTF8']='1'
cmd=[str(base/'tools/claude-runtime/node_modules/.bin/claude.cmd'),'--permission-mode',mode,'--effort','low','--print','--verbose','--output-format','stream-json','--include-hook-events']
if len(sys.argv)>5:cmd+=['--resume',sys.argv[5]]
prompt_text=Path(promptfile).read_text(encoding='utf-8')
meta={'cwd':cwd,'mode':mode,'command':cmd,'started':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'prompt_file':promptfile,'prompt_text_utf8_sha256':hashlib.sha256(prompt_text.encode('utf-8')).hexdigest()}
(base/'evidence'/f'{label}-invocation.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
with (base/'evidence'/f'{label}.jsonl').open('w',encoding='utf-8') as out, (base/'evidence'/f'{label}.stderr.txt').open('w',encoding='utf-8') as err:
 if label.startswith('literal-b-'):
  p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace',cwd=cwd,env=env)
  p.stdin.write(prompt_text);p.stdin.close()
  for line in p.stdout:
   out.write(line);out.flush()
   try:event=json.loads(line)
   except ValueError:continue
   failures=[v for v in event.get('message',{}).get('content',[]) if isinstance(v,dict) and v.get('type')=='tool_result' and v.get('is_error')] if event.get('type')=='user' else []
   if failures:
    meta['stopped_on_first_tool_error']=True;meta['failed_tool_ids']=[v.get('tool_use_id') for v in failures]
    subprocess.run(['taskkill.exe','/PID',str(p.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    break
  p.wait()
 else:
  p=subprocess.run(cmd,input=prompt_text,text=True,encoding='utf-8',cwd=cwd,env=env,stdout=out,stderr=err)
meta['exit_code']=p.returncode
(base/'evidence'/f'{label}-invocation.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print(json.dumps(meta))
print((base/'evidence'/f'{label}.stderr.txt').read_text(encoding='utf-8')[-2500:])
for line in (base/'evidence'/f'{label}.jsonl').read_text(encoding='utf-8').splitlines():
 try:
  e=json.loads(line)
  if e.get('type')=='result': print(json.dumps({k:e.get(k) for k in ['type','subtype','is_error','api_error_status','session_id','duration_ms','result']},ensure_ascii=True)[:3200])
 except ValueError: pass
sys.exit(p.returncode)
