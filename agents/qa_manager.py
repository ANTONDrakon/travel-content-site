from pathlib import Path
from datetime import datetime
import io
import sys

AGENTS = {
    "FACT": "agents.fact_agent",
    "IMAGE": "agents.image_agent",
    "LINK": "agents.link_agent",
    "COPY_SEO": "agents.copy_seo_agent",
    "UX_PERF": "agents.ux_performance_agent",
}

def run_agent(name, module):
    try:
        import importlib
        mod = importlib.import_module(module)
        old_stdout = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            result = mod.run()
        finally:
            sys.stdout = old_stdout
        output = buf.getvalue()[-500:]
        return {"agent": name, "status": "OK", "output": output, "issues": result}
    except Exception as e:
        return {"agent": name, "status": "ERROR", "output": str(e)}

def run():
    print("\n" + "="*60)
    print("QA MANAGER — FULL SITE AUDIT")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    reports = []
    for name, module in AGENTS.items():
        print(f"\n>>> Running {name}_AGENT...")
        report = run_agent(name, module)
        reports.append(report)

    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)

    total_issues = 0
    for r in reports:
        status_icon = "[OK]" if r["status"] == "OK" else "[ERR]"
        print(f"\n{status_icon} {r['agent']}_AGENT -- {r['status']}")
        if r.get("issues"):
            total_issues += r["issues"]
        if r["output"]:
            print(r["output"])

    print(f"\n{'='*60}")
    print(f"Audit complete. {len(reports)} agents executed, {total_issues} total issues.")
    print(f"{'='*60}")

if __name__ == "__main__":
    run()
