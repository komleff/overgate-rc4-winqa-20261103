import json,re,hashlib,shutil
from pathlib import Path
from prepare import B,E,S,SHA,REPO,run
R=B/'evidence-repo'
def sanitize_cli(p):
 events=[]; model=None;mode=None;version=None;calls={};results={};final=None
 for line in p.read_text(encoding='utf-8').splitlines():
  try:x=json.loads(line)
  except ValueError:continue
  typ=x.get('type')
  if typ=='system' and x.get('subtype')=='init':
   selected={k:x.get(k) for k in ['type','subtype','cwd','session_id','model','permissionMode','claude_code_version']}
   events.append(selected);model=x.get('model');mode=x.get('permissionMode');version=x.get('claude_code_version')
  elif typ=='assistant':
   for a in x.get('message',{}).get('content',[]):
    if a.get('type')=='tool_use':
     event={'type':'tool_use','id':a.get('id'),'name':a.get('name'),'input':a.get('input')};events.append(event);calls[a['id']]=event
  elif typ=='user':
   for a in x.get('message',{}).get('content',[]):
    if isinstance(a,dict) and a.get('type')=='tool_result':events.append(a);results[a.get('tool_use_id')]=a
  elif typ=='result':
   final={k:x.get(k) for k in ['type','subtype','is_error','api_error_status','duration_ms','num_turns','result','permission_denials','session_id','modelUsage']};events.append(final)
 out=E/(p.stem+'-receipts.json')
 out.write_text(json.dumps({'source_sha':SHA,'notice':'Only factual runtime init, tool calls/results and final report retained. Internal reasoning and OAuth flow are excluded.','events':events},ensure_ascii=False,indent=2),encoding='utf-8')
 summary={'file':out.name,'model':model,'mode':mode,'cli_version':version,'finished':final is not None,'final':final,'tool_count':len(calls),'errors':[],'commands':[]}
 for i,c in calls.items():
  outcome=results.get(i,{})
  if c['name']=='Bash':summary['commands'].append({'id':i,'command':c['input'].get('command'),'is_error':outcome.get('is_error',False),'output':outcome.get('content')})
  if outcome.get('is_error'):
   txt=str(outcome.get('content',''));summary['errors'].append({'id':i,'tool':c['name'],'input':c['input'],'reason':txt.split("']: ")[-1]})
 return summary
def collect():
 summaries={}
 for p in E.glob('*.jsonl'):
  summary=sanitize_cli(p);summaries[p.stem]=summary
 (E/'runtime-summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2),encoding='utf-8')
 for p in E.iterdir():
  if p.is_file() and p.suffix in {'.json','.txt','.md'}:
   data=p.read_bytes()
   if re.search(rb'(?:sk-ant-|sk-proj-|gh[pousr]_|github_pat_)[A-Za-z0-9_-]{16,}',data):raise RuntimeError('Possible credential marker: '+p.name)
   dest=R/'receipts'/p.name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(data)
 for p in B.glob('*.py'):
  (R/'harness').mkdir(exist_ok=True);shutil.copyfile(p,R/'harness'/p.name)
 for p in B.glob('*prompt*.txt'):
  (R/'harness').mkdir(exist_ok=True);shutil.copyfile(p,R/'harness'/p.name)
 index={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['plans','receipts','harness'] for p in (R/folder).rglob('*') if p.is_file()}
 (R/'SHA256SUMS.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Evidence files',len(index),'CLI sessions',len(summaries),'finished',sum(v['finished'] for v in summaries.values()))
 return summaries
if __name__=='__main__':collect()
