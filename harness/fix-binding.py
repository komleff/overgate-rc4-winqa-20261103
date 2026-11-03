import sys,json
from prepare import B,E,S,run
N=B/'source-2343df8';sha='2343df83a3a26ae83bc66d4009dd67a913eeea4e'
manifest=json.loads((N/'.agents/distribution-manifest.json').read_bytes());paths=sorted({x['source'] for x in manifest['files']})
def tree(ref):
 out=run(['git','ls-tree','-r',ref],N).stdout; result={}
 for line in out.splitlines():
  left,p=line.split('\t',1); mode,kind,blob=left.split();result[p]={'mode':mode,'blob':blob}
 return result
a=tree('403f95b8a7fae50957a99c16a211a8ef7217cb22');b=tree(sha)
data={'old_source_sha':'403f95b8a7fae50957a99c16a211a8ef7217cb22','new_source_sha':sha,'source_paths':len(paths),'changed':[{'path':p,'old':a[p],'new':b[p]} for p in paths if a[p]!=b[p]],'unchanged':[p for p in paths if a[p]==b[p]]}
(E/'fix-payload-binding.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print(json.dumps({'source_paths':len(paths),'changed':data['changed']}))
body='## WINDOWS QA → PM / AFFECTED PLAN PREPARED — Windows-QA\n\nОснование нового native run — exact-SHA Windows route уже указан в [опубликованном PM Developer packet](https://github.com/komleff/overgate/pull/12#issuecomment-6611272165): после явного снятия STOP и inventory повторить WB-01 на `2343df83a3a26ae83bc66d4009dd67a913eeea4e` и оставшиеся §5.4. Оба условия выполнены; это не вывод согласия из молчания.\n\nПодготовлены четыре inventory: native fresh/simple+complex (без helpers, затем rollback), и legitimate upgrade двух прерванных E2E403 targets. Перед apply их проверяет тот же target Reviewer; новых source reviews не запускаю. После approval выполню именно этот ограниченный route последовательно, без blind replay Beads/protection. Если PM требуется другой порядок/более узкий remaining scope, вопрос [6611343103](https://github.com/komleff/overgate/pull/12#issuecomment-6611343103) остаётся в канале.\n\nScope correction: installer входит в managed manifest. Across403→2343 изменён **один из75 managed source paths**, scripts/install-overgate.py; остальные74 mode/blob идентичны. Upgrade действительно меняет этот один файл и source binding; full-payload equivalence через fix не заявляется. Нативный повторный no-op проверю только после approved apply2343. Текущий status WB-01fix: NOT RUN до исполнения. Старый403 FAIL остаётся.\n\n— Windows-QA (Codex GPT-6)\n'
(E/'fix-prepared.md').write_text(body,encoding='utf-8');print(run([sys.executable,S/'.claude/tools/publish-pr-comment.py','12','-'],S,label='source-fix-prepared-publish',input=body).stdout)
