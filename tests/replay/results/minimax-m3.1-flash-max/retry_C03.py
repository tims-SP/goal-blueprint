import pathlib, subprocess, time, json
R=pathlib.Path("/tmp/goal-spec-mcode-replay")
case=next((R/"tests/replay/cases").glob("C03-*.md")).read_text()
prompt="""You are an independent senior engineering reviewer. Perform a STANDARD DESIGN REVIEW of the supplied specification as if reviewing a proposed engineering handoff.

Judge whether it is sufficiently clear and safe to hand to implementation as written. Inspect concrete requirements, user-visible behavior, business semantics, interfaces/contracts, architecture choices, assumptions, acceptance criteria, failure behavior, and scope boundaries where relevant. Do not force every category to have findings; only raise issues supported by the supplied text.

Return:
1. Verdict: READY, NEEDS_DECISION, or NOT_READY.
2. Findings, each with exact evidence/quote, why it matters, severity (blocker/major/minor), and the smallest proportionate correction.
3. Explicitly state what is already adequate and what should remain out of scope.
4. State whether any user/product decision is genuinely required, distinguishing it from reversible implementation details.

Do not write code. Do not inspect external files, use tools, assume hidden requirements, or invent features. Be precise; do not inflate minor omissions into blockers.

--- CASE INPUT (the complete and only review material) ---

"""+case
out=R/"results/minimax-m3.1-flash-max/retry/A/C03.md"
out.parent.mkdir(parents=True,exist_ok=True)
cwd=R/"isolated/A_C03_retry"; cwd.mkdir(parents=True,exist_ok=True)
cmd=["/root/.minimax-code/bin/mcode","exec","--model","minimax/MiniMax-M3.1-Flash","--effort","max","--prompt-mode","work","--permission","off","--timeout","5m","--max-steps","3","--cwd",str(cwd),"--input","-","--input-format","text","--output-format","text","-o",str(out)]
t=time.time()
p=subprocess.run(cmd,input=prompt,text=True,capture_output=True,timeout=360)
(R/"results/minimax-m3.1-flash-max/retry/A/C03.log").write_text((p.stdout or "")+"\n[stderr]\n"+(p.stderr or ""))
print(json.dumps({"exit_code":p.returncode,"seconds":round(time.time()-t,1),"output_exists":out.exists(),"output_bytes":out.stat().st_size if out.exists() else 0,"stderr":p.stderr[-2000:]},ensure_ascii=False))
