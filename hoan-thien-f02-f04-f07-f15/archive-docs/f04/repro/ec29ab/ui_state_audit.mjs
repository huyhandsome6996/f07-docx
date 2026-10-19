const{chromium}=await import('/opt/codex/cua_node/lib/node_modules/playwright/index.mjs');
import{readFileSync,writeFileSync}from'node:fs';
const root=process.env.F04_AUDIT_DIR,out=root+'/evidence',base='http://127.0.0.1:8044/api/v1';
const{password}=JSON.parse(readFileSync(root+'/.synthetic-credentials.json','utf8'));
async function api(path,{method='GET',token,body}={}){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});const d=await r.json();if(r.status>=400)throw Error(`${method} ${path} status ${r.status}`);return d;}
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});const results=[];
for(const[label,port,prefix,n,width]of[['web-student',5144,'HS',941,1440],['web-caregiver',5144,'PH',942,1440],['mini-student',3044,'HS',943,390],['mini-caregiver',3044,'PH',944,390]]){
 const row={label,states:{}};results.push(row);let ctx;
 try{
  const token=(await api('/auth/class-session',{method:'POST',body:{code:prefix+n,password}})).token;
  await api('/consents',{method:'POST',token,body:{purpose:'ai_processing',policy_version:'ai-v1',decision:'declined'}});
  const peer=(await api('/connections',{token})).results[0].other_party_id;
  const marker='AUDIT_UI_STATE_'+label;
  const draft=await api('/drafts',{method:'POST',token,body:{kind:'text',body:marker,recipient_id:peer}});
  ctx=await browser.newContext({viewport:{width,height:900}});const page=await ctx.newPage();page.setDefaultTimeout(8000);let refinements=0;
  page.on('request',r=>{if(r.url().endsWith('/ai/refine'))refinements++;});
  await page.goto(`http://127.0.0.1:${port}/#/login`);await page.locator('#fb-cred-code').fill(prefix+n);await page.locator('#fb-cred-password').fill(password);await page.getByRole('button',{name:'Đăng nhập vào không gian',exact:true}).click();await page.waitForURL('**/#/home');await page.evaluate(()=>location.hash='/compose');
  const text=page.locator('textarea.fb-compose__textarea');await text.waitFor();row.states.compose={label:await text.getAttribute('aria-label'),placeholder:await text.getAttribute('placeholder'),body:await text.inputValue()};
  const shot=async state=>{await page.screenshot({path:`${out}/${label}-state-${state}.png`,fullPage:true});};await page.evaluate(()=>scrollTo(0,0));await shot('compose');
  const ai=page.getByRole('button',{name:'AI gợi ý cách diễn đạt êm ái hơn',exact:true});await ai.click();await page.getByRole('button',{name:'Đồng ý và tạo gợi ý',exact:true}).waitFor();
  const consentText=await page.locator('.fb-sheet').innerText();row.states.consent={mentionsGemini:/Gemini/.test(consentText),refineCallsBeforeAgree:refinements};await shot('consent');
  await page.getByRole('button',{name:port===5144?'Tiếp tục viết tay':'Viết tay thôi',exact:true}).click();row.states.decline={refineCalls:refinements,bodyPreserved:await text.inputValue()===marker,editable:await text.isEditable()};
  await ai.click();let held;
  await page.route('**/api/v1/ai/refine',route=>{held=route;});
  await page.getByRole('button',{name:'Đồng ý và tạo gợi ý',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('.fb-compose__ai-cancel')?.getBoundingClientRect().height>0);
  row.states.loading={editable:await text.isEditable(),cancelVisible:await page.getByRole('button',{name:'Hủy chờ gợi ý',exact:true}).isVisible()};await shot('loading');
  await page.getByRole('button',{name:'Hủy chờ gợi ý',exact:true}).click();await held.continue();await page.unroute('**/api/v1/ai/refine');await page.waitForTimeout(180);
  row.states.cancel={bodyPreserved:await text.inputValue()===marker,suggestionVisible:await page.getByRole('button',{name:'Dùng gợi ý',exact:true}).isVisible()};
  await ai.click();await page.getByRole('button',{name:'Dùng gợi ý',exact:true}).waitFor();await shot('suggestion');row.states.suggestion={visible:true};
  await text.fill(marker+' edited after suggestion');row.states.stale={useDisabled:await page.getByRole('button',{name:'Dùng gợi ý',exact:true}).isDisabled(),retryVisible:await page.getByRole('button',{name:'Tạo gợi ý mới',exact:true}).isVisible()};await shot('stale');
  await page.getByRole('button',{name:'Bỏ',exact:true}).click();await page.waitForTimeout(140);row.states.discard={bodyPreserved:await text.inputValue()===marker+' edited after suggestion'};
  await text.fill('AUDIT_FORCE_OUTAGE '+label);const failed=page.waitForResponse(r=>r.url().endsWith('/ai/refine'));await ai.click();const failedResponse=await failed;await page.waitForTimeout(100);row.states.error={http:failedResponse.status(),bodyPreserved:await text.inputValue()==='AUDIT_FORCE_OUTAGE '+label};await shot('error');
  const save=page.waitForResponse(r=>r.request().method()==='POST'&&new URL(r.url()).pathname===`/api/v1/drafts/${draft.draft_id}`);await page.getByRole('button',{name:'Lưu nháp riêng',exact:true}).click();await save;
  const paused=page.waitForResponse(r=>r.request().method()==='POST'&&r.url().endsWith('/pause'));await page.getByRole('button',{name:'Bắt đầu 5 phút nghỉ',exact:true}).click();await paused;await page.getByRole('button',{name:'Hủy khoảng dừng',exact:true}).waitFor();
  row.states.pause={previewDisabled:await page.getByRole('button',{name:'Xem trước nội dung',exact:true}).isDisabled()};await shot('pause');
  const cancelPause=page.waitForResponse(r=>r.request().method()==='DELETE'&&r.url().endsWith('/pause'));await page.getByRole('button',{name:'Hủy khoảng dừng',exact:true}).click();await cancelPause;
  await page.getByRole('button',{name:'Đổi',exact:true}).click();await page.locator('.fb-sheet').waitFor();row.states.recipient={visible:true};await shot('recipient');await page.keyboard.press('Escape');
  row.result='COMPLETED';
 }catch(e){row.result='INCOMPLETE';row.error=e.message;}finally{if(ctx)await ctx.close();writeFileSync(out+'/ui-states.json',JSON.stringify(results,null,2));console.log(JSON.stringify(row));}
}
await browser.close();
