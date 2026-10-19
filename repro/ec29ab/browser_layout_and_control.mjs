const {chromium}=await import(process.env.F04_PLAYWRIGHT_MODULE || '/opt/codex/cua_node/lib/node_modules/playwright/index.mjs');
import {readFileSync,writeFileSync} from 'node:fs';
const root=process.env.F04_AUDIT_DIR || '/tmp/f04-audit',out=`${root}/evidence`;
const {password}=JSON.parse(readFileSync(`${root}/.synthetic-credentials.json`,'utf8'));
const base='http://127.0.0.1:8044/api/v1';
async function api(path,{method='GET',token,body}={}){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});return{status:r.status,data:await r.json()};}
async function token(code){return(await api('/auth/class-session',{method:'POST',body:{code,password}})).data.token;}
const browser=await chromium.launch({executablePath:process.env.F04_CHROMIUM || '/usr/bin/chromium',headless:true,args:['--no-sandbox']});
const results=[];
for(const [label,port,width] of [['web-1440',5144,1440],['web-390',5144,390],['mini-320',3044,320],['mini-390',3044,390]]){
 const context=await browser.newContext({viewport:{width,height:900}});const page=await context.newPage();
 await page.goto(`http://127.0.0.1:${port}/#/login`);await page.locator('#fb-cred-code').fill('HS941');await page.locator('#fb-cred-password').fill(password);await page.getByRole('button',{name:'Đăng nhập vào không gian',exact:true}).click();await page.waitForURL('**/#/home');await page.evaluate(()=>location.hash='/compose');await page.locator('textarea.fb-compose__textarea').waitFor();await page.waitForTimeout(200);
 const metrics=await page.evaluate(()=>{const rect=s=>{const el=document.querySelector(s);if(!el)return null;const r=el.getBoundingClientRect();return{width:r.width,height:r.height,left:r.left,right:r.right}};return{viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,page:rect('.fb-page'),textarea:rect('textarea.fb-compose__textarea'),grid:rect('.fb-compose-grid'),gridColumns:getComputedStyle(document.querySelector('.fb-compose-grid')).gridTemplateColumns,shellPresent:!!document.querySelector('.fb-shell'),visibleHiddenElements:[...document.querySelectorAll('[hidden]')].filter(e=>getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().width>0).map(e=>({tag:e.tagName,class:e.className,text:e.textContent.slice(0,70)}))}});
 await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${out}/${label}-layout.png`,fullPage:false});
 results.push({label,...metrics});await context.close();
}
// Positive control: after a provider error, deliberately save manual content,
// then preview + explicit confirm; the recipient must receive exactly that body.
{
 const hs=await token('HS945'),ph=await token('PH945');
 for(const t of [hs,ph])for(const[purpose,policy_version]of[['service','service-v1'],['ai_processing','ai-v1']])await api('/consents',{method:'POST',token:t,body:{purpose,policy_version,decision:'accepted'}});
 const proposal=(await api('/classroom/proposals',{token:hs})).data.results[0];
 for(const t of [hs,ph])await api(`/classroom/proposals/${proposal.proposal_id}/confirm`,{method:'POST',token:t,body:{}});
 const peer=(await api('/connections',{token:hs})).data.results[0].other_party_id;
 await api('/drafts',{method:'POST',token:hs,body:{kind:'text',body:'AUDIT_FORCE_OUTAGE synthetic original',recipient_id:peer}});
 const ctx=await browser.newContext({viewport:{width:1440,height:900}}),page=await ctx.newPage();
 await page.goto('http://127.0.0.1:5144/#/login');await page.locator('#fb-cred-code').fill('HS945');await page.locator('#fb-cred-password').fill(password);await page.getByRole('button',{name:'Đăng nhập vào không gian',exact:true}).click();await page.waitForURL('**/#/home');await page.evaluate(()=>location.hash='/compose');
 const textarea=page.locator('textarea.fb-compose__textarea');await textarea.waitFor();
 let aiFailure=null;page.on('response',r=>{if(r.url().endsWith('/ai/refine'))aiFailure=r.status();});
 await page.getByRole('button',{name:'AI gợi ý cách diễn đạt êm ái hơn',exact:true}).click();await page.waitForTimeout(450);
 const afterError=await textarea.inputValue();const manual='AUDIT_MANUAL_FINAL explicitly saved after AI outage';await textarea.fill(manual);
 await page.getByRole('button',{name:'Lưu nháp riêng',exact:true}).click();await page.waitForTimeout(400);
 await page.getByRole('button',{name:'Xem trước nội dung',exact:true}).click();await page.getByRole('button',{name:/^Gửi cho /}).click();await page.waitForTimeout(500);
 const row=(await api('/messages',{token:ph})).data.results[0];const detail=row?(await api(`/messages/${row.message_id}`,{token:ph})).data:null;
 results.push({label:'positive-manual-save-control',aiFailure,draftPreservedOnAiError:afterError.includes('AUDIT_FORCE_OUTAGE'),deliveredMatchesSavedFinal:detail?.body===manual,deliveredBody:detail?.body});await ctx.close();
}
writeFileSync(`${out}/layout-control.json`,JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));await browser.close();
