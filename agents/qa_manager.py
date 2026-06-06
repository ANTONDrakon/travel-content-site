from pathlib import Path
import subprocess, sys, json
from datetime import datetime

AGENTS = {
    "FACT": "agents.fact_agent",
    "IMAGE": "agents.image_agent",
    "LINK": "agents.link_agent",
    "COPY_SEO": "agents.copy_seo_agent",
    "UX_PERF": "agents.ux_performance_agent",
}

def run_agent(name, module):
    try:
        result = subprocess.run([sys.executable, "-m", module], capture_output=True, text=True, timeout=120)
        return {"agent": name, "status": "OK" if result.returncode == 0 else "ERROR", "output": result.stdout[-500:]}
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
        if r["output"]:
            print(r["output"])
    
    print(f"\n{'='*60}")
    print(f"Audit complete. {len(reports)} agents executed.")
    print(f"{'='*60}")

if __name__ == "__main__":
    run()
