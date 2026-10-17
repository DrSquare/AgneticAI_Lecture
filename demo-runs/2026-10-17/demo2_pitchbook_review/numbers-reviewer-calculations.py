"""FICTIONAL TEACHING MATERIAL. Independent GraspLoop AI numbers audit.
Review date: 2026-10-17 America/Los_Angeles. CSV observations through 2026-09.
Run with Python standard library; no network or supplied reference outputs.
"""
from pathlib import Path
import csv, json, hashlib, math
ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "Agentic_AI_Demos/demo2_pitchbook_review/inputs/data-room/kpi-monthly.csv"
OUT = Path(__file__).with_suffix(".json")
with SOURCE.open(newline="", encoding="utf-8-sig") as f:
    raw = list(csv.DictReader(f))
rows = [{k: (v if k == "month" else float(v)) for k, v in r.items()} for r in raw]
for i, row in enumerate(rows):
    row["csv_physical_row"] = i + 2
first, latest = rows[0], rows[-1]
def close(a, b): return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-6)
checks = []
def check(name, ok, evidence):
    checks.append({"name": name, "status": "pass" if ok else "fail", "evidence": evidence})
check("13 consecutive observations", len(rows)==13 and first["month"]=="2025-09" and latest["month"]=="2026-09", "CSV physical rows 2-14")
check("MRR equals paying robots times 3500", all(close(r["mrr_usd"], r["robots_live_paying"]*3500) for r in rows), "All 13 rows")
check("Booked field includes unpaid pilots", all(close(r["booked_arr_incl_pilots_usd"], (r["robots_live_paying"]+r["robots_in_unpaid_pilots"])*3500*12) for r in rows), "All 13 rows; does not prove pilot contracts")
check("Reported burn equals opex minus gross profit", all(close(r["net_burn_usd"], r["opex_usd"]-r["mrr_usd"]*r["gross_margin_pct"]/100) for r in rows), "All 13 rows; no separately visible capex line")
check("Cash rollforward", all(close(rows[i]["cash_end_usd"], rows[i-1]["cash_end_usd"]-rows[i]["net_burn_usd"]) for i in range(1,len(rows))), "Rows 3-14 against prior row; opening Sep25 cash not supplied")
periods = []
for label, start in [("September 2026",12),("Q3 2026: July-September",10),("April-September 2026",7),("October 2025-September 2026",1)]:
    selected, base = rows[start:], rows[start-1]
    spend = sum(r["sales_marketing_usd"] for r in selected)
    net_new = latest["mrr_usd"]-base["mrr_usd"]
    rev = sum(r["mrr_usd"] for r in selected)
    weighted_gm = sum(r["mrr_usd"]*r["gross_margin_pct"]/100 for r in selected)/rev
    periods.append({
        "interval":label,"spend_csv_rows":[r["csv_physical_row"] for r in selected],
        "baseline_csv_row":base["csv_physical_row"],"baseline_month":base["month"],
        "sales_marketing_usd":spend,"net_new_mrr_usd":net_new,
        "ending_gross_margin":latest["gross_margin_pct"]/100,
        "ending_gm_proxy_months":spend/(net_new*latest["gross_margin_pct"]/100),
        "revenue_weighted_period_gross_margin":weighted_gm,
        "weighted_gm_proxy_months":spend/(net_new*weighted_gm),
        "limitation":"Aggregate net-new-MRR proxy. Not acquisition cohort CAC; no gross adds, churn/expansion decomposition, attribution or lag data."
    })
growth = []
for i in range(1,len(rows)):
    growth.append({"month":rows[i]["month"],"csv_rows":[i+1,i+2],"mrr_growth_pct":(rows[i]["mrr_usd"]/rows[i-1]["mrr_usd"]-1)*100})
