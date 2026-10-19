const {chromium}=await import(process.env.F04_PLAYWRIGHT_MODULE || '/opt/codex/cua_node/lib/node_modules/playwright/index.mjs');
import {readFileSync,writeFileSync} from 'node:fs';
const root=process.env.F04_AUDIT_DIR || '/tmp/f04-audit',out=`${root}/evidence`,base='http://127.0.0.1:8044/api/v1';
const {password}=JSON.parse(readFileSync(`${root}/.synthetic-credentials.json`,'utf8'));
async function api(path,{method='GET',token,body}={}){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});return{status:r.status,data:await r.json()};}
async function login(code){return(await api('/auth/class-session',{method:'POST',body:{code,password}})).data.token;}
const browser=await chromium.launch({executablePath:process.env.F04_CHROMIUM || '/usr/bin/chromium',headless:true,args:['--no-sandbox']});const results=[];
for(const [label,port,n] of [['web',5144,941],['mini',3044,943]]){
 const author=await login(`HS${n}`),recipient=await login(`PH${n}`);const peer=(await api('/connections',{token:author})).data.results[0].other_party_id;
 const saved=`AUDIT_SAVED_BEFORE_PREVIEW_${label}`,reviewed=`AUDIT_EDITED_DURING_PREVIEW_${label}`;
 await api('/drafts',{method:'POST',token:author,body:{kind:'text',body:saved,recipient_id:peer}});
 const ctx=await browser.newContext({viewport:{width:label==='web'?1440:390,height:900}}),page=await ctx.newPage();
 await page.goto(`http://127.0.0.1:${port}/#/login`);await page.locator('#fb-cred-code').fill(`HS${n}`);await page.locator('#fb-cred-password').fill(password);await page.getByRole('button',{name:'Đăng nhập vào không gian',exact:true}).click();await page.waitForURL('**/#/home');await page.evaluate(()=>location.hash='/compose');
 const textarea=page.locator('textarea.fb-compose__textarea');await textarea.waitFor();let held=null;
 await page.route('**/api/v1/drafts/*/preview',route=>{held=route;});
 await page.getByRole('button',{name:'Xem trước nội dung',exact:true}).click();
 for(let i=0;i<100&&!held;i++)await page.waitForTimeout(30);if(!held)throw Error('preview not intercepted');
 const editable=await textarea.isEditable();if(editable)await textarea.fill(reviewed);
 await held.continue();await page.locator('.fb-compose__preview-body').waitFor();
 const previewText=await page.locator('.fb-compose__preview-body').innerText();await page.screenshot({path:`${out}/${label}-preview-inflight-race.png`,fullPage:true});
 await page.getByRole('button',{name:/^Gửi cho /}).click();await page.waitForTimeout(450);
 const row=(await api('/messages',{token:recipient})).data.results[0];const delivered=row?(await api(`/messages/${row.message_id}`,{token:recipient})).data.body:null;
 results.push({label,editableDuringPreview:editable,saved,reviewed,previewText,delivered,finalMatchesPreview:delivered===previewText});await ctx.close();
}
await browser.close();writeFileSync(`${out}/preview-race.json`,JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));
