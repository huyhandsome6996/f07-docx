const {chromium}=await import(process.env.F04_PLAYWRIGHT_MODULE || '/opt/codex/cua_node/lib/node_modules/playwright/index.mjs');
import {readFileSync,writeFileSync} from 'node:fs';
const root=process.env.F04_AUDIT_DIR || '/tmp/f04-audit',out=`${root}/evidence`;
const {password}=JSON.parse(readFileSync(`${root}/.synthetic-credentials.json`,'utf8'));
const base='http://127.0.0.1:8044/api/v1';
async function api(path,{method='GET',token,body}={}){
 const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});
 const data=await r.json();return {status:r.status,data};
}
async function login(code){const r=await api('/auth/class-session',{method:'POST',body:{code,password}});if(r.status!==200)throw Error(`Synthetic login status ${r.status}`);return r.data.token;}
async function consent(token){for(const [purpose,policy_version] of [['service','service-v1'],['ai_processing','ai-v1']]){const r=await api('/consents',{method:'POST',token,body:{purpose,policy_version,decision:'accepted'}});if(r.status>201)throw Error(`Consent ${r.status}`);}}
const browser=await chromium.launch({executablePath:process.env.F04_CHROMIUM || '/usr/bin/chromium',headless:true,args:['--no-sandbox']});
const results=[];
for(const [label,port,n,prefix,width] of [['web-student',5144,941,'HS',1440],['web-caregiver',5144,942,'PH',1440],['mini-student',3044,943,'HS',390],['mini-caregiver',3044,944,'PH',390]]){
 const hs=await login(`HS${n}`),ph=await login(`PH${n}`);await consent(hs);await consent(ph);
 let r=await api('/classroom/proposals',{token:hs});const proposal=r.data.results[0];
 if(proposal.status==='proposed')for(const token of [hs,ph]){r=await api(`/classroom/proposals/${proposal.proposal_id}/confirm`,{method:'POST',token,body:{}});if(r.status!==200)throw Error(`Proposal ${r.status}`);}
 const author=prefix==='HS'?hs:ph,recipient=prefix==='HS'?ph:hs;
 r=await api('/connections',{token:author});const peer=r.data.results[0].other_party_id;
 const original=`AUDIT_ORIGINAL_PRIVATE_${label}: lời cũ chưa được duyệt gửi.`;
 r=await api('/drafts',{method:'POST',token:author,body:{kind:'text',body:original,recipient_id:peer}});
 if(r.status!==201)throw Error(`Create draft ${r.status}`);const draftId=r.data.draft_id;
 const context=await browser.newContext({viewport:{width,height:900}});const page=await context.newPage();const calls=[],pageErrors=[];
 page.on('request',r=>{if(r.url().includes('/api/v1/'))calls.push({method:r.method(),path:new URL(r.url()).pathname});});
 page.on('pageerror',e=>pageErrors.push(e.message));
 await page.goto(`http://127.0.0.1:${port}/#/login`);await page.locator('#fb-cred-code').fill(`${prefix}${n}`);await page.locator('#fb-cred-password').fill(password);
 await page.getByRole('button',{name:'Đăng nhập vào không gian',exact:true}).click();await page.waitForURL('**/#/home');
 await page.evaluate(()=>location.hash='/compose');
 const text=page.locator('textarea.fb-compose__textarea');await text.waitFor();
 await page.getByRole('button',{name:'AI gợi ý cách diễn đạt êm ái hơn',exact:true}).click();
 await page.getByRole('button',{name:'Dùng gợi ý',exact:true}).click();
 await page.waitForTimeout(350);
 const approved=await text.inputValue();
 const before=(await api('/messages',{token:recipient})).data.results.length;
 await page.screenshot({path:`${out}/${label}-applied.png`,fullPage:true});
 await page.getByRole('button',{name:'Xem trước nội dung',exact:true}).click();
 const preview=page.locator('.fb-compose__preview-body');await preview.waitFor();const previewText=await preview.innerText();
 const storedBefore=(await api(`/drafts/${draftId}`,{token:author})).data.body;
 await page.screenshot({path:`${out}/${label}-preview.png`,fullPage:true});
 await page.getByRole('button',{name:/^Gửi cho /}).click();await page.waitForTimeout(550);
 r=await api('/messages',{token:recipient});const rows=r.data.results;
 let detail=null;if(rows.length>before)detail=(await api(`/messages/${rows[0].message_id}`,{token:recipient})).data;
 const suggestions=(await api('/ai/suggestions',{token:author})).data.results;
 const foreign=suggestions[0]?(await api(`/ai/suggestions/${suggestions[0].suggestion_id}`,{token:recipient})).status:null;
 results.push({label,provider:'LOCAL_SYNTHETIC_PROVIDER; NOT live Gemini',original,approved,previewText,storedBefore,deliveredBody:detail?.body??null,finalMatchesApproval:detail?.body===approved,originalReachedRecipient:detail?.body===original,messagesBeforeExplicitConfirm:before,messagesAfterConfirm:rows.length,foreignSuggestionStatus:foreign,recipientDetailFields:detail?Object.keys(detail):[],pageErrors,calls});
 writeFileSync(`${out}/browser-e2e.json`,JSON.stringify(results,null,2));
 console.log(JSON.stringify(results.at(-1)));
 await context.close();
}
await browser.close();
