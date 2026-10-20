// UI regression against real localhost API. Seed with seed_repeat.py first.
import {mkdir,writeFile} from 'node:fs/promises';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE||'playwright');
const out=process.env.F07_REPEAT_OUTPUT||'/tmp/f07-repeat-save';await mkdir(out,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
const results=[];
try { for (const [client,origin,code] of [['mini',process.env.F07_MINI_BASE||'http://127.0.0.1:3019','HSR08M19'],['web',process.env.F07_WEB_BASE||'http://127.0.0.1:5179','HSR08W19']]) {
 if(!['localhost','127.0.0.1'].includes(new URL(origin).hostname))throw Error('Local synthetic testing only');
 const page=await browser.newPage({viewport:{width:390,height:844}});await page.goto(origin+'/#/login');
 await page.locator('#fb-cred-code').fill(code);await page.locator('#fb-cred-password').fill(process.env.F07_SYNTHETIC_PASSWORD||'E2e-local-2026!');await page.getByRole('button',{name:'Đăng nhập vào không gian'}).click();await page.waitForURL(u=>!u.hash.startsWith('#/login'));
 await page.evaluate(()=>location.hash='/mood');const root=page.locator('[data-page=mood]');await root.locator('.fb-mood[data-emotion=vui]').waitFor();await page.waitForTimeout(500);
 for(const scenario of ['create-then-save','history-edit-then-save']) {
  if(scenario.startsWith('history')) {await root.getByRole('button',{name:'Sửa mục này',exact:true}).first().click();}
  const steps=[];
  for(let i=1;i<=2;i++) {const note=`R08 ${client} ${scenario} lần ${i} ${Date.now()}`;await root.locator('.fb-mood[data-emotion=vui]').click();await root.locator('.fb-textarea').fill(note);
   const responsePromise=page.waitForResponse(r=>new URL(r.url()).pathname.startsWith('/api/v1/mood/entries')&&['POST','PATCH'].includes(r.request().method()));
   await root.getByRole('button',{name:/^Lưu/}).first().click();const r=await responsePromise;await page.waitForTimeout(400);
   steps.push({attempt:i,method:r.request().method(),status:r.status(),saveLabel:await root.getByRole('button',{name:/^Lưu/}).first().innerText(),feedback:(await root.innerText()).split('\n').filter(s=>s.includes('Ngày này')||s.includes('Máy chủ đã ghi nhận')),draftPreserved:await root.locator('.fb-textarea').inputValue()===note});
  }
  const result={client,scenario,steps,pass:steps.every(s=>s.status<300)&&steps[1].method==='PATCH'};results.push(result);console.log(JSON.stringify(result));await page.screenshot({path:`${out}/${client}-${scenario}.png`,fullPage:true});
 }
 await page.close();
 }} finally {await writeFile(out+'/results.json',JSON.stringify({scope:'Real UI; dedicated unconnected synthetic accounts; no remount between saves',results},null,2)+'\n');await browser.close();}
process.exitCode=results.some(r=>!r.pass)?1:0;
