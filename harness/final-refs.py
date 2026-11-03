from prepare import E,S,run
run(['gh','pr','list','-R','komleff/overgate-rc4-winqa-20261103','--state','all','--limit','30','--json','number,title,headRefOid,state,isDraft,headRefName,baseRefName,url'],label='test-pr-final-refs')
run(['gh','api','repos/komleff/overgate/compare/403f95b8a7fae50957a99c16a211a8ef7217cb22...de55285687f673f85516e1d173940a6c491010b0'],label='head-delta-403-de552')
run(['git','status','--porcelain'],S,label='source-final-clean')
run(['git','status','--short','--branch'],'D:/GitHub/overgate',label='working-overgate-unchanged')
