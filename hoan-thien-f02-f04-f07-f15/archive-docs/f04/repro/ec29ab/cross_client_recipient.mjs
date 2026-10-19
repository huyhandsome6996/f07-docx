const {chromium}=await import('/opt/codex/cua_node/lib/node_modules/playwright/index.mjs');
import{readFileSync,writeFileSync}from'node:fs';
const root=process.env.F04_AUDIT_DIR,out=root+'/evidence',base='http://127.0.0.1:8044/api/v1';
const {password}=JSON.parse(readFileSync(root+'/.synthetic-credentials.json','utf8'));
async function api(path,{method='GET',token,body}={}){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});const data=await r.json();if(r.status>=400)throw Error(`${method} ${path}: ${r.status} ${JSON.stringify(data)}`);return data;}
async function login(code){return(await api('/auth/class-session',{method:'POST',body:{code,password}})).token;}
async function open(browser,port,code){const ctx=await browser.newContext({viewport:{width:port===5144?1440:390,height:900}}),p=await ctx.newPage();p.setDefaultTimeout(8000);await p.goto(`http://127.0.0.1:${port}/#/login`);await p.locator('#fb-cred-code').fill(code);await p.locator('#fb-cred-password').fill(password);await p.getByRole('button',{name:'Đăng nhập vào không gian',exact:true}).click();await p.waitForURL('**/#/home');await p.evaluate(()=>location.hash='/compose');await p.locator('textarea.fb-compose__textarea').waitFor();return{ctx,p};}
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});const results=[];
try{
for(const[label,reviewPort,otherPort,n,secondaryN]of[['web-review-mini-edit',5144,3044,941,942],['mini-review-web-edit',3044,5144,943,944]]){
 const author=await login('HS'+n),primary=await login('PH'+n),secondary=await login('PH'+secondaryN);
 const originalPeer=(await api('/connections',{token:author})).results[0].other_party_id;
 const invite=await api('/connections/invites',{method:'POST',token:author,body:{relationship_kind:'backup'}});
 await api('/connections/invites/claim',{method:'POST',token:secondary,body:{code:invite.code}});
 await api(`/connections/invites/${invite.invite_id}/confirm`,{method:'POST',token:author,body:{}});
 const cs=(await api('/connections',{token:author})).results;const other=cs.find(x=>x.other_party_id!==originalPeer);if(!other)throw Error('Missing secondary connection');
 const marker=`AUDIT_CROSS_CLIENT_WRONG_RECIPIENT_${label}`;
 const draft=await api('/drafts',{method:'POST',token:author,body:{kind:'text',body:marker,recipient_id:originalPeer}});
 const a=await open(browser,reviewPort,'HS'+n),b=await open(browser,otherPort,'HS'+n);
 const shownRecipient=await a.p.locator('.fb-compose__recipient-name').textContent().catch(()=>null);
 await b.p.getByRole('button',{name:'Đổi',exact:true}).click();
 const buttons=b.p.locator('.fb-sheet').getByRole('button');
 const labels=await buttons.allTextContents();const secondLabel=other.counterpart?.display_name||'Người hỗ trợ dự phòng';
 await b.p.locator('.fb-sheet').getByRole('button',{name:secondLabel,exact:true}).click();
 const save=b.p.waitForResponse(r=>r.request().method()==='POST'&&new URL(r.url()).pathname===`/api/v1/drafts/${draft.draft_id}`);
 await b.p.getByRole('button',{name:'Lưu nháp riêng',exact:true}).click();await save;
 const updated=await api(`/drafts/${draft.draft_id}`,{token:author});
 const previewWait=a.p.waitForResponse(r=>r.request().method()==='POST'&&r.url().endsWith('/preview'));
 await a.p.getByRole('button',{name:'Xem trước nội dung',exact:true}).click();
 const preview=await(await previewWait).json();await a.p.locator('.fb-compose__preview-body').waitFor();
 const confirm=a.p.getByRole('button',{name:/^Gửi cho /});const confirmLabel=await confirm.textContent();
 await a.p.screenshot({path:`${out}/${label}-wrong-recipient-preview.png`,fullPage:true});
 const confirmResponse=a.p.waitForResponse(r=>r.request().method()==='POST'&&r.url().endsWith('/confirm-send'));
 await confirm.click();const sent=await confirmResponse;await a.p.waitForTimeout(150);
 const primaryRows=(await api('/messages',{token:primary})).results;
 const secondaryRows=(await api('/messages',{token:secondary})).results;
 async function markerMessages(rows,token){const matches=[];for(const row of rows){const d=await api('/messages/'+row.message_id,{token});if(d.body===marker)matches.push(d.message_id);}return matches;}
 const atPrimary=await markerMessages(primaryRows,primary),atSecondary=await markerMessages(secondaryRows,secondary);
 const result={label,shownRecipient,confirmLabel,secondaryChoiceLabel:secondLabel,recipientSheetLabels:labels,localOriginalRecipient:originalPeer,otherClientSavedRecipient:updated.recipient_id,serverPreviewRecipient:preview.recipient_id,serverPreviewRevision:preview.revision,serverPreviewBody:preview.body,confirmHttp:sent.status(),atPrimary,atSecondary,wrongRecipientReceived:atSecondary.length===1&&atPrimary.length===0};
 results.push(result);writeFileSync(out+'/cross-client-recipient.json',JSON.stringify(results,null,2));console.log(JSON.stringify(result));await a.ctx.close();await b.ctx.close();
}
}finally{await browser.close();}
