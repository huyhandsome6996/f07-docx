const{chromium}=await import('/opt/codex/cua_node/lib/node_modules/playwright/index.mjs');
import{readFileSync,writeFileSync}from'node:fs';
import{randomUUID}from'node:crypto';
const root=process.env.F04_AUDIT_DIR,out=root+'/evidence',base='http://127.0.0.1:8044/api/v1';const{password}=JSON.parse(readFileSync(root+'/.synthetic-credentials.json','utf8'));
async function api(path,{method='GET',token,body,key}={}){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`} :{}),...(key?{'X-Idempotency-Key':key}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});const d=await r.json();if(r.status>=400)throw Error(`${method} ${path} ${r.status}`);return d;}
async function login(code){return(await api('/auth/class-session',{method:'POST',body:{code,password}})).token;}
async function open(browser,port,code,messageId){const ctx=await browser.newContext({viewport:{width:port===5144?1440:390,height:900}}),p=await ctx.newPage();p.setDefaultTimeout(8000);await p.goto(`http://127.0.0.1:${port}/#/login`);await p.locator('#fb-cred-code').fill(code);await p.locator('#fb-cred-password').fill(password);await p.getByRole('button',{name:'Đăng nhập vào không gian',exact:true}).click();await p.waitForURL('**/#/home');await p.evaluate(id=>location.hash='/messages/'+id,messageId);await p.locator('textarea.fb-textarea').waitFor();return{ctx,p};}
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});const results=[];
for(const[label,port,prefix,n]of[['web-student',5144,'HS',941],['web-caregiver',5144,'PH',942],['mini-student',3044,'HS',943],['mini-caregiver',3044,'PH',944]]){
 const result={label};results.push(result);let a,b;
 try{
  const actor=await login(prefix+n),peer=await login((prefix==='HS'?'PH':'HS')+n);const peerConnections=(await api('/connections',{token:peer})).results;
  const actorId=(await api('/auth/me',{token:actor})).user_id;
  const other=peerConnections.find(x=>x.other_party_id===actorId);if(!other)throw Error('Pair fixture missing');
  const seed='AUDIT_RECEIVED_FINAL_'+label;
  const message=await api('/messages',{method:'POST',token:peer,key:randomUUID(),body:{kind:'text',recipient_id:actorId,body:seed}});
  a=await open(browser,port,prefix+n,message.message_id);const p=a.p,text=p.locator('textarea.fb-textarea');
  result.receivedFinalVisible=(await p.locator('main').textContent()).includes(seed);
  await p.screenshot({path:`${out}/${label}-state-recipient-final.png`,fullPage:true});
  const original='AUDIT_PRIVATE_REPLY_ORIGINAL_'+label;await text.fill(original);
  await p.getByRole('button',{name:'AI gợi ý cách diễn đạt êm ái hơn',exact:true}).click();await p.getByRole('button',{name:'Dùng gợi ý',exact:true}).click();await p.waitForTimeout(130);
  const approved=await text.inputValue();result.original=original;result.approved=approved;await p.screenshot({path:`${out}/${label}-state-reply-ai.png`,fullPage:true});
  const before=(await api('/messages',{token:peer})).results;result.noSendBeforeExplicit=!(await Promise.all(before.map(r=>api('/messages/'+r.message_id,{token:peer})))).some(r=>r.reply_to===message.message_id);
  const pending=p.waitForResponse(r=>r.request().method()==='POST'&&new URL(r.url()).pathname==='/api/v1/messages');await p.getByRole('button',{name:'Gửi phản hồi',exact:true}).click();const sent=await pending;const sentBody=await sent.json();
  const detail=await api('/messages/'+sentBody.message_id,{token:peer});result.http=sent.status();result.finalMatchesApproval=detail.body===approved;result.originalNotDelivered=detail.body!==original;result.fields=Object.keys(detail);result.replyToMatches=detail.reply_to===message.message_id;
  b=await open(browser,port===5144?3044:5144,(prefix==='HS'?'PH':'HS')+n,sentBody.message_id);await b.p.screenshot({path:`${out}/${label}-state-final-on-other-client.png`,fullPage:true});result.otherClientReadsFinal=(await b.p.locator('main').textContent()).includes(approved);result.result='COMPLETED';
 }catch(e){result.result='INCOMPLETE';result.error=e.message;}finally{if(a)await a.ctx.close();if(b)await b.ctx.close();writeFileSync(out+'/reply-e2e.json',JSON.stringify(results,null,2));console.log(JSON.stringify(result));}
}
await browser.close();
