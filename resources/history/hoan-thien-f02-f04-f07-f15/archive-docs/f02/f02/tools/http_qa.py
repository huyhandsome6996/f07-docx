"""Independent HTTP checks. Synthetic loopback fixture only. No token output."""
import argparse
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser()
parser.add_argument("--base", default="http://127.0.0.1:8004")
parser.add_argument("--out", required=True)
args = parser.parse_args()
base = args.base.rstrip("/")
parsed = urlsplit(base)
assert parsed.scheme == "http" and parsed.hostname in ("127.0.0.1", "localhost", "::1")
password = os.environ["F02_QA_PASSWORD"]
results = []

def call(path, actor=None, body=None):
    headers = {"Content-Type": "application/json"}
    if actor:
        headers["Authorization"] = "Bearer " + actor
    req = Request(base + "/api/v1" + path, headers=headers,
                  data=None if body is None else json.dumps(body).encode())
    try:
        with urlopen(req, timeout=15) as response:
            return response.status, json.load(response)
    except HTTPError as err:
        return err.code, json.load(err)

def check(identifier, name, passed, actual=None):
    row = {"id": identifier, "name": name, "pass": bool(passed), "actual": actual}
    results.append(row)
    print(("PASS" if passed else "FAIL") + " " + identifier + " " + name)

def login(code):
    status, data = call("/auth/class-session", body={"code": code, "password": password})
    check("LOGIN-" + code, "login synthetic actor", status == 200 and bool(data.get("token")), status)
    assert status == 200, "Fixture login failed."
    return data["token"]

key = "dong-hanh-bon-tuan"
activity = "f09-w1-tieng-long-chua-noi"
hs, ph, outsider = [login(code) for code in ("HS901", "PH901", "HS903")]
for label, actor in (("HS", hs), ("PH", ph)):
    status, data = call("/consents", actor, {"purpose": "service",
        "policy_version": "service-v1", "decision": "accepted"})
    check("CONSENT-" + label, "participant chooses service consent", status in (200, 201), status)
    status, data = call("/connections", actor)
    check("A01-" + label, "admin pair already active without confirmation",
          status == 200 and len(data["results"]) == 1
          and data["results"][0]["status"] == "active", data)
    if label == "HS":
        connection_id = data["results"][0]["connection_id"]
        peer = data["results"][0]["other_party_id"]
    status, data = call("/classroom/proposals", actor)
    check("A01-PROPOSALS-" + label, "no proposal to confirm", status == 200 and not data["results"], data)
status, data = call("/program/catalog", hs)
check("A04", "four published weeks from real startup provider",
      status == 200 and len(data["results"]) == 1
      and len(data["results"][0]["weeks"]) == 4,
      {"status": status, "count": len(data.get("results", []))})
status, data = call("/program/catalog")
check("E01", "anonymous request denied", status == 401, status)
for label, actor in (("HS", hs), ("PH", ph)):
    status, data = call("/program/enroll", actor, {"program_key": key, "program_revision": 1})
    check("B01-" + label, "voluntary enrollment pins revision1",
          status == 201 and data["program_revision"] == 1, data)
    status, data = call("/program/weeks/" + key, actor)
    check("A07-" + label, "week4 available before week1 completion",
          status == 200 and [w["week_no"] for w in data["weeks"]] == [1,2,3,4]
          and all(w["locked"] is False for w in data["weeks"]),
          {"status": status, "week_numbers": [w["week_no"] for w in data.get("weeks", [])]})
    check("C01-" + label, "real weeks response has activities, not fake field",
          "activities" in data["weeks"][0] and "joint_activity_keys" not in data["weeks"][0])
    check("B10-" + label, "paper alternative", "sổ giấy" in data["note_paper_guide"])
for label, actor, state in (("HS",hs,"done"), ("PH",ph,"skipped")):
    status, data = call("/program/progress", actor, {"program_key":key,
        "week_no":1, "activity_key":activity, "status":state})
    check("B02-" + label, "save own progress " + state, status == 201 and data["status"] == state, data)
    status, data = call("/program/weeks/" + key, actor)
    check("B03-" + label, "reload keeps own independent progress",
          status == 200 and data["weeks"][0]["activities"][0]["status"] == state)
status, data = call("/program/progress", hs, {"program_key":key, "week_no":1,
    "activity_key":activity, "status":"done", "participant_id":peer})
check("B04", "cannot tick another participant", status == 400, data)
status, data = call("/program/progress", hs, {"program_key":key, "week_no":4,
    "activity_key":activity, "status":"done"})
check("B05", "reject activity outside requested week", status == 400, data)
status, data = call("/program/progress", hs, {"program_key":key, "week_no":1,
    "activity_key":activity, "status":"reset"})
