// Real local browser/API parity checks. No response bodies or tokens are logged.
import {mkdir,writeFile} from 'node:fs/promises';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const output=process.env.F07_PARITY_OUTPUT || '/tmp/f07-client-parity';
const apiBase=process.env.F07_API_BASE || 'http://127.0.0.1:8019';
const origins={mini:process.env.F07_MINI_BASE || 'http://127.0.0.1:3019',web:process.env.F07_WEB_BASE || 'http://127.0.0.1:5179'};
for(const value of [apiBase,...Object.values(origins)]) if(!['localhost','127.0.0.1'].includes(new URL(value).hostname)) throw new Error('Disposable localhost testing only');
await mkdir(output,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium',headless:true,args:['--no-sandbox']});
const results=[];
const requests=[];
function check(name,pass,observed){results.push({name,pass,observed});console.log(`${pass?'PASS':'FAIL'} ${name}: ${JSON.stringify(observed)}`);}
try{
  for(const [client,origin] of Object.entries(origins)){
    const page=await browser.newPage({viewport:client==='web'?{width:1280,height:900}:{width:390,height:844}});
    page.on('response',r=>{const path=new URL(r.url()).pathname;if(path.startsWith('/api/v1/')) requests.push({client,method:r.request().method(),path:path.replace(/[0-9a-f]{8}-[0-9a-f-]{27}/gi,'<id>'),status:r.status()});});
    await page.goto(`${origin}/#/login`);
    await page.locator('#fb-cred-code').fill(process.env.F07_PARITY_CODE || 'HSPAR19');
    await page.locator('#fb-cred-password').fill(process.env.F07_SYNTHETIC_PASSWORD || 'E2e-local-2026!');
    const login=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/v1/auth/class-session' && r.request().method()==='POST');
    await page.getByRole('button',{name:'Đăng nhập vào không gian'}).click();
    check(`${client}-real-login`,(await login).status()===200,(await login).status());
    await page.waitForURL(url=>!url.hash.startsWith('#/login'));
    const diagnostic=await page.evaluate(async({client,apiBase})=>{
      const module=client==='web'?await import('/src/adapter/web-adapter.js'):await import('/src/core/adapter/zalo-adapter.js');
      const adapter=client==='web'?module.createWebAdapter({baseUrl:apiBase}):module.createZaloAdapter({baseUrl:apiBase});
      const names=['getMoodEntry','editMoodEntry','moodSummary','listMoodEntryShares','shareMoodEntry','revokeMoodShare','listSharedMoodEntries','getSharedMoodEntry'];
      const list=await adapter.listMoodEntries({limit:2});
      let detailRead=false;
      if(list.results[0]) detailRead=(await adapter.getMoodEntry(list.results[0].entry_id)).entry_id===list.results[0].entry_id;
      return {allEightMethods:names.every(name=>typeof adapter[name]==='function'),listed:list.results.length,detailRead};
    },{client,apiBase});
    check(`${client}-shared-adapter-real-api`,diagnostic.allEightMethods && diagnostic.detailRead,diagnostic);
    for(const route of ['mood','mood-shared']){
      await page.evaluate(route=>{location.hash=`/${route}`},route);
      await page.locator(`[data-page="${route}"],[data-page="not-found"]`).first().waitFor();
      const observed=await page.locator('[data-page]').evaluateAll(nodes=>nodes.map(n=>n.dataset.page));
      check(`${client}-route-${route}`,observed.includes(route),observed);
      await page.screenshot({path:`${output}/${client}-${route}.png`,fullPage:true});
    }
    await page.evaluate(()=>{location.hash='/profile'});
    await page.locator('[data-page="profile"]').waitFor();
    const owner=page.getByRole('button',{name:'Tâm trạng của mình',exact:true}).or(page.getByRole('link',{name:'Tâm trạng của mình',exact:true}));
    const recipient=page.getByRole('button',{name:'Được chia sẻ với bạn',exact:true}).or(page.getByRole('link',{name:'Được chia sẻ với bạn',exact:true}));
    check(`${client}-profile-f07-navigation`,await owner.count()>0 && await recipient.count()>0,{owner:await owner.count(),recipient:await recipient.count()});
    await page.screenshot({path:`${output}/${client}-profile.png`,fullPage:true});
    if(client==='web'){
      await page.evaluate(()=>{location.hash='/home'});
      await page.locator('[data-page="u08-home"]').waitFor();
      await page.waitForLoadState('networkidle');
      const chip=page.locator('[data-page="u08-home"] [data-emotion="vui"]').first();
      if(await chip.count()){
        for(let attempt=0;attempt<2;attempt++){
          const response=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/v1/mood/entries' && r.request().method()==='POST');
          await chip.click();
          const status=(await response).status();
          check(`web-home-quick-mood-api-${attempt+1}`,[201,400].includes(status),status);
        }
      }else{
        console.log('INFO no legacy quick-mood card; validate the full F07 flow separately');
      }
      const placeholder=(await page.locator('body').innerText()).includes('Màn nhật ký sẽ cho phép chỉnh sửa ở bản đầy đủ.');
      console.log('INFO web-home-edit-placeholder',placeholder);
      await page.screenshot({path:`${output}/web-home-duplicate-no-edit.png`,fullPage:true});
    }
    await page.close();
  }
}finally{
  await writeFile(`${output}/results.json`,JSON.stringify({scope:'Real local class-session and adapter API; route/navigation parity; synthetic parity fixtures only',results,requests},null,2)+'\n');
  await browser.close();
}
process.exitCode=results.some(r=>!r.pass)?1:0;
