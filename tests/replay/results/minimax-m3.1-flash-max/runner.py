#!/usr/bin/env python3
import os, subprocess, pathlib, time, json, sys
ROOT=pathlib.Path("/tmp/goal-spec-mcode-replay")
CASES=ROOT/"tests/replay/cases"
OUT=ROOT/"results"/"minimax-m3.1-flash-max"
MODEL="minimax/MiniMax-M3.1-Flash"
BIN="/root/.minimax-code/bin/mcode"
OUT.mkdir(parents=True, exist_ok=True)
meta={"model":MODEL,"effort":"max","cli_version":"0.7.2","source_commit":"418b2bc6a9c72e9a1a26a80a6d5090808520ae93","runs":[]}
prompts={
"A": """You are an independent senior engineering reviewer. Perform a STANDARD DESIGN REVIEW of the supplied specification as if reviewing a proposed engineering handoff.

Judge whether it is sufficiently clear and safe to hand to implementation as written. Inspect concrete requirements, user-visible behavior, business semantics, interfaces/contracts, architecture choices, assumptions, acceptance criteria, failure behavior, and scope boundaries where relevant. Do not force every category to have findings; only raise issues supported by the supplied text.

Return:
1. Verdict: READY, NEEDS_DECISION, or NOT_READY.
2. Findings, each with exact evidence/quote, why it matters, severity (blocker/major/minor), and the smallest proportionate correction.
3. Explicitly state what is already adequate and what should remain out of scope.
4. State whether any user/product decision is genuinely required, distinguishing it from reversible implementation details.

Do not write code. Do not inspect external files, use tools, assume hidden requirements, or invent features. Be precise; do not inflate minor omissions into blockers.""",
"B": """You are an independent reviewer operating a GOAL-SPEC PRE-EXECUTION GATE. Evaluate whether the supplied specification can be handed to a long-running autonomous Goal agent so it can execute the approved objective and determine completion without silently inventing product requirements.

Gate dimensions (apply only where relevant):
- objective and outcome closure;
- user workflow and business semantics;
- completeness and consistency of cross-module/interface/data constraints;
- foundational architecture and identity decisions that are expensive to reverse;
- critical assumptions that need evidence before autonomous execution;
- observable, reproducible acceptance and failure criteria;
- explicit in-scope/out-of-scope boundaries and approval/freeze authority;
- separation of genuine user decisions from reversible implementation details.

Return:
1. Verdict: READY, NEEDS_DECISION, or NOT_READY.
2. Findings with exact evidence/quote, failure mode for autonomous execution, severity, and the smallest proportionate fix.
3. Explicitly distinguish blockers from details the Goal agent may decide during implementation.
4. Identify any scope expansion or over-engineering that the gate must reject.
5. State what is already sufficient and should not be expanded.

Do not write code. Do not inspect external files, use tools, assume hidden requirements, or invent features. A gate is not a demand for exhaustive documentation: block only material ambiguity, contradiction, missing evidence, or non-verifiable completion.""",
}
order=[("C01","B"),("C01","A"),("C02","A"),("C02","B"),("C03","B"),("C03","A"),("C04","A"),("C04","B"),("C05","B"),("C05","A"),("C06","A"),("C06","B")]
for idx,(cid,group) in enumerate(order,1):
    case=next(CASES.glob(cid+"-*.md"))
    text=case.read_text()
    prompt=prompts[group]+"\n\n--- CASE INPUT (the complete and only review material) ---\n\n"+text
    run_id=f"{group}/{cid}"
    work=ROOT/"isolated"/f"{group}_{cid}"
    work.mkdir(parents=True,exist_ok=True)
    dest=OUT/group/f"{cid}.md"
    dest.parent.mkdir(parents=True,exist_ok=True)
    log=OUT/group/f"{cid}.log"
    cmd=[BIN,"exec","--model",MODEL,"--effort","max","--prompt-mode","work","--permission","off","--timeout","5m","--max-steps","1","--cwd",str(work),"--input","-","--input-format","text","--output-format","text","-o",str(dest)]
    started=time.time()
    print(f"[{idx}/12] START {run_id}",flush=True)
    try:
        p=subprocess.run(cmd,input=prompt,text=True,capture_output=True,timeout=360)
        combined=(p.stdout or "")+("\n[stderr]\n"+p.stderr if p.stderr else "")
        log.write_text(combined)
        status="ok" if p.returncode==0 and dest.exists() and dest.stat().st_size>0 else "failed"
        entry={"run":run_id,"status":status,"exit_code":p.returncode,"seconds":round(time.time()-started,1),"output":str(dest) if dest.exists() else None,"log":str(log)}
        if status!="ok":
            entry["diagnostic"]=combined[-5000:]
        meta["runs"].append(entry)
        print(f"[{idx}/12] {status.upper()} {run_id} exit={p.returncode} seconds={entry['seconds']} bytes={(dest.stat().st_size if dest.exists() else 0)}",flush=True)
    except subprocess.TimeoutExpired as e:
        log.write_text((e.stdout or b"").decode(errors="replace") if isinstance(e.stdout,bytes) else (e.stdout or ""))
        entry={"run":run_id,"status":"timeout","seconds":round(time.time()-started,1),"output":None,"log":str(log)}
        meta["runs"].append(entry)
        print(f"[{idx}/12] TIMEOUT {run_id}",flush=True)
    (OUT/"run-manifest.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print("SUMMARY",json.dumps({x["run"]:x["status"] for x in meta["runs"]},ensure_ascii=False),flush=True)
