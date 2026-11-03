import json,re
from pathlib import Path
from prepare import B,E,S,SHA,run
R=B/'evidence-repo'
rows=[]
prslog=(E/'test-pr-final-refs.txt').read_text(encoding='utf-8'); raw=prslog.split('STDOUT:\n',1)[1].split('\nSTDERR:',1)[0];prs=json.loads(raw);bybranch={p['headRefName']:p for p in prs}
for c in json.loads((E/'targets.json').read_text(encoding='utf-8')):
 n=c['name'];native=json.loads((E/(n+'-native-results.json')).read_text(encoding='utf-8'));r={'scenario':n,'source_sha':SHA,'path':c['target'],'install_pr':c['pr'],'plan_sha256':c['plan_sha256'],'target_before_sha':c['target_before_sha'],'native_target_after_sha':native.get('target_after_sha'),'native_results_file':n+'-native-results.json'}
 if c['mode']=='rollback':r['step8']='PASS' if native.get('restored_before_bytes') and native.get('install_state_absent') and native.get('rollback_rc')==0 else 'FAIL'
 else:
  noop=json.loads((E/(n+'-noop-results.json')).read_text(encoding='utf-8'));r['final_target_sha']=noop['target_head'];r['branch']=noop['target_branch'];pr=bybranch.get(r['branch']);r['runtime_pr']=pr.get('url') if pr else None;r['noop']='PASS' if noop['operations_equal'] else 'FAIL';r['noop_mode_only']=all(x['before']['sha256']==x['after']['sha256'] for x in noop['mismatches']);r['noop_mode_mismatches']=len(noop['mismatches']);r['checker_native']='PASS' if native.get('checker_rc')==0 else 'FAIL';r['memory_six_exact']=native['memory_six_exact'];r['beads_rc']=native['beads_rc'];r['protection_rc']=native['protection_rc'];r['live_receipts_file']=n+'-live-2317-receipts.json'
  doc=json.loads((E/r['live_receipts_file']).read_text(encoding='utf-8'));init=next(x for x in doc['events'] if x.get('subtype')=='init');r['runtime_model']=init['model'];r['runtime_mode']=init['permissionMode'];r['runtime_version']=init['claude_code_version'];events=doc['events'];calls={v['id']:v for v in events if v.get('type')=='tool_use'};results={v['tool_use_id']:v for v in events if v.get('type')=='tool_result'}
  r['negative_probe_receipts']=[]
  for id,v in calls.items():
   cmd=v.get('input',{}).get('command','')
   if v['name']=='Bash' and any(x in cmd for x in ['git push origin main','gh pr merge 1','gh pr comment 1','red verification must block']):
    out=results.get(id,{});r['negative_probe_receipts'].append({'id':id,'command':cmd,'is_error':out.get('is_error',False),'hook_intercept':'PreToolUse:Bash hook error:' in str(out.get('content','')),'reason':str(out.get('content','')).split("']: ")[-1]})
  r['step5_live']='PASS' if len(r['negative_probe_receipts'])>=4 and all(v['hook_intercept'] for v in r['negative_probe_receipts']) else 'NOT RUN'
 rows.append(r)
(E/'completed-403-matrix.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps([{k:r.get(k) for k in ['scenario','final_target_sha','runtime_pr','runtime_mode','step5_live','noop','noop_mode_mismatches','step8']} for r in rows],indent=2))
