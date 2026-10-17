"""GraspLoop AI: fictional teaching data. Read-only inputs; reproducible local audit.
Run: python calculate.py [--input path/to/kpi-monthly.csv]
CSV row numbers include header as row 1. Financial values are USD.
"""
import argparse, csv, hashlib, json, math
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=Path, default=ROOT/'Agentic_AI_Demos/demo2_pitchbook_review/inputs/data-room/kpi-monthly.csv')
args = parser.parse_args()
raw = list(csv.DictReader(args.input.open(encoding='utf-8-sig', newline='')))
r = [{k: (v if k=='month' else float(v)) for k,v in row.items()} for row in raw]
for i,row in enumerate(r,2): row['csv_row'] = i
first, last = r[0], r[-1]
checks = []
def check(name, valid, evidence):
    checks.append({'name':name,'status':'pass' if valid else 'fail','evidence':evidence})
check('13 ordered unique monthly records',len(r)==13 and len({x['month'] for x in r})==13 and [x['month'] for x in r]==sorted(x['month'] for x in r), 'CSV rows 2-14; Sep 2025-Sep 2026')
check('Source period', first['month']=='2025-09' and last['month']=='2026-09', f"{first['month']} to {last['month']}")
for x in r:
    row = f"row {x['csv_row']} ({x['month']})"
    check('Paying MRR identity: '+row,abs(x['mrr_usd']-3500*x['robots_live_paying'])<.01,'mrr_usd = paying robots * 3500')
    check('Booked metric identity: '+row,abs(x['booked_arr_incl_pilots_usd']-(x['robots_live_paying']+x['robots_in_unpaid_pilots'])*3500*12)<.01,'booked_arr_incl_pilots = (paying + unpaid pilot robots) * 3500 * 12; not evidence of signed bookings')
    check('Burn identity: '+row,abs(x['net_burn_usd']-(x['opex_usd']-x['mrr_usd']*x['gross_margin_pct']/100))<.01,'net burn = opex - implied gross profit; separate capex not identifiable')
for a,b in zip(r,r[1:]):
    check('Cash roll-forward: '+b['month'],abs(a['cash_end_usd']-b['net_burn_usd']-b['cash_end_usd'])<.01,f"rows {a['csv_row']}-{b['csv_row']}: prior cash - current burn = current cash")

gm = last['gross_margin_pct']/100
paying_arr = last['mrr_usd']*12
booked_arr = last['booked_arr_incl_pilots_usd']
annual_spend = sum(x['sales_marketing_usd'] for x in r[1:])
net_new = last['mrr_usd']-first['mrr_usd']
windows=[]
for months in (1,3,6,12):
    baseline = r[-months-1]
    subset=r[-months:]
    spend=sum(x['sales_marketing_usd'] for x in subset)
    delta=last['mrr_usd']-baseline['mrr_usd']
    incr_gp=sum((b['mrr_usd']-a['mrr_usd'])*b['gross_margin_pct']/100 for a,b in zip(r[-months-1:-1],subset))
    windows.append({'months':months,'spend_period':f"{subset[0]['month']} to {last['month']}",'spend_csv_rows':[int(x['csv_row']) for x in subset],'mrr_baseline_month':baseline['month'],'baseline_csv_row':int(baseline['csv_row']),'sales_marketing_usd':spend,'net_new_mrr_usd':delta,'ending_gross_margin':gm,'payback_proxy_months':spend/(delta*gm),'monthly_margin_weighted_proxy_months':spend/incr_gp,'warning':'Net new MRR includes expansion/contraction/churn; not gross new-logo MRR. Spend is not acquisition-cohort aligned. Actual CAC payback unverifiable.'})

