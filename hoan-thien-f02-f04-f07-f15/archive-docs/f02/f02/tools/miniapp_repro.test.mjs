// Read-only independent regressions against a selected application checkout.
// F02_APP_ROOT must name the exact QA source. Expected RED on c29469b.
import { register } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";
import { test } from "node:test";
import assert from "node:assert/strict";

const root = process.env.F02_APP_ROOT;
if (!root) throw new Error("Set F02_APP_ROOT to the application checkout.");
const appUrl = (file) => pathToFileURL(path.join(root, file));
await register(appUrl("zalo-mini-app/tests/asset-hook.mjs"));
const { Window } = await import(appUrl("zalo-mini-app/node_modules/happy-dom/lib/index.js"));
const win = new Window({url:"https://localhost/"});
for (const key of ["window","document","Node","Element","HTMLElement",
  "DocumentFragment","Event","CustomEvent","KeyboardEvent","location"]) {
  globalThis[key] = key === "window" ? win : win[key];
}
globalThis.requestAnimationFrame = (fn) => setTimeout(fn,0);
const session = await import(appUrl("zalo-mini-app/src/core/session.js"));
const store = await import(appUrl("zalo-mini-app/src/app/store.js"));
const { page } = await import(appUrl("zalo-mini-app/src/pages/companion/index.js"));
const wait = () => new Promise(resolve => setTimeout(resolve,80));
const key = "qa-program";
const detail = "BƯỚC ĐỘC LẬP: mỗi người lắng nghe và nhắc lại điều đã hiểu.";
const weeks = {program_key:key,pinned_revision:1,suggested_week:1,
  agreement:{revision:1,title:"Thỏa ước",commitments:["Một việc cụ thể"]},
  weeks:[1,2,3,4].map(n=>({week_no:n,title:"Chủ đề "+n,goals:[],
    student_guide:"HƯỚNG DẪN ĐỘC LẬP TUẦN "+n,caregiver_guide:"Hướng dẫn PH "+n,
    activities:n===1?[{activity_key:"qa-act",status:"none"}]:[],locked:false}))};

function fixture(enrolled=true) {
  session.clearSession();
  session.setSession({token:"synthetic-only",userId:"qa-self",expiresAt:Date.now()+120000});
  store.initStore({demoMode:false}); store.resetState(); store.setRole("student");
  const calls = [];
  const adapter = {
    programMy:async()=>({results:enrolled?[{program_key:key,program_revision:1,active:true}]:[]}),
    programCatalog:async()=>({results:[{program_key:key,revision:1,title:"QA",weeks:weeks.weeks}]}),
    programWeeks:async()=>weeks,
    programAgreement:async()=>({agreement:null,agreement_template:weeks.agreement,
      other_party_id:"qa-peer",connection_generation:1}),
    activitiesInvites:async()=>({results:[]}),
    activitiesCatalog:async()=>({results:[2,1].map(revision=>({
      content_key:"qa-act",revision,title:"Hoạt động QA",kind:"activity",
      audience:"joint",minutes:5,body:JSON.stringify({steps:[detail]})}))}),
    activitiesInvite:async(payload)=>{calls.push(payload);return {status:"pending"};},
  };
  const host=document.createElement("div");document.body.appendChild(host);
  host.appendChild(page.render({store:{getState:store.getState},adapter,navigate:()=>{}}));
  return {host,calls,close:()=>{page.destroy();host.remove();session.clearSession();}};
}

test("R01: two published revisions cannot make an old one overwrite latest",async()=>{
  const f=fixture();
  try {
    await wait();
    const button=[...f.host.querySelectorAll("button")].find(b=>b.textContent.includes("Mời cùng làm"));
    assert.ok(button);button.click();await wait();
    assert.equal(f.calls[0]?.contentRevision,2,"catalog [rev2,rev1] must not send rev1");
  } finally {f.close();}
});
test("R05: logged-in user can inspect a week guide without enrollment",async()=>{
  const f=fixture(false);
  try {
    await wait();
    const readable=f.host.textContent.includes("HƯỚNG DẪN ĐỘC LẬP")
      || [...f.host.querySelectorAll("button,a")].some(el=>
        /xem.*(tuần|chi tiết|chủ đề|hướng dẫn)/i.test(el.textContent));
    assert.ok(readable,"only enrollment CTA and titles do not provide read-only exploration");
  } finally {f.close();}
});
test("R06: published activity steps are readable or have a detail CTA",async()=>{
  const f=fixture();
  try {
    await wait();
    const readable=f.host.textContent.includes(detail)
      || [...f.host.querySelectorAll("button,a")].some(el=>
        /chi tiết|cách thực hiện|xem hoạt động/i.test(el.textContent));
    assert.ok(readable,"title/minutes/invite buttons are insufficient activity instructions");
  } finally {f.close();}
});
