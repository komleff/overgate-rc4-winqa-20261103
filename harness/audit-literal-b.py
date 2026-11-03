import sys,json,hashlib,re
from pathlib import Path
from prepare import B,E,run
SHA='2343df83a3a26ae83bc66d4009dd67a913eeea4e';S=B/'source-2343df8'
def fingerprint(p):return {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':p.stat().st_mode&0o777} if p.is_file() else None
def audit(name,stage):
 c=next(x for x in json.loads((E/'literal-b-targets.json').read_text(encoding='utf-8')) if x['name']==name);t=Path(c['target']);r={'case':name,'stage':stage,'source_sha':SHA,'target':str(t),'repo':c['repo'],'pr':c['pr']};checks={}
 state=json.loads((t/'.overgate/install-state.json').read_bytes());r['state']={k:state.get(k) for k in ['format','source_sha','mode','beads']};checks['exact_source_mode_strict_beads']=state.get('source_sha')==SHA and state.get('mode')==c['state_mode'] and state.get('beads') is c['beads']
 settings=json.loads((t/'.claude/settings.json').read_bytes());checks['default_mode']=settings['permissions']['defaultMode']==c['runtime_mode']
 checks['memory_six_exact']=len(list((t/'.memory-bank').glob('*.md')))==6 and all((t/'.memory-bank'/p.name).read_bytes()==p.read_bytes() for p in (t/'.agents/templates/memory-bank').glob('*.md'))
 checks['project_verify']=run(['C:/Program Files/Git/bin/bash.exe','.agents/project/verify.sh'],t,label=name+'-'+stage+'-project-verify',ok=False).returncode==0
 checks['checker']=run([sys.executable,S/'scripts/check-reference.py','--root',t],label=name+'-'+stage+'-checker',ok=False).returncode==0
 pfile=E/(name+'-'+stage+'-noop-plan.json');args=[sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',SHA,'--target',t,'--contract',c['contract'],'--target-pr',c['pr'],'--output',pfile]
 if c['mode']=='no-beads':args+=['--no-beads']
 if c['mode']=='bypass':args+=['--mode','bypass']
 p=run(args,label=name+'-'+stage+'-noop',ok=False);v=json.loads(pfile.read_bytes()) if p.returncode==0 else None;checks['noop']=v is not None and not v['conflicts'] and all(x['before']==x['after'] for x in v['operations']);r['noop_operations']=len(v['operations']) if v else None
 refs=run(['git','ls-remote','--heads','origin'],t,label=name+'-'+stage+'-remote-refs').stdout;refs={line.split()[1]:line.split()[0] for line in refs.splitlines()};r['remote_refs']=refs
 if c['beads']:
  ready=run(['bd','--sandbox','ready','--json'],t,label=name+'-'+stage+'-bd-ready',ok=False)
  try:checks['bd_ready']=ready.returncode==0 and isinstance(json.loads(ready.stdout),list)
  except ValueError:checks['bd_ready']=False
  r['backup_sha']=refs.get('refs/heads/beads-backup');checks['first_backup_present']=bool(r['backup_sha']);meta=json.loads((t/'.beads/metadata.json').read_bytes());checks['embedded_database']=meta.get('dolt_mode')=='embedded'
 else:
  manifest=json.loads((S/'.agents/distribution-manifest.json').read_bytes());checks['no_beads_payload_or_db']=not (t/'.beads').exists() and all(not (t/x['target']).exists() for x in manifest['files'] if x.get('component')=='beads');checks['no_backup']=not refs.get('refs/heads/beads-backup');r['bd_ready']='SKIPPED --no-beads'
 prot=json.loads(run(['gh','api','repos/'+c['repo']+'/branches/main/protection'],t,label=name+'-'+stage+'-protection').stdout);checks['protection']=prot['enforce_admins']['enabled'] is True and prot.get('required_pull_request_reviews') is not None and prot['allow_force_pushes']['enabled'] is False and prot['allow_deletions']['enabled'] is False
 # Explicit component binding to the corresponding original A runtime case.
 oldcase=c['path_class']+'-'+c['mode'];old=next(x for x in json.loads((E/'targets.json').read_text(encoding='utf-8')) if x['name']==oldcase);oldroot=Path(old['target']);manifest=json.loads((S/'.agents/distribution-manifest.json').read_bytes());paths=sorted({x['target'] for x in manifest['files'] if (c['beads'] or x.get('component')!='beads') and (x['target'].startswith(('.claude/hooks/','.claude/tools/')) or x['target'] in {'.claude/settings.json','.codex/hooks.json'})})
 binding={'baseline_source_sha':'403f95b8a7fae50957a99c16a211a8ef7217cb22','new_source_sha':SHA,'baseline_case':oldcase,'old_path':str(oldroot),'new_path':str(t),'path_class':c['path_class'],'mode':c['runtime_mode'],'files':[{'path':p,'A':fingerprint(oldroot/p),'B':fingerprint(t/p)} for p in paths]}
 binding['all_bytes_observed_modes_equal']=all(x['A'] is not None and x['A']==x['B'] for x in binding['files']);binding['no_local_settings_overrides']=not (oldroot/'.claude/settings.local.json').exists() and not (t/'.claude/settings.local.json').exists()
 base=json.loads((E/'completed-403-matrix.json').read_text(encoding='utf-8'));row=next(x for x in base if x['scenario']==oldcase);binding['A_actual_hook_receipts']=row['negative_probe_receipts'];binding['A_runtime_version']=row['runtime_version'];binding['A_effective_mode']=row['runtime_mode'];primitives=['git push origin main','gh pr merge 1','gh pr comment 1 --body "ready to merge"','git commit -m "qa: red verification must block"'];binding['command_primitives']=[{'text':x,'sha256':hashlib.sha256(x.encode()).hexdigest(),'present_in_A_actual_tool_input':any(x in y['command'] and y['hook_intercept'] for y in row['negative_probe_receipts'])} for x in primitives]
 binding['command_mapping_note']='A actual tool inputs remain A. Primitive command bytes are unchanged; complex A cd prefixes carry the old literal root and are not relabelled as B tool calls. Same simple/space+Cyrillic path class, relative installed dispatcher and same command grammar. Project-owned green verifier is checked anew on B, not claimed byte-identical to A.'
 init=None
 live=E/(name+'-worker.jsonl')
 if live.exists():
  for line in live.read_text(encoding='utf-8').splitlines():
   try:x=json.loads(line)
   except ValueError:continue
   if x.get('type')=='system' and x.get('subtype')=='init':init={k:x.get(k) for k in ['model','permissionMode','claude_code_version','cwd']};break
 r['runtime_init']=init;checks['actual_runtime_mode']=init is not None and init['permissionMode']==c['runtime_mode'] and init['claude_code_version']==binding['A_runtime_version'];binding['B_runtime_init']=init;binding['reuse_4_5_6_supported']=binding['all_bytes_observed_modes_equal'] and binding['no_local_settings_overrides'] and checks['actual_runtime_mode'] and all(x['present_in_A_actual_tool_input'] for x in binding['command_primitives']);checks['A_runtime_reuse_binding']=binding['reuse_4_5_6_supported']
 (E/(name+'-A-B-runtime-binding.json')).write_text(json.dumps(binding,ensure_ascii=False,indent=2),encoding='utf-8')
 r['head']=run(['git','rev-parse','HEAD'],t,label=name+'-'+stage+'-head').stdout.strip();r['branch']=run(['git','branch','--show-current'],t).stdout.strip();checks['working_branch']=r['branch']=='install/overgate-b'
 if stage=='final':
  status=run(['git','status','--porcelain'],t,label=name+'-final-status');index=run(['git','diff','--cached','--name-status'],t,label=name+'-final-index');checks['clean']=not status.stdout and status.returncode==0;checks['index_empty']=not index.stdout and index.returncode==0;checks['remote_head']=refs.get('refs/heads/'+r['branch'])==r['head'];pr=json.loads(run(['gh','pr','view','1','--json','url,state,isDraft,headRefOid'],t,label=name+'-final-pr').stdout);r['pr_readback']=pr;checks['draft_pr_head']=pr['isDraft'] is True and pr['state']=='OPEN' and pr['headRefOid']==r['head']
 r['checks']=checks;r['result']='PASS' if all(checks.values()) else 'FAIL';(E/(name+'-'+stage+'-audit.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r,ensure_ascii=True));return 0 if r['result']=='PASS' else 1
if __name__=='__main__':sys.exit(audit(*sys.argv[1:]))