cash=last['cash_end_usd']; raise_usd=18_000_000; gp=last['mrr_usd']*gm
scaled_opex=last['opex_usd']*85/38
scaled_burn=scaled_opex-gp
runway=[]
for label,start,burn in [('No raise, September burn unchanged',cash,last['net_burn_usd']),('Raise closes immediately; September burn unchanged',cash+raise_usd,last['net_burn_usd']),('Raise closes immediately; full 85-person opex scale at constant September gross profit',cash+raise_usd,scaled_burn)]:
    runway.append({'scenario':label,'opening_cash_usd':start,'monthly_burn_usd':burn,'runway_months':start/burn,'type':'Illustrative sensitivity, not a forecast. No fees, separate capex, financing flows or working capital.'})
forward=[]; balance=cash+raise_usd
for month in range(1,25):
    hc=38+(85-38)*month/24
    opex=last['opex_usd']*hc/38
    burn=opex-gp
    prior=balance;balance-=burn
    forward.append({'fictional_teaching_material':True,'source_data_as_of':'2026-09-30','scenario':'Illustrative linear 24-month headcount ramp; not forecast; no separate capex','month_after_raise':month,'assumed_headcount':hc,'assumed_opex_usd':opex,'assumed_gross_profit_usd':gp,'assumed_burn_usd':burn,'ending_cash_usd':balance})
ramp_runout=next((x['month_after_raise']-1+(x['ending_cash_usd']+x['assumed_burn_usd'])/x['assumed_burn_usd'] for x in forward if x['ending_cash_usd']<0),None)
future=[]
for year,arr in [(2026,2_400_000),(2027,9_000_000),(2028,30_000_000),(2029,100_000_000)]:
    robots=math.ceil(arr/(3500*12))
    future.append({'year':year,'deck_arr_target_usd':arr,'required_paying_robots_at_current_price':robots,'incremental_robots_vs_sep2026':robots-int(last['robots_live_paying']),'illustrative_incremental_hardware_usd_at_unverified_42000_unit_cost':(robots-last['robots_live_paying'])*42000})

metrics={
'fictional_teaching_material':True,'data_as_of':'2026-09-30','review_date':'2026-10-17','timezone':'America/Los_Angeles',
'paying_arr_usd':paying_arr,'pilot_inclusive_metric_usd':booked_arr,'unpaid_pilot_arr_equivalent_usd':booked_arr-paying_arr,
'pilot_inclusive_overstatement_relative_to_paying_pct':100*(booked_arr/paying_arr-1),
'paying_yoy_multiple':last['mrr_usd']/first['mrr_usd'],'paying_yoy_growth_pct':100*(last['mrr_usd']/first['mrr_usd']-1),
'pilot_inclusive_yoy_multiple':booked_arr/first['booked_arr_incl_pilots_usd'],
'paying_mrr_monthly_growth_pct':[{'month':b['month'],'csv_row':int(b['csv_row']),'growth_pct':100*(b['mrr_usd']/a['mrr_usd']-1)} for a,b in zip(r,r[1:])],
'paying_mrr_12mo_compound_monthly_growth_pct':100*((last['mrr_usd']/first['mrr_usd'])**(1/12)-1),
'paying_mrr_q3_growth_pct':100*(last['mrr_usd']/r[-4]['mrr_usd']-1),
'paying_customers':last['paying_customers'],'unpaid_pilot_customers':last['pilot_customers_unpaid'],
'fleet_mixed_sku_success_pct':last['pick_success_mixed_sku_pct'],'best_site_single_sku_success_pct':last['pick_success_best_site_single_sku_pct'],
'gross_margin_pct':last['gross_margin_pct'],'gross_profit_usd':gp,'implied_cogs_usd':last['mrr_usd']-gp,
'revenue_weighted_12mo_gross_margin_pct':sum(x['mrr_usd']*x['gross_margin_pct'] for x in r[1:])/sum(x['mrr_usd'] for x in r[1:]),
'nrr_sep2025_cohort_pct':100*last['sep2025_cohort_mrr_usd']/first['sep2025_cohort_mrr_usd'],'nrr_starting_customer_count':3,
'cac_payback_proxies':windows,'cash_end_usd':cash,'september_net_burn_usd':last['net_burn_usd'],
'24mo_max_average_burn_after_raise_usd':(cash+raise_usd)/24,'runway_sensitivities':runway,
'linear_24mo_headcount_ramp_runout_month':ramp_runout,'linear_ramp_24mo_ending_cash_usd':balance,
'headcount_increase_pct':100*(85/38-1),'forward_targets':future,
'hardware_scenario_assumption':'Each incremental paying robot above September 46 is newly purchased; no conversion/reuse of existing 12 pilot robots, no spare inventory, no leasing or vendor finance. Unit cost42000 is unverified.',
'2026_to_2029_target_cagr_pct':100*((100_000_000/2_400_000)**(1/3)-1),
'pre_money_usd':90_000_000,'post_money_usd':108_000_000,'new_money_ownership_pct_simple':100*18/108,
'use_of_proceeds_usd':{'rnd':9_000_000,'gtm':5_400_000,'operations':3_600_000},
'hardware_revenue_recovery_months_unverified_cost':42000/3500,'hardware_gp_recovery_months_unverified_cost':42000/(3500*gm),
'limitations':['Fictional aggregated data, no contracts, invoices, customer identities, cohort movements or cost ledger.','Actual CAC payback, true contracted ARR and forward runway cannot be established.','Hardware cost, team records, market claims, fundraising and hiring assumptions are deck-only and unverifiable.']}