paying_arr = latest["mrr_usd"]*12
cash, burn, raise_usd = latest["cash_end_usd"], latest["net_burn_usd"], 18000000
forward_opex = latest["opex_usd"]*85/latest["headcount"]
forward_burn = forward_opex-latest["mrr_usd"]*latest["gross_margin_pct"]/100
results = {
    "fictional_teaching_material":True,
    "review_date":"2026-10-17","review_timezone":"America/Los_Angeles","source_data_through":"2026-09",
    "source_relative_path":str(SOURCE.relative_to(ROOT)),"source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "row_reference_convention":"Physical CSV rows, including header as row 1.",
    "paying_arr_usd":paying_arr,"booked_including_unpaid_pilots_usd":latest["booked_arr_incl_pilots_usd"],
    "unpaid_pilot_annualized_capacity_usd":latest["robots_in_unpaid_pilots"]*3500*12,
    "paying_arr_overstatement_pct":(latest["booked_arr_incl_pilots_usd"]/paying_arr-1)*100,
    "paying_arr_yoy_multiple":latest["mrr_usd"]/first["mrr_usd"],
    "paying_arr_yoy_growth_pct":(latest["mrr_usd"]/first["mrr_usd"]-1)*100,
    "booked_including_pilots_yoy_multiple":latest["booked_arr_incl_pilots_usd"]/first["booked_arr_incl_pilots_usd"],
    "latest_paying_customers":latest["paying_customers"],"latest_unpaid_pilot_customers":latest["pilot_customers_unpaid"],
    "reported_mixed_sku_success_pct":latest["pick_success_mixed_sku_pct"],
    "reported_best_site_single_sku_success_pct":latest["pick_success_best_site_single_sku_pct"],
    "september_2025_cohort_n":first["paying_customers"],
    "september_2025_cohort_nrr_pct":latest["sep2025_cohort_mrr_usd"]/first["sep2025_cohort_mrr_usd"]*100,
    "september_2026_reported_gm_pct":latest["gross_margin_pct"],
    "september_2026_implied_cogs_usd":latest["mrr_usd"]*(1-latest["gross_margin_pct"]/100),
    "september_2026_gross_profit_usd":latest["mrr_usd"]*latest["gross_margin_pct"]/100,
    "monthly_mrr_growth":growth,
    "q3_mrr_cumulative_growth_pct":(latest["mrr_usd"]/rows[9]["mrr_usd"]-1)*100,
    "q3_geometric_monthly_mrr_growth_pct":((latest["mrr_usd"]/rows[9]["mrr_usd"])**(1/3)-1)*100,
    "year_geometric_monthly_mrr_growth_pct":((latest["mrr_usd"]/first["mrr_usd"])**(1/12)-1)*100,
    "cac_proxy_intervals":periods,
    "current_pre_raise_static_runway_months":cash/burn,
    "post_raise_static_runway_months":(cash+raise_usd)/burn,
    "max_average_monthly_net_cash_burn_for_24_months_usd":(cash+raise_usd)/24,
    "headcount_proportional_opex_stress_scenario":{
        "not_a_forecast":True,"assumptions":"Immediate 85/38 scaling of all Sep26 opex; MRR and GM flat; raise immediately; zero fees; no additional explicit capex.",
        "forward_opex_usd":forward_opex,"forward_burn_usd":forward_burn,
        "post_raise_runway_months":(cash+raise_usd)/forward_burn},
    "price_constant_robot_target_scenario":[
        {"year":year,"deck_arr_usd":arr,"minimum_paying_robots":math.ceil(arr/(3500*12))}
        for year,arr in [(2026,2400000),(2027,9000000),(2028,30000000),(2029,100000000)]],
    "ask_allocation_usd":{"R_and_D_50pct":9000000,"go_to_market_30pct":5400000,"operations_20pct":3600000},
    "proposed_postmoney_usd":108000000,"proposed_new_money_ownership_pct":18000000/108000000*100,
    "checks":checks,
    "source_rows":rows
}
check("Q3 proxy rounds to 26 months", round(periods[1]["ending_gm_proxy_months"])==26, "490000 / ((161000-115500)*0.41) = 26.2664 months")
check("Paying ARR is below blended booked field", paying_arr==1932000 and latest["booked_arr_incl_pilots_usd"]==2436000, "161000*12; difference504000 from12 unpaid pilot robots")
check("NRR near 160 is not exact and has n=3", close(results["september_2025_cohort_nrr_pct"],157.14285714285714) and first["paying_customers"]==3, "38500/24500*100; rows2,14")
assert all(c["status"]=="pass" for c in checks), checks
OUT.write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:results[k] for k in ["fictional_teaching_material","source_data_through","paying_arr_usd","paying_arr_yoy_multiple","september_2025_cohort_nrr_pct","cac_proxy_intervals","current_pre_raise_static_runway_months","post_raise_static_runway_months","max_average_monthly_net_cash_burn_for_24_months_usd","checks"]},indent=2))
print("Saved "+str(OUT))

