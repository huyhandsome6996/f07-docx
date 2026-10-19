const{chromium}=await import('/opt/codex/cua_node/lib/node_modules/playwright/index.mjs');import{readFileSync,writeFileSync}from'node:fs';
const root=process.env.F04_AUDIT_DIR,out=root+'/evidence',base='http://127.0.0.1:8044/api/v1';const{password}=JSON.parse(readFileSync(root+'/.synthetic-credentials.json','utf8'));
async function api(path,{method='GET',token,body}={}){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});const d=await r.json();if(r.status>=400)throw Error(`${path} ${r.status}`);return d;}
async function open(browser,port,code){const ctx=await browser.newContext({viewport:{width:port===5144?1440:390,height:900}}),p=await ctx.newPage();p.setDefaultTimeout(8000);await p.goto(`http://127.0.0.1:${port}/#/login`);await p.locator('#fb-cred-code').fill(code);await p.locator('#fb-cred-password').fill(password);await p.getByRole('button',{name:'Đăng nhập vào không gian',exact:true}).click();await p.waitForURL('**/#/home');await p.evaluate(()=>location.hash='/compose');await p.locator('textarea.fb-compose__textarea').waitFor();return{ctx,p};}
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});const results=[];
try{for(const[label,portA,portB,n]of[['web-stale-save-after-mini',5144,3044,941],['mini-stale-save-after-web',3044,5144,943]]){
 const token=(await api('/auth/class-session',{method:'POST',body:{code:'HS'+n,password}})).token;
 const peer=(await api('/connections',{token})).results[0].other_party_id;
 const draft=await api('/drafts',{method:'POST',token,body:{kind:'text',body:'AUDIT_CONFLICT_BASE_'+label,recipient_id:peer}});
 const a=await open(browser,portA,'HS'+n),b=await open(browser,portB,'HS'+n);
 const oldText='AUDIT_CLIENT_A_UNSAVED_'+label,newText='AUDIT_CLIENT_B_SAVED_'+label;
 await a.p.locator('textarea.fb-compose__textarea').fill(oldText);await b.p.locator('textarea.fb-compose__textarea').fill(newText);
 const waitB=b.p.waitForResponse(r=>r.request().method()==='POST'&&new URL(r.url()).pathname===`/api/v1/drafts/${draft.draft_id}`);await b.p.getByRole('button',{name:'Lưu nháp riêng',exact:true}).click();const responseB=await waitB;const resultB=await responseB.json();
 const waitA=a.p.waitForResponse(r=>r.request().method()==='POST'&&new URL(r.url()).pathname===`/api/v1/drafts/${draft.draft_id}`);await a.p.getByRole('button',{name:'Lưu nháp riêng',exact:true}).click();const responseA=await waitA;const resultA=await responseA.json();
 const final=await api('/drafts/'+draft.draft_id,{token});await a.p.screenshot({path:`${out}/${label}-silent-overwrite.png`,fullPage:true});
 const row={label,initialRevision:draft.revision,otherClientSaveHttp:responseB.status(),otherClientSavedRevision:resultB.revision,staleClientSaveHttp:responseA.status(),staleClientResponseRevision:resultA.revision,finalServerBody:final.body,overwroteOtherClientWithoutConflict:responseA.ok()&&final.body===oldText&&resultB.body===newText};results.push(row);writeFileSync(out+'/cross-client-draft-conflict.json',JSON.stringify(results,null,2));console.log(JSON.stringify(row));await a.ctx.close();await b.ctx.close();
}}finally{await browser.close();}