claims=[]
def add(cid,page,claim,status,result,evidence,formula='',kind='historical',missing=''):
    claims.append(dict(id=cid,page=page,claim=claim,status=status,result=result,evidence=evidence,formula=formula,kind=kind,missing_data=missing))
for cid,claim in [('P2-01','Peak-season picker turnover >100%'),('P2-02','Order growth 3x headcount growth since 2020'),('P2-03','Fully loaded cost per pick $0.42'),('P2-04','Cost per pick rising 9%/yr'),('P2-05','Vendors serve top 1%; other 99% left with clipboards')]:
    add(cid,2,claim,'unverifiable','No supporting market/customer study in supplied room','Deck p2 only',missing='Definitions, sampled sites, period and underlying source')
for cid,claim in [('P3-01','Off-the-shelf 6-axis arm'),('P3-02','Installs in one day'),('P3-03','New SKU learned in 10 minutes'),('P3-04','New SKU learned from 20 picks'),('P3-05','Remote operators resolve picks in seconds')]:
    add(cid,3,claim,'unverifiable','Product/system evidence absent','Deck p3 only',missing='BOM, installation logs or SKU learning and intervention timing tests')
for cid,claim in [('P4-01','Foundation models made generalist grasping practical in 2025-26'),('P4-02','Collaborative arms below $25,000')]:
    add(cid,4,claim,'unverifiable','No dated evaluation or purchase quote supplied','Deck p4 only',missing='Technical evaluation or arm quote; arm price differs from full robot cost')
for cid,claim in [('P5-01','$120B TAM in 2030'),('P5-02','$9B SAM US/EU mid-size piece-picking'),('P5-03','$450M SOM reachable by 2030')]:
    add(cid,5,claim,'unverifiable','Market sizing and share assumptions absent','Deck p5 only',kind='market estimate/projection',missing='Bottom-up site count, spend, eligibility and adoption model')