check("B02-RESET", "clear own progress", status == 201 and data["status"] == "reset", data)
status, data = call("/activities/catalog?kind=activity", hs)
revs = [i["revision"] for i in data["results"] if i["content_key"] == activity]
check("C02-CATALOG", "published activity revision2 exists", 2 in revs, revs)
status, invite = call("/activities/invites", hs, {"invitee_id":peer,
    "content_key":activity, "content_revision":2})
check("C04", "invite does not auto-accept", status == 201 and invite["status"] == "pending", invite)
invite_id = invite["invite_id"]
status, duplicate = call("/activities/invites", hs, {"invitee_id":peer,
    "content_key":activity, "content_revision":2})
check("C07", "duplicate pending invite uses same id", status == 201 and duplicate["invite_id"] == invite_id)
status, data = call("/activities/invites", ph)
check("C04-RECEIVED", "receiver sees actual pending invite",
      any(i["invite_id"] == invite_id and i["direction"] == "received" for i in data["results"]))
status, data = call("/activities/invites/" + invite_id + "/respond", hs, {"decision":"accept"})
check("C05-SENDER", "sender cannot accept for receiver", status == 404, data)
status, data = call("/activities/invites/" + invite_id + "/respond", outsider, {"decision":"accept"})
check("C06", "other family cannot accept invite", status == 404, data)
status, data = call("/activities/invites/" + invite_id + "/respond", ph, {"decision":"accept"})
check("C05-ACCEPT", "receiver accepts", status == 200 and data["status"] == "accepted", data)
status, agreement = call("/program/agreement/propose", hs, {"program_key":key})
agreement_id = agreement["agreement_id"]
check("D01-D04", "admin inviteNULL pair can propose without signatures",
      status == 201 and agreement["status"] == "proposed"
      and not agreement["my_confirmed"] and not agreement["counterpart_confirmed"], agreement)
status, data = call("/program/agreement/" + agreement_id + "/confirm", outsider, {})
check("D11", "other family cannot sign", status == 404, data)
status, data = call("/program/agreement/" + agreement_id + "/confirm", hs, {})
first_time = data["updated_at"]
check("D05", "one signature stays proposed",
      status == 200 and data["my_confirmed"] and data["status"] == "proposed", data)
status, data = call("/program/agreement/" + agreement_id + "/confirm", hs, {})
check("D05-DUP", "same person cannot sign twice", status == 400, data)
time.sleep(0.05)
status, data = call("/program/agreement/" + agreement_id + "/confirm", ph, {})
check("D06", "two different signatures confirm same revision",
      status == 200 and data["status"] == "confirmed"
      and data["my_confirmed"] and data["counterpart_confirmed"], data)
check("NEW-TIMESTAMP", "confirmed_at is second-signature time",
      data["confirmed_at"] > first_time,
      {"first_signature": first_time, "confirmed_at":data["confirmed_at"],
       "second_signature": data["updated_at"]})
status, data = call("/program/opt-out", hs, {"program_key":key})
check("B09-OUT", "opt-out is voluntary", status == 200 and data["active"] is False, data)
status, data = call("/program/weeks/" + key, hs)
check("B09-NO-ENROLL", "no phantom active enrollment", status == 404, data)
status, data = call("/program/enroll", hs, {"program_key":key, "program_revision":1})
check("B09-REJOIN", "rejoin explicitly", status == 201 and data["active"] is True, data)

# Pending second activity to probe F09 unlink guard on a different invite.
status, pending = call("/activities/invites", hs, {"invitee_id":peer,
    "content_key":"f09-w2-ban-sac-rieng", "content_revision":1})
check("C04-UNLINK-PRE", "pending invite exists before unlink", status == 201 and pending["status"] == "pending")
status, data = call("/connections/" + connection_id + "/revoke", hs, {})
check("D12-UNLINK", "unlink succeeds through real F01", status == 200 and data["status"] == "revoked", data)
status, data = call("/program/agreement?program_key=" + key, ph)
check("D12-OVERVIEW", "old family agreement unavailable after unlink",
      status in (400,404), data)
status, data = call("/activities/invites/" + pending["invite_id"] + "/respond", ph, {"decision":"accept"})
check("NEW-F09-UNLINK", "cannot accept joint invitation after connection revoked",
      status in (400,403,404,409) or data.get("status") in ("cancelled","expired"),
      {"status":status, "response":data})

out = Path(args.out)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"base":base,"synthetic_only":True,"results":results,
    "pass":sum(r["pass"] for r in results),"fail":sum(not r["pass"] for r in results)},
    ensure_ascii=False, indent=2), encoding="utf-8")
print("RESULT", sum(r["pass"] for r in results), "PASS;",
      sum(not r["pass"] for r in results), "FAIL")