add('P6-01',6,'$2.4M ARR','contradicted_as_paying_arr',f'Paying ARR ${paying_arr:,.0f}; pilot-inclusive metric ${booked_arr:,.0f}','CSV row 14 (2026-09), README','161000 * 12; (46 + 12) * 3500 * 12',missing='Signed contracts needed to establish actual contracted ARR')
add('P6-02',6,'8x YoY ARR growth','needs_qualification',f"Paying {metrics['paying_yoy_multiple']:.4f}x (+{metrics['paying_yoy_growth_pct']:.2f}%); pilot-inclusive {metrics['pilot_inclusive_yoy_multiple']:.4f}x",'CSV rows 2 and 14 (2025-09,2026-09)','161000 / 24500; 2436000 / 294000')
add('P6-03',6,'14 customers','needs_qualification','11 paying + 3 unpaid pilots = 14 total','CSV row 14 (2026-09)','11 + 3')
add('P6-04',6,'Includes 3 Fortune 500 retailers','unverifiable','Customer identities unavailable','Deck p6 only',missing='Customer list and status')
add('P6-05',6,'99.7% pick success','needs_qualification','99.7% best site single SKU; 97.2% fleet mixed SKU','CSV row 14 (2026-09), README','Read distinct success columns',missing='Trial design and raw success denominators')
add('P6-06',6,'160% NRR','needs_qualification',f"{metrics['nrr_sep2025_cohort_pct']:.2f}% for starting n=3 only; 160% is rough rounding",'CSV rows 2 and 14; README cohort definition','38500 / 24500 * 100',missing='Customer-level cohort bridge, churn and expansion')
add('P7-01',7,'$3,500 per robot per month','supported','Matches all 13 paying MRR rows','CSV rows 2-14; README','mrr_usd / robots_live_paying = 3500',missing='Contract verification outside supplied data')
add('P7-02',7,'3-year term','unverifiable','No executed contracts supplied','Deck p7 only',missing='Signed agreements and cancellation rights')
add('P7-03',7,'68% gross margin','contradicted_as_current',f"September 41%; no month reaches 68%; trailing-12 revenue-weighted {metrics['revenue_weighted_12mo_gross_margin_pct']:.2f}%",'CSV rows 2-14 (2025-09 to 2026-09)','Read monthly gross_margin_pct; sum(MRR * GM) / sum(MRR)',missing='Cost composition; 68% may be a future target but deck does not label it')
add('P7-04',7,'4-month CAC payback','unverifiable_and_inconsistent_with_available_proxy',f"Net-new-MRR proxies: Sept {windows[0]['payback_proxy_months']:.2f}; Q3 {windows[1]['payback_proxy_months']:.2f}; TTM {windows[3]['payback_proxy_months']:.2f} months",'CSV rows 2-14; interval details in calculations.json','matching-window S&M / (net new MRR * ending GM)',missing='Acquisition cohort, gross new-logo MRR, sales lag and attributable spend')
add('P7-05',7,'9-month pilot-to-contract sales cycle','unverifiable','Monthly stocks cannot identify elapsed cohort conversion time','Deck p7 and CSV customer stocks',missing='Pilot start and contract dates')
add('P7-06',7,'$42,000 hardware cost per robot','unverifiable','No bill of materials or invoices supplied','Deck p7 only',missing='Hardware invoices and capital/lease treatment')
for cid,claim in [('P9-01','CEO has 2 prior exits'),('P9-02','VP Customer Ops ran 14 fulfillment centers')]:
    add(cid,9,claim,'unverifiable','Fictional biographies have no supporting records','Deck p9 only',missing='Attributed role/employer/transaction records')
for year,arr in [(2026,2_400_000),(2027,9_000_000),(2028,30_000_000),(2029,100_000_000)]:
    target=next(x for x in future if x['year']==year)
    add('P10-'+str(year),10,f'${arr/1e6:g}M ARR in {year}','projection_unvalidated',f"Requires {target['required_paying_robots_at_current_price']} paying robots at current price; 2026 point is ambiguous actual vs year-end target",'Deck p10; CSV row 14 current baseline','ceil(target ARR / (3500 * 12))',kind='projection',missing='Deployment, conversion, pricing, churn, staffing and funding schedule')
for cid,claim,result,formula in [('P11-01','$18M raise','$18M is an ask, not cash received',''),('P11-02','$90M pre-money','$108M simple post-money; 16.67% simple new-money ownership','90M + 18M; 18M / 108M'),('P11-03','50% R&D','$9M allocation','18M * .50'),('P11-04','30% go-to-market','$5.4M allocation','18M * .30'),('P11-05','20% operations','$3.6M allocation','18M * .20'),('P11-06','12 AEs, 3 regions','Deployment/hiring plan unvalidated',''),('P11-07','LoopBrain v2','Product version milestone; no roadmap supplied','')]:
    add(cid,11,claim,'stated_plan_unvalidated',result,'Deck p11 only',formula,kind='plan',missing='Financing terms, budget and execution schedule')
add('P11-08',11,'Headcount 38 to 85','baseline_supported_plan_unvalidated','38 matches September; 85 is a hiring target (+123.68%)','CSV row 14 (2026-09); deck p11','85 / 38 - 1',kind='plan',missing='Hiring dates and fully loaded compensation')
add('P11-09',11,'24 months runway','unverifiable',f"Current cash / September burn = {cash/last['net_burn_usd']:.2f} months; immediate $18M raise, flat burn = {(cash+raise_usd)/last['net_burn_usd']:.2f} months; 24 months needs average burn <= ${(cash+raise_usd)/24:,.0f}",'CSV row 14; deck p11','cash / forward burn; scenarios in calculations.json',kind='projection',missing='Raise close date, monthly hiring, hardware capex, revenue, collections, fees, working capital and financing model')

manifest={'fictional_teaching_material':True,'data_as_of':'2026-09-30','review_date':'2026-10-17','timezone':'America/Los_Angeles','input_csv':str(args.input.resolve()),'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),'source_row_convention':'Header row 1; data rows 2-14','claims':claims}
(HERE/'calculations.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
(HERE/'claims.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(HERE/'numerical-checks.json').write_text(json.dumps({'fictional_teaching_material':True,'checks':checks,'all_pass':all(c['status']=='pass' for c in checks)},indent=2),encoding='utf-8')
with (HERE/'forward-burn-sensitivity.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=forward[0]);writer.writeheader();writer.writerows(forward)
lines=['# Calculation results','', 'FICTIONAL COMPANY AND DATA - TEACHING MATERIAL', '', 'Reviewed 2026-10-17 (America/Los_Angeles). Monthly data through September 2026.','',f'Paying ARR: ${paying_arr:,.0f}. Pilot-inclusive metric: ${booked_arr:,.0f}.',f"Paying YoY: {metrics['paying_yoy_multiple']:.3f}x (+{metrics['paying_yoy_growth_pct']:.2f}%). September GM: {gm:.0%}.",f"NRR: {metrics['nrr_sep2025_cohort_pct']:.2f}% for the three-customer September 2025 cohort.",'','## CAC payback proxy sensitivity','', '| Spending interval | S&M | Net new MRR | End GM | Proxy months | Monthly GM variant |','|---|---:|---:|---:|---:|---:|']
for w in windows:
    lines.append(f"| {w['spend_period']} | ${w['sales_marketing_usd']:,.0f} | ${w['net_new_mrr_usd']:,.0f} | {gm:.0%} | {w['payback_proxy_months']:.2f} | {w['monthly_margin_weighted_proxy_months']:.2f} |")
lines+=['','~26 months is reproducible for Q3 2026 using ending GM; it is not a unique interval-independent result. It is not the TTM result. All are proxies, not verified acquisition-cohort CAC payback. Monthly GM variant sums each monthly MRR increment times that month\'s GM.','', '## Runway sensitivities','']
for s in runway:lines.append(f"- {s['scenario']}: {s['runway_months']:.2f} months.")
lines += [f"- Linear 24-month hiring ramp (opex proportional to headcount, static September gross profit): cash exhausted around month {ramp_runout:.2f}; ending cash ${balance:,.0f}.",'','All sensitivities are illustrative assumptions, with no separate capex or financing flows. Opex scaling does not establish payroll cost. Do not call them the company forecast.','',f"Checks: {sum(c['status']=='pass' for c in checks)}/{len(checks)} pass. See numerical-checks.json.",f'Claim inventory: {len(claims)} quantitative/time-bound/plan claims. See claims.json.']
(HERE/'calculation-results.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
if not all(c['status']=='pass' for c in checks):raise SystemExit('Numerical checks failed')
