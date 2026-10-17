"""Stage 1: source-limited NVIDIA FY2026 extraction, authored 2026-10-17.
Only reads the approved inputs in this run. Writes financials.md and its own validation.
"""
import json, hashlib, math, re
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "inputs"
source_manifest = json.loads((INPUT / "sources.json").read_text(encoding="utf-8-sig"))
manifest = {s["id"]:s for s in source_manifest}
pages = json.loads((INPUT / "annual-report-pages.json").read_text(encoding="utf-8-sig"))
qtext = {q:(INPUT / (q+"-release.txt")).read_text(encoding="utf-8-sig") for q in ("q2","q3","q4")}
filing = (INPUT / "filing-index.txt").read_text(encoding="utf-8-sig")
sources = {}
def ar(p, heading):
    sid = "AR"+str(p)
    sources[sid] = dict(id=sid, document="NVIDIA FY2026 Form 10-K in 2026 Annual Report",
        printed_page=p, pdf_page=p+88, pdf_index=p+87, heading=heading,
        url=manifest["annual_report"]["url"]+"#page="+str(p+88))
for p,h in [
 (1,"Form 10-K cover (unnumbered cover; logical printed page 1)"),
 (15,"Risk Factors - Risks Related to Demand, Supply, and Manufacturing"),
 (16,"Risk Factors - Risks Related to Demand, Supply, and Manufacturing"),
 (33,"Item 5 - Stock split and Issuer Purchases of Equity Securities"),
 (36,"MD&A - Recent Developments, Future Objectives and Challenges"),
 (37,"MD&A - Investments and Fiscal Year 2026 Summary"),
 (38,"MD&A - Critical Accounting Estimates - Inventories"),
 (41,"MD&A - Concentration of Revenue; Gross Profit and Gross Margin; Operating Expenses"),
 (42,"MD&A - Total Other Income, Net; Income Taxes; Liquidity and Capital Resources"),
 (43,"MD&A - Liquidity and Capital Return to Shareholders"),
 (44,"MD&A - Material Cash Requirements and Other Obligations"),
 (51,"Consolidated Statements of Income"),
 (53,"Consolidated Balance Sheets"),
 (54,"Consolidated Statements of Shareholders' Equity"),
 (55,"Consolidated Statements of Cash Flows"),
 (56,"Note 1 - Organization and Summary of Significant Accounting Policies"),
 (60,"Note 1 - Non-Marketable Equity Securities"),
 (61,"Note 2 - Groq; Note 3 - Stock-Based Compensation"),
 (65,"Note 7 - Cash Equivalents and Marketable Securities"),
 (66,"Note 7 - Cash Equivalents and Marketable Securities; Note 8"),
 (67,"Note 8 - Non-marketable Equity Securities; Note 9 - Balance Sheet Components"),
 (68,"Note 9 - Balance Sheet Components"),
 (69,"Note 10 - Facility Lease Guarantees"),
 (70,"Note 11 - Debt; Note 12 - Commitments and Contingencies - Commitments"),
 (72,"Note 13 - Income Taxes"),
 (73,"Note 13 - FY2026 income tax reconciliation"),
 (74,"Note 13 - FY2025/FY2024 income tax reconciliation"),
 (75,"Note 13 - Deferred tax assets and valuation allowance"),
 (76,"Note 14 - Shareholders' Equity; Note 16 - Segment Information"),
 (77,"Note 16 - Segment Information"),
 (78,"Note 16 - Segment reconciliation, geography, and concentration"),
 (79,"Note 16 - Revenue by End Market; Note 17 - Leases"),
 (85,"Signatures")]:
    ar(p,h)
for q in ("q2","q3","q4"):
    for suffix,heading in [
        ("SUMMARY",{"q2":"Q2 Fiscal 2026 Summary","q3":"Q3 Fiscal 2026 Summary","q4":"Q4 Fiscal 2026 Summary"}[q]),
        ("INTRO","Opening financial results narrative (before quarterly summary)"),
        ("OUTLOOK","Outlook"),
        ("RECON","RECONCILIATION OF GAAP TO NON-GAAP FINANCIAL MEASURES"),
        ("OUTLOOK_RECON","RECONCILIATION OF GAAP TO NON-GAAP OUTLOOK")]:
        sid=q.upper()+"_"+suffix
        sources[sid]=dict(id=sid,document={"q2":"NVIDIA Announces Financial Results for Second Quarter Fiscal 2026","q3":"NVIDIA Announces Financial Results for Third Quarter Fiscal 2026","q4":"NVIDIA Announces Financial Results for Fourth Quarter and Fiscal 2026"}[q],heading=heading,url=manifest[q+"_release"]["url"],printed_page=None,pdf_page=None,pdf_index=None)
sources["Q4_ANNUAL"]=dict(sources["Q4_SUMMARY"],id="Q4_ANNUAL",heading="Fiscal 2026 Summary")
sources["Q4_MEASURES"]=dict(sources["Q4_SUMMARY"],id="Q4_MEASURES",heading="Non-GAAP Measures")
sources["SEC_INDEX"]=dict(id="SEC_INDEX",document="SEC Form 10-K filing index",heading="Filing Detail - Filing Date and Period of Report",url=manifest["filing_index"]["url"],printed_page=None,pdf_page=None,pdf_index=None)

rows=[]
groups={}
def add(g,id,metric,period,segment,value,unit,source,status="reported",formula=None,notes=""):
    r=dict(id=id,metric=metric,period=period,segment=segment,value=value,unit=unit,
           source=source,status=status,formula=formula,notes=notes)
    rows.append(r); groups.setdefault(g,[]).append(r); return r
def pair(g,id,metric,v26,v25,source,unit="USD million",segment="Consolidated",notes="",stock=False,status="reported"):
    for y,v in [(26,v26),(25,v25)]:
        src=source[y-25] if isinstance(source,list) else source
        add(g,id+"_fy"+str(y),metric,("2026-01-25" if y==26 else "2025-01-26") if stock else "FY20"+str(y),segment,v,unit,src,
            "not disclosed" if v is None else status,notes=notes)
def calc(g,id,metric,period,segment,value,unit,source,expression,inputs,notes=""):
    return add(g,id,metric,period,segment,round(value,8),unit,source,"calc",
               {"expression":expression,"inputs":inputs},notes)
def get(id): return next(r["value"] for r in rows if r["id"]==id)
def fmt(v):
    if v is None: return "not disclosed"
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.4f}".rstrip("0").rstrip(".")
def cite(src):
    return "; ".join("["+s+"]" for s in src.split(";"))

# Annual GAAP financial statements, sign-preserving.
for id,name,a,b,unit in [
 ("revenue","Revenue",215938,130497,"USD million"),
 ("cost_revenue","Cost of revenue",62475,32639,"USD million"),
 ("gross_profit","Gross profit",153463,97858,"USD million"),
 ("rd","Research and development",18497,12914,"USD million"),
 ("sga","Sales, general and administrative",4579,3491,"USD million"),
 ("opex","Total operating expenses",23076,16405,"USD million"),
 ("operating_income","Operating income",130387,81453,"USD million"),
 ("interest_income","Interest income",2300,1786,"USD million"),
 ("interest_expense","Interest expense",-259,-247,"USD million"),
 ("other_income","Other income, net",9022,1034,"USD million"),
 ("total_other_income","Total other income, net",11063,2573,"USD million"),
 ("pretax_income","Income before income tax",141450,84026,"USD million"),
 ("income_tax","Income tax expense",21383,11146,"USD million"),
 ("net_income","Net income",120067,72880,"USD million"),
 ("basic_eps","Net income per share - Basic",4.93,2.97,"USD per share"),
 ("diluted_eps","Net income per share - Diluted",4.90,2.94,"USD per share"),
 ("basic_shares","Weighted average shares used in per share computation - Basic",24359,24555,"million shares"),
 ("diluted_shares","Weighted average shares used in per share computation - Diluted",24514,24804,"million shares")]:
    pair("income",id,name,a,b,"AR51",unit)
pair("income","gaap_gm","GAAP gross margin",71.1,75.0,"AR41","%")
pair("income","effective_tax","Effective tax rate",15.1,13.3,"AR42","%")
for y in (26,25):
    for id,name,num,den,unit in [
      ("rd_pct","Research and development / revenue","rd","revenue","%"),
      ("operating_margin","Operating margin","operating_income","revenue","%"),
      ("net_margin","Net margin","net_income","revenue","%")]:
        calc("income",id+"_fy"+str(y),name,"FY20"+str(y),"Consolidated",get(num+"_fy"+str(y))/get(den+"_fy"+str(y))*100,unit,"AR51",num+"/revenue * 100",[num+"_fy"+str(y),den+"_fy"+str(y)])

for id,name,a,b,unit in [
 ("non_gaap_gm","Non-GAAP gross margin",71.3,75.5,"%"),
 ("non_gaap_gp","Non-GAAP gross profit",153994,98505,"USD million"),
 ("non_gaap_opex","Non-GAAP operating expenses",16694,11716,"USD million"),
 ("non_gaap_oi","Non-GAAP operating income",137300,86789,"USD million"),
 ("non_gaap_net_income","Non-GAAP net income",116997,74265,"USD million"),
 ("non_gaap_eps","Non-GAAP diluted earnings per share",4.77,2.99,"USD per share")]:
    pair("margins",id,name,a,b,"Q4_RECON",unit,notes="FY2025/FY2026 basis excludes stock-based compensation. Includes H20 charges/releases; not H20-adjusted.")
pair("margins","inventory_and_commitment_provision","Provisions for inventory and excess inventory purchase obligations",7200,3700,"AR41",notes="Rounded billions converted to USD million. Includes H20 charge; do not add H20 again.")
pair("margins","inventory_provision","Inventory provisions recorded in cost of revenue",4000,1600,"AR67",notes="Rounded billions. Component of broader inventory and excess purchase-obligation provisions.")
pair("margins","excess_purchase_expense","Expense for excess inventory purchase obligations in cost of revenue",3200,2000,"AR68",notes="Approximately; rounded. Rounded component totals need not equal rounded combined provision.")
pair("margins","provision_release","Provision release from sales of previously reserved inventory and settlements of excess inventory purchase obligations",1500,689,"AR41",notes="FY2026 rounded billions; not exclusively H20.")
pair("margins","inventory_net_gm_impact","Net gross-margin effect of inventory provisions and sales/settlements of previously reserved items",-2.6,-2.3,"AR41","percentage points",notes="Company describes an unfavorable 2.6% / 2.3% effect; represented as negative margin points.")
pair("margins","h20_charge_rounded","H20 excess inventory and purchase obligations charge (initial Q1 event, annual narrative)",4500,None,"AR36;AR41",notes="FY2026 narrative rounded; precise Q1 charge is 4,538 in Q2 release. FY2025 comparable H20 charge not disclosed.")
pair("margins","annual_h20_net_exact","Annual H20 charges/(releases), net - exact",None,None,"Q4_RECON",notes="FY2026 footnote gives rounded Q1 charge, exact Q2 release, and insignificant Q3/Q4; no exact annual total. Do not treat insignificant as zero.")
calc("margins","h20_initial_charge_annual_pts","Initial H20 charge / FY2026 revenue (scale illustration)","FY2026","Consolidated",4500/215938*100,"percentage points","AR36;AR51","rounded initial H20 charge / FY2026 revenue * 100",["h20_charge_rounded_fy26","revenue_fy26"],"Approximate initial charge only, not net annual H20 effect, normalized margin, or complete margin bridge.")
pair("margins","blackwell_margin_attribution","Quantified margin impact attributable solely to Blackwell transition",None,None,"AR41",unit="percentage points",notes="Management names transition as a driver but does not quantify an isolated amount. Do not assign residual margin change wholly to Blackwell.")

# Reportable segments, with unallocated costs explicitly separate.
for id,name,seg,a,b in [
 ("cn_revenue","Revenue","Compute & Networking",193479,116193),
 ("graphics_revenue","Revenue","Graphics",22459,14304),
 ("cn_other_items","Other segment items","Compute & Networking",63338,33318),
 ("graphics_other_items","Other segment items","Graphics",13303,9219),
 ("cn_oi","Operating income","Compute & Networking",130141,82875),
 ("graphics_oi","Operating income","Graphics",9156,5085),
 ("segment_oi","Segment operating income","Reportable segments total",139297,87960)]:
    pair("segments",id,name,a,b,"AR77",segment=seg)
for id,name,a,b in [
 ("sbc_bridge","Stock-based compensation expense (segment reconciliation)",-6386,-4737),
 ("unallocated_opex","Unallocated operating expenses",-1997,-1171),
 ("acquisition_bridge","Acquisition-related and other costs",-527,-599)]:
    pair("segments",id,name,a,b,"AR78",segment="Unallocated reconciliation")
pair("segments","all_other_reported","All Other (separately named reported line)",None,None,"AR77;AR78",segment="Unallocated reconciliation",notes="Current annual report does not label an All Other line; use calculated aggregate below, not a third reportable segment.")
for y in (26,25):
    suff="_fy"+str(y)
    calc("segments","all_other_bridge"+suff,"All Other equivalent / aggregate unallocated operating-income bridge","FY20"+str(y),"Unallocated reconciliation",get("operating_income"+suff)-get("segment_oi"+suff),"USD million","AR51;AR78","consolidated operating income - segment operating income",["operating_income"+suff,"segment_oi"+suff],"Calculated analytical label; sum of SBC, unallocated operating expenses, and acquisition-related and other costs; not reported as All Other.")
    for seg,id in [("Compute & Networking","cn"),("Graphics","graphics")]:
        calc("segments",id+"_margin"+suff,"Segment operating margin","FY20"+str(y),seg,get(id+"_oi"+suff)/get(id+"_revenue"+suff)*100,"%","AR77","segment operating income / segment revenue * 100",[id+"_oi"+suff,id+"_revenue"+suff])

for id,name,a,b in [
 ("dc_revenue","Data Center",193737,115186),
 ("dc_compute","Compute",162361,102196),
 ("dc_networking","Networking",31376,12990),
 ("gaming","Gaming",16042,11350),
 ("proviz","Professional Visualization",3191,1878),
 ("automotive","Automotive",2349,1694),
 ("oem_other","OEM and Other",619,389)]:
    pair("platforms",id,"Revenue by End Market - "+name,a,b,"AR79",segment="Data Center subcategory" if id in ("dc_compute","dc_networking") else "End market",notes="End-market disclosure is separate from reportable segment disclosure; avoid adding Data Center and its Compute/Networking subcategories together.")

# Cash flows, returns, investments.
for id,name,a,b in [
 ("cfo","Net cash provided by operating activities",102718,64089),
 ("capex_purchases","Purchases related to property and equipment and intangible assets",6042,3236),
 ("capex_principal","Principal payments on property and equipment and intangible assets",101,129),
 ("cash_buybacks","Payments related to repurchases of common stock",40086,33706),
 ("dividends","Dividends paid",974,834),
 ("equity_taxes","Payments related to employee stock plan taxes",7948,6930),
 ("cash_investing","Net cash used in investing activities",-52228,-20421),
 ("cash_financing","Net cash used in financing activities",-48474,-42359),
 ("cash_change","Change in cash and cash equivalents",2016,1309),
 ("investment_gains_cf","Gains on non-marketable equity securities and publicly-held equity securities, net (economic gain; cash-flow adjustment is negative)",8918,1030),
 ("private_purchases","Purchases of non-marketable equity securities",17502,1486),
 ("private_sales","Proceeds from sales of non-marketable equity securities",84,171),
 ("groq_cash","Groq, Inc. cash payment",13000,0),
 ("cash_taxes","Cash paid for income taxes, net",20288,15118)]:
    pair("cash",id,name,a,b,"AR55",notes="Cash outflows shown as positive amounts for capex, repurchases, dividends, tax payments, and investment purchases; net investing/financing preserve statement signs.")
pair("cash","fcf","Free cash flow",96575,60724,"Q4_RECON",notes="Company-defined non-GAAP FCF = CFO minus PP&E/intangible purchases minus principal payments on those assets.")
pair("cash","capex_narrative","Capital expenditures (rounded MD&A narrative)",6100,3400,"AR44",notes="Rounded narrative corresponds to purchases plus principal payments; preserve precision separately.")
pair("cash","repurchase_cost","Shares repurchased - accounting cost",40388,34015,"AR54",notes="Different basis from cash payments related to repurchases. MD&A rounds to 40.4bn / 34.0bn.")
pair("cash","repurchased_shares","Shares repurchased",282,310,"AR54","million shares")
pair("cash","remaining_auth","Remaining share repurchase authorization",58500,None,"AR76",stock=True,notes="FY2026 rounded; FY2025 year-end remaining authorization not disclosed in approved sources.")
add("cash","new_auth_fy26","Additional share repurchase authorization","2025-08-26","Consolidated",60000,"USD million","AR76",notes="No expiration.")
add("cash","capital_return_reported_fy26","Returned to shareholders - shares repurchased and cash dividends","FY2026","Consolidated",41100,"USD million","Q4_INTRO",notes="Rounded release narrative; cash-flow components sum to 41,060.")
for y in (26,25):
    suff="_fy"+str(y)
    calc("cash","cash_capex_total"+suff,"Cash capital expenditures including principal payments","FY20"+str(y),"Consolidated",get("capex_purchases"+suff)+get("capex_principal"+suff),"USD million","AR55","PP&E/intangible purchases + principal payments",["capex_purchases"+suff,"capex_principal"+suff])
    calc("cash","cash_capital_return"+suff,"Cash returned via repurchases and dividends","FY20"+str(y),"Consolidated",get("cash_buybacks"+suff)+get("dividends"+suff),"USD million","AR55","cash repurchase payments + dividends paid",["cash_buybacks"+suff,"dividends"+suff],"Excludes employee equity tax withholding; uses cash-flow basis.")
    calc("cash","fcf_conversion"+suff,"FCF / net income","FY20"+str(y),"Consolidated",get("fcf"+suff)/get("net_income"+suff)*100,"%","Q4_RECON;AR51","FCF / net income * 100",["fcf"+suff,"net_income"+suff])
    calc("cash","capital_return_fcf"+suff,"Cash capital returned / FCF","FY20"+str(y),"Consolidated",get("cash_capital_return"+suff)/get("fcf"+suff)*100,"%","AR55;Q4_RECON","(cash repurchase payments + dividends paid) / FCF * 100",["cash_capital_return"+suff,"fcf"+suff])
add("cash","post_year_end_buybacks","Post-year-end repurchases","2026-01-26 through 2026-02-20","Consolidated",1500,"USD million","AR76",notes="Rounded; separate from FY2026.")
add("cash","post_year_end_shares","Post-year-end repurchased shares","2026-01-26 through 2026-02-20","Consolidated",8,"million shares","AR76")

for id,name,a,b,src in [
 ("cash_equivalents","Cash and cash equivalents",10605,8589,"AR53"),
 ("marketable_securities","Marketable securities",51951,34621,"AR53"),
 ("cash_marketable","Cash, cash equivalents, and marketable securities",62556,43210,"AR42"),
 ("receivables","Accounts receivable, net",38466,23065,"AR53"),
 ("inventory","Inventories",21403,10080,"AR53"),
 ("prepaid_other_current","Prepaid expenses and other current assets",3180,3771,"AR53"),
 ("ppne","Property and equipment, net",10383,6283,"AR53"),
 ("private_equity","Non-marketable equity securities",22251,3387,"AR53"),
 ("other_assets","Other assets",8301,3038,"AR53"),
 ("total_assets","Total assets",206803,111601,"AR53"),
 ("accounts_payable","Accounts payable",9812,6310,"AR53"),
 ("current_liabilities","Total current liabilities",32163,18047,"AR53"),
 ("longterm_debt","Long-term debt",7469,8463,"AR53"),
 ("debt_total","Debt - net carrying amount",8468,8463,"AR70"),
 ("total_liabilities","Total liabilities",49510,32274,"AR53"),
 ("shareholders_equity","Total shareholders' equity",157293,79327,"AR53"),
 ("raw_materials","Inventories - Raw materials",3807,3408,"AR67"),
 ("wip","Inventories - Work in process",8822,3399,"AR67"),
 ("finished_goods","Inventories - Finished goods",8774,3273,"AR67"),
 ("excess_inventory_obligation","Excess inventory purchase obligations (accrued current liability)",2739,2095,"AR68"),
 ("prepaid_supply","Prepaid manufacturing/supply/capacity agreements - separately quantified balance",None,None,"AR15;AR16;AR53"),
 ("supply_commitments","Manufacturing, supply, and capacity commitments",95200,None,"AR70"),
 ("cloud_commitments","Multi-year cloud service agreement commitments",27000,None,"AR70"),
 ("investment_commitments","Investment commitments",11400,None,"AR70"),
 ("other_commitments","Other commitments",3400,None,"AR70"),
 ("guarantee_gross","Facility lease guarantees - maximum gross exposure",3500,None,"AR69"),
 ("guarantee_escrow","Partners' escrow against facility lease guarantees",712,None,"AR69"),
 ("future_uncommenced_leases","Future obligations for leases expected to commence FY2027-FY2030",22700,None,"AR79")]:
    note=""
    if id=="prepaid_supply": note="Risk discussion says prepaid agreements exist; total prepaid expenses and other current assets is not a proxy for this balance."
    if id in ("supply_commitments","investment_commitments","other_commitments"): note="Rounded billions. Substantially all supply/investment commitments, and majority of other commitments, expected through FY2027. Prior-year comparison unavailable in approved sources. Investment commitments subject to contingencies."
    if id=="cloud_commitments": note="Rounded; supports R&D. Capacity may be reduced, terminated, or sold by CSPs, reducing commitments."
    if id=="guarantee_gross": note="In exchange for warrants; terms 5-7 years, exposure reduces with payments. Escrow mitigates exposure, not a recognized net debt balance. Prior-year amount not disclosed."
    if id=="future_uncommenced_leases": note="Primarily R&D data centers; lease terms 1.8-20 years; separate from recognized operating lease liabilities."
    pair("balance",id,name,a,b,src,stock=True,notes=note)
for y in (26,25):
    suff="_fy"+str(y)
    calc("balance","inventory_days"+suff,"Days of inventory (ending balance / annual cost of revenue)","FY20"+str(y),"Consolidated",get("inventory"+suff)/get("cost_revenue"+suff)*365,"days","AR53;AR51","ending inventory / annual cost of revenue * 365",["inventory"+suff,"cost_revenue"+suff],"Requested convention uses 365, not actual 52-week fiscal-day count; ending balance, not average inventory.")
for year,val in [(2027,7000),(2028,6000),(2029,5000),(2030,5000),(2031,2000),("2032 and thereafter",2000)]:
    add("commitments","cloud_due_"+str(year).replace(" ","_"),"Multi-year cloud service agreement commitments - expected payment","FY"+str(year),"Consolidated",val,"USD million","AR70",notes="As of 2026-01-25; future contractual schedule; rounded.")
pair("investments","public_equity_value","Publicly-held equity securities - total estimated fair value",17726,381,["AR66","AR65"],stock=True,notes="FY2026 includes 12,886 current marketable securities and 4,840 in Other assets; do not add entire amount to cash+marketable securities.")
add("investments","public_equity_current_fy26","Publicly-held equity securities reported in marketable securities","2026-01-25","Consolidated",12886,"USD million","AR65")
add("investments","public_equity_other_assets_fy26","Publicly-held equity securities reported in other assets","2026-01-25","Consolidated",4840,"USD million","AR65",notes="Long-term lock-up through December 2027.")
add("investments","public_equity_short_lockup_fy26","Public equity investments subject to short-term lock-up restrictions","2026-01-25","Consolidated",10500,"USD million","AR65",notes="Rounded; liquidity restriction within the reported portfolio.")
pair("investments","public_equity_unrealized","Net unrealized gains on publicly-held equity securities held at period end",6600,None,"AR65",notes="FY2026 rounded; FY2025 reported not significant, exact amount not disclosed; do not enter zero.")
pair("investments","public_equity_realized","Net realized gains on publicly-held equity securities sold - exact",None,None,"AR65",notes="Reported not significant for both years, not zero. Complete realized/unrealized split of total Other income is not disclosed.")
pair("investments","private_unrealized","Non-marketable equity securities - Unrealized gains",2369,816,"AR67")
pair("investments","private_losses","Non-marketable equity securities - Impairments and unrealized losses",-101,-59,"AR67")
pair("investments","private_net_additions","Non-marketable equity securities - Net additions",17444,1309,"AR67")
pair("investments","private_reclassification","Non-marketable equity securities - Reclassification",-848,0,"AR67",notes="Reclassification to marketable following public market trading; dash in FY2025 table denotes no reclassification.")
pair("investments","private_realized","Non-marketable equity securities - realized gains/losses separately quantified",None,None,"AR60;AR67",notes="Realized/unrealized changes recognized in Other income, net; table does not separately quantify realized gains.")
add("investments","private_funds_invested_fy26","Invested in private companies and infrastructure funds","FY2026","Consolidated",17500,"USD million","AR37",notes="Rounded narrative; includes AI model makers buying directly or through CSPs. Purchases cash-flow line 17,502 preserved separately.")
add("investments","fund_commitment_separate_fy26","Infrastructure-fund commitments separately quantified","2026-01-25","Consolidated",None,"USD million","AR37;AR70","not disclosed",notes="Combined investment commitments disclosed; fund-only portion unavailable.")
add("investments","groq_total_consideration","Groq consideration (cash plus stated future payment)","December 2025 transaction","Compute & Networking",17000,"USD million","AR61",notes="13.0bn paid at closing + 4.0bn inclusive of imputed interest payable within one year; use disclosed components. No equity interests, products or customer contracts purchased.")
add("investments","groq_future_payment","Groq future consideration payable within one year","2026-01-25","Compute & Networking",4000,"USD million","AR61",notes="Inclusive of imputed interest; accrued purchase consideration carrying value is separately 3,921.")
add("investments","openai_transaction_size","OpenAI investment/partnership transaction amount in current negotiations","As of FY2026 filing","Consolidated",None,"USD million","AR44","not disclosed",notes="Agreement being finalized; no assurance of agreement or completed transaction in filing. Do not imply consummation.")

# Tax items are not all directly comparable between years due to new disclosure presentation.
add("tax","valuation_release_fy26","State deferred-tax valuation allowance release","FY2026","Consolidated",711,"USD million","AR42;AR75")
add("tax","obbba_expense_fy26","Tax expense from OBBBA","FY2026","Consolidated",48,"USD million","Q4_RECON",notes="Explicitly identified in non-GAAP reconciliation; not a quantified total long-run OBBBA benefit/cost.")
for id,name,a,b,src in [
 ("fddei_tax_benefit","Foreign-derived deduction eligible income tax benefit",-4208,-2976,"AR73;AR74"),
 ("sbc_tax_benefit","Stock-based compensation tax benefit",-1475,-2097,"AR73;AR74")]:
    pair("tax",id,name,a,b,src,notes="Tax reconciliation classification; do not interpret as all tax effects of related expense.")
pair("tax","valuation_allowance","Deferred tax valuation allowance",768,1610,"AR75",stock=True)
pair("tax","gross_unrecognized_tax","Gross unrecognized tax benefits",4420,2861,"AR76",stock=True)
pair("tax","tax_credit_line","Tax credits (FY2026); U.S. federal research and development tax credit (FY2025)",-1933,-990,"AR73;AR74",notes="Non-identical line labels; FY2026 broader 'Tax credits', FY2025 'U.S. federal research and development tax credit'. Do not use as a like-for-like growth series.")

# Geography: same headquarters basis for both annual periods.
for id,geo,a,b in [("geo_us","United States",149617,77482),("geo_taiwan","Taiwan",42345,23600),("geo_china","China (including Hong Kong)",19677,25048),("geo_other","Other",4299,4367)]:
    pair("geography",id,"Geographic Revenue based upon Customer Headquarters Location - "+geo,a,b,"AR78",segment="Customer headquarters geography",notes="FY2025 recast; end customer and shipping locations may differ.")
pair("geography","outside_us_share","Revenue from customers headquartered outside United States",31,41,"AR78","%",segment="Customer headquarters geography",notes="Rounded reported shares.")
pair("geography","billing_geo","Annual revenue by billing location",None,None,"AR78",segment="Billing geography",notes="Not disclosed in approved FY2026 annual report or supplied releases; do not substitute headquarters data.")
add("geography","taiwan_dc_end_customers","Taiwan-headquartered customer Data Center revenue attributed to US/Europe end customers","FY2026","Customer headquarters geography",76,"%","AR78",notes="Company estimate; denominator is Taiwan-headquartered Data Center revenue, not all Taiwan revenue.")
for id,period,value in [("direct_largest_fy26","FY2026",22),("direct_second_fy26","FY2026",14),("direct_largest_fy25","FY2025",12),("direct_second_fy25","FY2025",11),("direct_third_fy25","FY2025",11)]:
    add("concentration",id,"Direct customer share of total revenue - "+("largest" if "largest" in id else "second disclosed" if "second" in id else "third disclosed"),period,"Primarily Compute & Networking",value,"%","AR78",notes="Anonymous customers; order labels do not establish that the same customer appears in both years.")
pair("concentration","indirect_threshold","Threshold met by some individually significant indirect customers",10,None,"AR41","%",segment="Indirect customers",notes="Current annual report says 10% OR MORE, not an exact customer share. Indirect revenue estimated; identities and exact percentages not disclosed. FY2025-specific threshold comparison is not separately disclosed in approved sources.")
pair("concentration","indirect_exact","Largest indirect customer revenue share - exact",None,None,"AR41","%",segment="Indirect customers",notes="Not disclosed. One unnamed AI research/deployment company described as contributing a meaningful FY2026 amount through cloud purchases.")
for id,period,val in [("ar_customer1_fy26","2026-01-25",25),("ar_customer2_fy26","2026-01-25",18),("ar_customer3_fy26","2026-01-25",13),("ar_customer1_fy25","2025-01-26",17),("ar_customer2_fy25","2025-01-26",16)]:
    add("concentration",id,"Direct customer concentration in accounts receivable - "+id.split("_")[1],period,"Consolidated",val,"%","AR67",notes="Accounts-receivable share, not revenue share; identities not disclosed.")

# Quarterly FY2026 actuals; exact dollars from summary tables.
quarter_data=[
 ("Q1 FY2026",1,"Q2_SUMMARY",44062,60.5,61.0,5030,3583,21638,18775,0.76,26_668),
 ("Q2 FY2026",2,"Q2_SUMMARY",46743,72.4,72.7,5413,3795,28440,26422,1.08,33_853),
 ("Q3 FY2026",3,"Q3_SUMMARY",57006,73.4,73.6,5839,4215,36010,31910,1.30,41_849),
 ("Q4 FY2026",4,"Q4_SUMMARY",68127,75.0,75.2,6794,5102,44299,42960,1.76,51_093)]
for period,q,src,rev,gm,ngm,opx,nopx,oi,ni,eps,gp in quarter_data:
    for key,metric,value,unit in [
      ("revenue","Revenue",rev,"USD million"),("gaap_gm","GAAP gross margin",gm,"%"),("non_gaap_gm","Non-GAAP gross margin",ngm,"%"),
      ("opex","GAAP operating expenses",opx,"USD million"),("non_gaap_opex","Non-GAAP operating expenses",nopx,"USD million"),
      ("oi","GAAP operating income",oi,"USD million"),("net_income","GAAP net income",ni,"USD million"),("eps","GAAP diluted earnings per share",eps,"USD per share")]:
        add("quarterly",key+"_q"+str(q)+"fy26",metric,period,"Consolidated",value,unit,src,notes="Historical actual, not latest quarter as of execution date. FY2026 non-GAAP excludes SBC but includes H20 charges/releases.")
    add("quarterly","gp_q"+str(q)+"fy26","GAAP gross profit",period,"Consolidated",gp,"USD million",src.replace("SUMMARY","RECON"))
for q,gm in [(1,71.3),(2,72.3)]:
    add("quarterly","non_gaap_gm_ex_h20_q"+str(q)+"fy26","Non-GAAP gross margin, as adjusted to exclude H20 related charges/releases, net","Q"+str(q)+" FY2026","Consolidated",gm,"%","Q2_RECON",notes="Separate company-reported H20-adjusted metric; do not relabel standard non-GAAP gross margin.")
for q,val in [(1,4538),(2,-180),(3,None),(4,None)]:
    add("quarterly","h20_net_q"+str(q)+"fy26","H20 related charges/(releases), net","Q"+str(q)+" FY2026","Consolidated",val,"USD million","Q2_RECON" if q<3 else "Q4_RECON","reported" if val is not None else "not disclosed",notes="Exact Q1/Q2 table values. Q3/Q4 reported insignificant, exact amounts not disclosed; not zero.")
add("quarterly","h20_outside_china_q2","Unrestricted H20 sales to a customer outside China","Q2 FY2026","Consolidated",650,"USD million","Q2_INTRO",notes="Approximately; associated with 180m reserve release.")
add("quarterly","h20_china_q2","H20 sales to China-based customers","Q2 FY2026","Consolidated",0,"USD million","Q2_INTRO",notes="Explicitly no H20 sales to China-based customers.")
add("quarterly","h20_license_revenue_fy26","H20 revenue under August 2025 US government licenses","FY2026","Consolidated",60,"USD million","AR36",notes="Approximately; not all H20 revenue globally.")
add("quarterly","h200_license_revenue_at_filing","Revenue under February 2026 H200 licensing program","As of FY2026 filing","Consolidated",0,"USD million","AR36",notes="No revenue to date under program; subsequent-to-year-end disclosure. Small licensed shipments; import permission uncertain.")
add("quarterly","h200_tariff","Tariff upon US importation under new H200 license inspection process","As of FY2026 filing","Consolidated",25,"%","AR36",notes="License requires US inspection before shipment to customer; statement is as of filing, not current trade-policy advice.")

# Forward-looking guidance, always anchored to release date.
for id,metric,value,unit,src,note in [
 ("q4_guidance_revenue","Revenue guidance midpoint",65000,"USD million","Q3_OUTLOOK","Plus/minus 2%."),
 ("q4_guidance_revenue_tolerance","Revenue guidance tolerance",2,"%","Q3_OUTLOOK","Relative tolerance around midpoint."),
 ("q4_guidance_gaap_gm","GAAP gross-margin guidance midpoint",74.8,"%","Q3_OUTLOOK","Plus/minus 50 basis points."),
 ("q4_guidance_ng_gm","Non-GAAP gross-margin guidance midpoint",75.0,"%","Q3_OUTLOOK","Plus/minus 50 basis points."),
 ("q4_guidance_gm_tolerance","Gross-margin guidance tolerance",50,"basis points","Q3_OUTLOOK","Applies to both GAAP and non-GAAP."),
 ("q4_guidance_gaap_opex_table","GAAP operating-expense guidance - reconciliation table",6650,"USD million","Q3_OUTLOOK_RECON","Preserve exact table precision; narrative says approximately 6.7bn."),
 ("q4_guidance_gaap_opex_narrative","GAAP operating-expense guidance - rounded narrative",6700,"USD million","Q3_OUTLOOK","Approximately; use 6,650 table value for precise comparison."),
 ("q4_guidance_ng_opex","Non-GAAP operating-expense guidance",5000,"USD million","Q3_OUTLOOK_RECON","Approximately."),
 ("q4_guidance_other_income","GAAP/non-GAAP other income and expense guidance",500,"USD million","Q3_OUTLOOK","Income; excludes gains/losses from non-marketable and publicly-held equity securities."),
 ("q4_guidance_tax","GAAP/non-GAAP tax-rate guidance midpoint",17,"%","Q3_OUTLOOK","Plus/minus 1 percentage point, excluding discrete items."),
 ("q4_guidance_tax_tolerance","Tax-rate guidance tolerance",1,"percentage point","Q3_OUTLOOK","Excludes discrete items.")]:
    add("guidance",id,metric,"Q4 FY2026 guidance issued 2025-11-19","Consolidated",value,unit,src,notes="FORWARD-LOOKING WHEN ISSUED. "+note)
for id,metric,value,unit,src,note in [
 ("q1fy27_guidance_revenue","Revenue guidance midpoint",78000,"USD million","Q4_OUTLOOK","Plus/minus 2%."),
 ("q1fy27_guidance_revenue_tolerance","Revenue guidance tolerance",2,"%","Q4_OUTLOOK","Relative tolerance around midpoint."),
 ("q1fy27_china_dc_assumption","Assumed China Data Center compute revenue",0,"USD million","Q4_OUTLOOK","Outlook assumption, not a reported result."),
 ("q1fy27_guidance_gaap_gm","GAAP gross-margin guidance midpoint",74.9,"%","Q4_OUTLOOK","Plus/minus 50 basis points."),
 ("q1fy27_guidance_ng_gm","Non-GAAP gross-margin guidance midpoint",75.0,"%","Q4_OUTLOOK","Plus/minus 50 basis points; new basis includes SBC."),
 ("q1fy27_guidance_gm_tolerance","Gross-margin guidance tolerance",50,"basis points","Q4_OUTLOOK","Both measures."),
 ("q1fy27_sbc_gm","Stock-based compensation impact included in gross-margin guidance",0.1,"percentage point","Q4_OUTLOOK_RECON","Company states 0.1%; included, not excluded."),
 ("q1fy27_guidance_gaap_opex","GAAP operating-expense guidance",7700,"USD million","Q4_OUTLOOK_RECON","Approximately."),
 ("q1fy27_guidance_ng_opex","Non-GAAP operating-expense guidance",7500,"USD million","Q4_OUTLOOK_RECON","Approximately; new basis includes SBC."),
 ("q1fy27_sbc_opex","Stock-based compensation expense included in operating-expense guidance",1900,"USD million","Q4_OUTLOOK_RECON","Included in both measures."),
 ("q1fy27_guidance_other_income","Other income and expense guidance",None,"USD million","Q4_OUTLOOK","Not separately disclosed in this release."),
 ("q1fy27_guidance_tax","Q1-specific tax-rate guidance",None,"%","Q4_OUTLOOK","Release provides full-FY2027 tax outlook; do not relabel it Q1-only.")]:
    add("guidance",id,metric,"Q1 FY2027 guidance issued 2026-02-25","Consolidated",value,unit,src,"reported" if value is not None else "not disclosed",notes="FORWARD-LOOKING WHEN ISSUED. "+note)
for id,metric,val in [("fy27_tax_low","Full-year GAAP/non-GAAP tax-rate guidance - low",17),("fy27_tax_high","Full-year GAAP/non-GAAP tax-rate guidance - high",19)]:
    add("guidance",id,metric,"FY2027 guidance issued 2026-02-25","Consolidated",val,"%","Q4_OUTLOOK",notes="FORWARD-LOOKING WHEN ISSUED. Excludes discrete items and material tax-environment changes. Full fiscal year, not Q1-only.")
for key,val,formula,inputs,unit in [
 ("q4_revenue_beat_pct",(68127/65000-1)*100,"actual revenue / guidance midpoint - 1, multiplied by 100",["revenue_q4fy26","q4_guidance_revenue"],"%"),
 ("q4_revenue_beat_amount",68127-65000,"actual revenue - guidance midpoint",["revenue_q4fy26","q4_guidance_revenue"],"USD million"),
 ("q4_revenue_guidance_low",65000*.98,"guidance midpoint * (1 - 2%)",["q4_guidance_revenue","q4_guidance_revenue_tolerance"],"USD million"),
 ("q4_revenue_guidance_high",65000*1.02,"guidance midpoint * (1 + 2%)",["q4_guidance_revenue","q4_guidance_revenue_tolerance"],"USD million"),
 ("q4_gaap_gm_delta",75.0-74.8,"actual GAAP GM - guidance midpoint",["gaap_gm_q4fy26","q4_guidance_gaap_gm"],"percentage points"),
 ("q4_ng_gm_delta",75.2-75.0,"actual non-GAAP GM - guidance midpoint",["non_gaap_gm_q4fy26","q4_guidance_ng_gm"],"percentage points"),
 ("q4_gaap_opex_delta",6794-6650,"actual GAAP opex - reconciliation-table guidance",["opex_q4fy26","q4_guidance_gaap_opex_table"],"USD million"),
 ("q4_ng_opex_delta",5102-5000,"actual non-GAAP opex - guidance",["non_gaap_opex_q4fy26","q4_guidance_ng_opex"],"USD million"),
 ("q4_gaap_etr",7437/50397*100,"income tax expense / income before income tax * 100",["q4_actual_tax_expense","q4_actual_pretax"],"%")]:
    calc("guidance",key,key.replace("_"," "),"Q4 FY2026 actual versus 2025-11-19 guidance","Consolidated",val,unit,"Q3_OUTLOOK;Q3_OUTLOOK_RECON;Q4_SUMMARY;Q4_RECON",formula,inputs,"GAAP actual tax includes discrete items, unlike guidance; other measures use corresponding disclosed basis.")
for id,metric,val in [("q4_actual_tax_expense","Q4 GAAP income tax expense",7437),("q4_actual_pretax","Q4 GAAP income before income tax",50397),("q4_actual_other_income","Q4 GAAP total other income, net",6098),("q4_actual_equity_gains","Q4 gains from non-marketable and publicly-held equity securities, net",5491),("q4_actual_ng_other_income","Q4 non-GAAP total other income, net",620)]:
    # Income-statement fields use a specific exact release heading.
    sid="Q4_INCOME" if id in ("q4_actual_tax_expense","q4_actual_pretax") else "Q4_RECON"
    add("guidance",id,metric,"Q4 FY2026","Consolidated",val,"USD million",sid,notes="Historical actual. Non-GAAP other income also adjusts other expense; not simply identical to guidance exclusions.")
sources["Q4_INCOME"]=dict(sources["Q4_SUMMARY"],id="Q4_INCOME",heading="CONDENSED CONSOLIDATED STATEMENTS OF INCOME")
calc("guidance","q4_actual_other_ex_equity","Q4 GAAP other income excluding disclosed equity gains","Q4 FY2026","Consolidated",6098-5491,"USD million","Q4_RECON","GAAP total other income - equity gains",["q4_actual_other_income","q4_actual_equity_gains"],"607m versus approximately 500m prior guidance on equity-gains-excluded basis; non-GAAP reported 620m differs by 13m other adjustments.")
for name,val,expr in [("low",78000*.98,"midpoint * (1 - 2%)"),("high",78000*1.02,"midpoint * (1 + 2%)")]:
    calc("guidance","q1fy27_revenue_"+name,"Revenue guidance range - "+name,"Q1 FY2027 guidance issued 2026-02-25","Consolidated",val,"USD million","Q4_OUTLOOK",expr,["q1fy27_guidance_revenue","q1fy27_guidance_revenue_tolerance"],"FORWARD-LOOKING WHEN ISSUED; not actual.")

# Reproducible verification of key totals.
checks=[]
def check(name,actual,expected,source,tol=1e-7,note=""):
    ok=abs(actual-expected)<=tol
    checks.append(dict(name=name,actual=actual,expected=expected,difference=actual-expected,passed=ok,tolerance=tol,source=source,note=note))
    if not ok: raise AssertionError(name)
for y in (26,25):
    s="_fy"+str(y)
    check("income_gross_profit"+s,get("revenue"+s)-get("cost_revenue"+s),get("gross_profit"+s),"AR51")
    check("income_opex"+s,get("rd"+s)+get("sga"+s),get("opex"+s),"AR51")
    check("income_operating"+s,get("gross_profit"+s)-get("opex"+s),get("operating_income"+s),"AR51")
    check("income_other"+s,get("interest_income"+s)+get("interest_expense"+s)+get("other_income"+s),get("total_other_income"+s),"AR51")
    check("income_pretax"+s,get("operating_income"+s)+get("total_other_income"+s),get("pretax_income"+s),"AR51")
    check("income_net"+s,get("pretax_income"+s)-get("income_tax"+s),get("net_income"+s),"AR51")
    check("segment_revenue"+s,get("cn_revenue"+s)+get("graphics_revenue"+s),get("revenue"+s),"AR77")
    check("segment_oi"+s,get("cn_oi"+s)+get("graphics_oi"+s),get("segment_oi"+s),"AR77")
    check("segment_bridge"+s,get("segment_oi"+s)+get("sbc_bridge"+s)+get("unallocated_opex"+s)+get("acquisition_bridge"+s),get("operating_income"+s),"AR78")
    check("platform_revenue"+s,sum(get(k+s) for k in ("dc_revenue","gaming","proviz","automotive","oem_other")),get("revenue"+s),"AR79")
    check("data_center"+s,get("dc_compute"+s)+get("dc_networking"+s),get("dc_revenue"+s),"AR79")
    check("geographic_revenue"+s,sum(get(k+s) for k in ("geo_us","geo_taiwan","geo_china","geo_other")),get("revenue"+s),"AR78")
    check("inventory"+s,sum(get(k+s) for k in ("raw_materials","wip","finished_goods")),get("inventory"+s),"AR67")
    check("cash_marketable"+s,get("cash_equivalents"+s)+get("marketable_securities"+s),get("cash_marketable"+s),"AR42;AR53")
    check("fcf"+s,get("cfo"+s)-get("capex_purchases"+s)-get("capex_principal"+s),get("fcf"+s),"AR55;Q4_RECON")
    check("balance_sheet"+s,get("total_liabilities"+s)+get("shareholders_equity"+s),get("total_assets"+s),"AR53")
    check("net_cash_change"+s,get("cfo"+s)+get("cash_investing"+s)+get("cash_financing"+s),get("cash_change"+s),"AR55")
    check("non_gaap_income"+s,get("non_gaap_gp"+s)-get("non_gaap_opex"+s),get("non_gaap_oi"+s),"Q4_RECON")
    check("rounded_diluted_eps"+s,round(get("net_income"+s)/get("diluted_shares"+s),2),get("diluted_eps"+s),"AR51")
check("quarter_revenue_sum",sum(get("revenue_q"+str(q)+"fy26") for q in (1,2,3,4)),get("revenue_fy26"),"Q2_SUMMARY;Q3_SUMMARY;Q4_SUMMARY")
check("quarter_gp_sum",sum(get("gp_q"+str(q)+"fy26") for q in (1,2,3,4)),get("gross_profit_fy26"),"Q2_RECON;Q3_RECON;Q4_RECON")
check("quarter_net_income_sum",sum(get("net_income_q"+str(q)+"fy26") for q in (1,2,3,4)),get("net_income_fy26"),"Q2_SUMMARY;Q3_SUMMARY;Q4_SUMMARY")
check("cloud_schedule",sum(r["value"] for r in groups["commitments"]),27000,"AR70")
check("private_equity_rollforward_fy26",3387+17444+2369-848-101,22251,"AR67")
check("private_equity_rollforward_fy25",1321+1309+816-59,3387,"AR67")
check("public_equity_balance",12886+4840,17726,"AR65")
check("capital_return_rounding",round((40086+974)/1000,1),41.1,"AR55;Q4_INTRO")
# Data-shape and input-reference checks.
ids=[r["id"] for r in rows]
assert len(ids)==len(set(ids))
for r in rows:
    assert r["status"] in ("reported","calc","not disclosed")
    assert r["value"] is None or isinstance(r["value"],(int,float))
    assert r["status"]!="not disclosed" or r["value"] is None
    assert all(s in sources for s in r["source"].split(";")),r
    if r["status"]=="calc":
        assert r["formula"] and all(k in ids for k in r["formula"]["inputs"]),r
assert "2026-02-25" in filing and "2026-01-25" in filing
assert "For the fiscal year ended January" in pages[88]["text"] and "2026" in pages[88]["text"]
for p in (51,53,55,77,78,79):
    assert pages[p+87]["pdf_page"]==p+88
    assert pages[p+87]["text"].rstrip().endswith(str(p))
# Explicit reporting precision observations; not failures or hidden corrections.
rounding_notes=[
 dict(name="Quarter GAAP opex total",sum=5030+5413+5839+6794,annual=23076,status="exact"),
 dict(name="Quarter non-GAAP opex total",sum=3583+3795+4215+5102,annual=16694,status="difference of 1m from reported rounded quarterly data; preserve source values"),
 dict(name="Q1/Q2 H20",q1_table=4538,q1_annual_narrative=4500,q2_release=-180,status="different precision; annual exact net absent"),
 dict(name="Inventory provision components FY2025",components_sum=1600+2000,combined=3700,status="rounded narrative components; do not force exact equality"),
 dict(name="Q4 prior GAAP opex guidance",reconciliation=6650,narrative_approx=6700,status="both preserved; exact comparison uses reconciliation"),
 dict(name="Repurchase bases",fy26_cash=40086,fy26_accounting=40388,status="not interchangeable; timing/tax basis differences not fully quantified")
]
caveats=[
 "This is a historical FY2026 annual-report dataset, executed 2026-10-17. FY2026 ended 2026-01-25 and the 10-K was filed 2026-02-25 [AR1; SEC_INDEX]. Q4 FY2026 is not described as the latest quarter on the execution date. Later actuals were outside the source scope.",
 "The full annual-report PDF contains annual-review/proxy front matter. The Form 10-K begins at PDF page 89 (index 88), logically page 1; the cover does not print a page number. Verified numbered 10-K pages follow PDF page = printed page + 88 and PDF index = printed page + 87. Printed 51 = PDF 139/index 138; printed 77 = PDF 165/index 164. Financial citations use the 10-K printed pages, not the proxy pagination.",
 "Amounts are USD million unless shown otherwise. Exact table values are retained; rounded billion disclosures are converted to million and labeled. Parentheses retain expense/outflow signs where applicable. Cash spending metrics show positive spending amounts with an explicit note. Percent changes differ from percentage-point changes.",
 "Reported segments are Compute & Networking and Graphics [AR77]. End markets are a different disclosure [AR79]. Data Center is not identical to Compute & Networking. Data Center Compute plus Networking is a subtotal, not additional revenue. Segment expenses exclude selected corporate costs; segment margins are not consolidated margins.",
 "The current annual report has no separately named All Other line. The analytical All Other equivalent is a calculated negative bridge, not a third segment [AR77; AR78].",
 "Management attributes margin decline to the Hopper HGX-to-Blackwell full-scale datacenter transition and the H20 charge [AR41]. Broad inventory provisions include H20. Reserve releases mitigate some charges. No complete quantitative bridge or isolated Blackwell impact is disclosed; do not attribute the residual entirely to Blackwell.",
 "FY2026 standard non-GAAP margins still include H20 charges/releases. H20-adjusted Q1/Q2 margins are separate company measures. The exact Q1 H20 charge is 4,538 in the Q2 reconciliation versus rounded 4.5bn in annual narrative; Q3/Q4 effects are insignificant, not zero [Q2_RECON; Q4_RECON; AR41].",
 "FCF follows the company definition: CFO less purchases related to PP&E/intangible assets less principal payments on those assets [Q4_MEASURES]. It does not subtract Groq's separately classified payment or investment purchases. Do not present FCF as cash left after all investments. Cash return uses cash repurchase payments plus dividends, not the accounting repurchase-cost line [AR54; AR55].",
 "Geography is based on direct-customer headquarters; prior years are recast after the change in Q3 FY2026 [AR78]. It is not billing, shipping, deployment, or end-use geography. Billing-basis annual data are not disclosed in the approved sources. The Taiwan end-customer estimate applies only to Taiwan-headquartered Data Center revenue.",
 "Concentration remains anonymous. The largest disclosed direct-customer shares are 22% in FY2026 and 12% in FY2025 [AR78]; this does not establish a ten-point increase for the same customer. Do not add direct and indirect shares, or equate accounts-receivable concentration with revenue concentration.",
 "Other income includes large investment gains [AR42; AR65; AR67]. Public unrealized gains and private unrealized changes are disclosed at differing precision; a complete exact realized/unrealized decomposition is unavailable. Not significant is recorded as not disclosed numerically, never zero.",
 "Prepaid supply balances are not separately quantified. Total prepaid expenses and other current assets is broader and cannot stand in for them [AR15; AR16; AR53]. Prior-year supply/cloud/investment commitments and guarantee comparatives are not disclosed in the approved sources; do not retrieve them from prior demo artifacts or estimate them.",
 "Commitments, recognized liabilities, portfolio balances, annual purchases, escrow and contingent guarantees are different measures. Do not sum them into one debt or spending figure. Facility guarantees support partner buildouts in exchange for warrants; partner escrow mitigates contingent exposure [AR69].",
 "Q4 FY2026 prior GAAP opex outlook is 6,650 in the reconciliation versus approximately 6.7bn in narrative [Q3_OUTLOOK_RECON; Q3_OUTLOOK]. Use the former for precise variance. Q4 revenue exceeded the 65bn midpoint and upper bound; gross margins were within their stated bands. Tax guidance excluded discrete items, so the actual GAAP tax rate is not a clean beat/miss comparison.",
 "Q1 FY2027 guidance was forward-looking as of 2026-02-25, not an actual result or current outlook. Its non-GAAP basis includes SBC, unlike FY2026. The 17%-19% tax range is full FY2027, not Q1-only [Q4_OUTLOOK; Q4_OUTLOOK_RECON].",
 "No financial-statement error correction/restatement is indicated on the 10-K cover [AR1]. Geography prior periods were recast [AR78]; non-marketable equity was reclassified from Other assets to a separate line with no total-asset or cash-flow impact [AR56]. New tax disclosure rules were adopted prospectively [AR72]. These presentation changes are not a profit restatement.",
 "All share/per-share figures are retrospectively adjusted for the June 2024 ten-for-one stock split [AR33]. FY2026 and FY2025 are both 52-week years; FY2027 is a 53-week year with a 14-week fourth quarter [AR56].",
 "PDF printed page 40 / PDF128 has corrupt extracted font encoding. No figures were transcribed from its corrupt text; clean Note 16 data and calculated ratios from the income statement are used instead. Parent independently visually spot-checks original PDF financial pages; this stage relies on mechanical extraction and complete relevant-page reading."
]
narratives={
 "income":"Consolidated GAAP statements are authoritative for the annual totals. R&D growth is attributed to compensation/benefits and compute/infrastructure: the reported increases were 29% and 79%, respectively [AR41]. SG&A growth is attributed primarily to compensation and benefits [AR42].",
 "margins":"Keep company-stated drivers distinct from analytical calculations. The initial H20 annual-revenue scale illustration is not a normalized margin or a complete year-over-year bridge. Inventory-related effects are already embedded in GAAP gross profit.",
 "segments":"The segment bridge subtracts unallocated costs to reach consolidated operating income, then adds total other income to reach pretax income. Expenses in the reportable-segment tables are not the consolidated R&D/SG&A lines.",
 "platforms":"Preserve the reported end-market names. Do not interchange these with reportable segments or infer a one-to-one mapping.",
 "cash":"FCF definition: GAAP operating cash flow less purchases of PP&E/intangibles and less principal payments on those assets [Q4_MEASURES]. Repurchase cost and repurchase cash payments remain separate.",
 "balance":"Balances are fiscal-year-end stocks; commitments and guarantees are separate contractual or contingent measures. Supply agreements may be cancellable, reschedulable or adjustable before firm orders, with possible additional costs [AR70].",
 "investments":"Management states investments include AI model makers purchasing NVIDIA products directly or through CSPs [AR37]. This is ecosystem exposure, not proof that purchases are artificial or circular. Other income grew primarily because of unrealized gains, including Intel common stock [AR42].",
 "tax":"Reported effective tax-rate increase reflects lower tax benefits as a percentage of higher pretax income. Benefit sources include FDDEI, stock compensation, lower-tax jurisdictions and federal research credit [AR42]. FY2026 tax disaggregation differs from FY2025 [AR72; AR73; AR74].",
 "geography":"Use headquarters geography consistently for both years; annual FY2025 amounts have been recast [AR78].",
 "concentration":"Anonymous disclosures; direct, indirect and receivables concentration have different denominators and cannot be summed.",
 "quarterly":"Historical Q1-Q4 FY2026 actuals. Q1 is explicitly supplied by the Q2 release comparative/reconciliation table, not estimated by subtraction. Annual margin is revenue-weighted through gross profit, not an unweighted mean of rounded quarterly percentages.",
 "guidance":"Every outlook row is forward-looking as of its source release date. Q4 actual comparisons use source precision and distinguish excluded equity gains and tax discrete items. FY2027 non-GAAP includes stock compensation [Q4_OUTLOOK].",
 "commitments":"Contractual expected cloud-service payment schedule as of FY2026 year end. Rounded values sum to the reported total; this is not realized cash spending."
}
# Add two quantitative driver rows named in the narrative.
add("margins","rd_comp_growth_fy26","R&D compensation and benefits expense increase","FY2026 vs FY2025","Consolidated",29,"%","AR41",notes="Includes stock-based compensation; stated expense driver.")
add("margins","rd_compute_growth_fy26","R&D compute and infrastructure increase","FY2026 vs FY2025","Consolidated",79,"%","AR41",notes="Stated expense driver.")
# Groq total consideration is a calculated sum, preserving the filing's component disclosure.
next(r for r in rows if r["id"]=="q4_gaap_etr")["source"]="Q3_OUTLOOK;Q4_INCOME"
groq_row=next(r for r in rows if r["id"]=="groq_total_consideration")
groq_row.update(status="calc",formula={"expression":"cash paid at closing + future consideration inclusive of imputed interest","inputs":["groq_cash_fy26","groq_future_payment"]})
# Metadata provenance limited to approved input list.
allowed_names=["10K-NVDA.pdf","annual-report-pages.json","annual-report.txt","q2-release.html","q2-release.txt","q3-release.html","q3-release.txt","q4-release.html","q4-release.txt","sources.json","filing-index.html","filing-index.txt"]
provenance=[]
for name in allowed_names:
    p=INPUT/name
    provenance.append(dict(file="inputs/"+name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
for item in source_manifest:
    actual=next(p for p in provenance if p["file"]==item["file"])
    assert actual["sha256"]==item["sha256"],item["file"]

out=["# NVIDIA FY2026 financials and semiconductor KPIs",
     "",
     "Extraction stage 1 | Run date: 2026-10-17 | Historical annual-report snapshot, not latest-quarter reporting.",
     "",
     "FY2026 ended **January 25, 2026**; FY2025 ended **January 26, 2025** [AR51]. The Form 10-K filing date is **February 25, 2026** [SEC_INDEX]. All financial values below are source-reported unless explicitly marked **calc**. Missing numerical disclosures are **not disclosed**, not zero.",
     "",
     "## Reading and source conventions",
     "",
     "Each source ID resolves to an exact page or release heading in the source map below. Annual citations include printed 10-K page, 1-based PDF page, and zero-based PDF index. Release-only values have official release URLs and headings, never invented PDF pages. The machine-readable rows reuse the same source IDs.",
     "",
     "## Source map","",
     "| ID | Exact locator / heading | Official source |",
     "|---|---|---|"]
for sid,s in sources.items():
    loc=(f"Printed {s['printed_page']}; PDF page {s['pdf_page']}; PDF index {s['pdf_index']}. " if s["pdf_page"] else "HTML release / index; no PDF page. ")+s["heading"]
    out.append(f"| {sid} | {loc} | [{s['document']}]({s['url']}) |")
out+=["","## Annual and quarterly metric tables",""]
titles={"income":"Consolidated results","margins":"Margins, provisions, and non-GAAP","segments":"Reportable segments and unallocated bridge","platforms":"Market platforms / end markets","cash":"Cash generation and capital return","balance":"Balance sheet, working capital and obligations","investments":"Equity investments and ecosystem exposure","tax":"Tax items and comparability","geography":"Geography","concentration":"Customer concentration","quarterly":"Quarterly FY2026 actuals","guidance":"Prior guidance, actual comparisons, and forward outlook","commitments":"Cloud service commitment schedule"}
for g in ["income","margins","segments","platforms","cash","balance","investments","tax","geography","concentration","quarterly","guidance","commitments"]:
    out += ["### "+titles[g],"",narratives[g],"","| Metric | Period | Segment / basis | Value | Unit | Status | Source | Notes / formula |","|---|---|---|---:|---|---|---|---|"]
    for r in groups[g]:
        note=r["notes"]
        if r["formula"]: note=(r["formula"]["expression"]+"; "+note).strip()
        cells=[r["metric"],r["period"],r["segment"],fmt(r["value"]),r["unit"],r["status"],cite(r["source"]),note]
        out.append("| "+" | ".join(str(v).replace("|","/").replace("\n"," ") for v in cells)+" |")
    out.append("")
out += ["## Stated drivers versus interpretation","",
        "| Topic | Company-stated explanation | Extraction / analytical boundary |",
        "|---|---|---|",
        "| Gross margin | Hopper HGX to Blackwell full-scale datacenter solutions; H20 charge; inventory/purchase-obligation provisions and releases [AR41]. | No complete quantified bridge. The H20 scale illustration is calculated; no residual assigned to Blackwell. |",
        "| Other income | Mainly unrealized gains in non-marketable/public equity, including Intel stock [AR42]. | Exact full realized/unrealized split not available. Portfolio gains are not operating income or operating cash generation. |",
        "| Cash flow | Higher CFO driven by higher revenue; increased investing use from equity purchases and Groq agreement [AR43]. | FCF excludes these investing outflows by company definition; do not equate it with post-investment cash remaining. |",
        "| Ecosystem investments | Private companies/funds include AI model makers buying through CSPs or directly; facility guarantees support buildout [AR37; AR69]. | Identify exposure and contractual links; no inference of fabricated demand. |",
        "| Supply | Datacenter-scale production and longer ordering horizons across current/future architectures [AR70]. | Missing FY2025 commitment data prevents a verified commitment growth percentage. Inventory growth can be calculated from disclosed balances. |",
        "",
        "## Caveats and handoff rules",""]
for c in caveats: out.append("- "+c)
out += ["","## Validation","",
        f"{len(checks)} key numeric reconciliations passed. Unique metric IDs, allowed source IDs, calculation inputs, page offsets, filing dates, and source-file SHA-256 checks passed. See evidence/stage1-validation.json for formulas, observed precision differences, and provenance.",
        "",
        "The quarterly non-GAAP operating-expense figures sum to 16,695 versus the annual 16,694; preserve the reported values rather than forcing equality [Q2_SUMMARY; Q3_SUMMARY; Q4_ANNUAL]. Rounded annual provision components also need not add exactly [AR41; AR67; AR68].",
        "",
        "## Machine-readable metric rows","",
        "Schema: id, metric, period, segment, value (number/null), unit, source (semicolon-separated IDs in source map), status (reported/calc/not disclosed), formula (expression plus input IDs for calculations; null otherwise), notes. Guidance status reported means the guidance was reported, not that it became an actual.",
        "",chr(96)*3+"json"]
out += ["["]+[json.dumps(r,ensure_ascii=False,separators=(",",":"))+("," if i<len(rows)-1 else "") for i,r in enumerate(rows)]+["]",chr(96)*3,""]
out += [f"[{sid}]: {s['url']} \"{s['heading']}"+(f"; printed {s['printed_page']}; PDF {s['pdf_page']}; index {s['pdf_index']}" if s["pdf_page"] else "")+"\"" for sid,s in sources.items()]
(BASE/"financials.md").write_text("\n".join(out)+"\n",encoding="utf-8")
validation=dict(stage=1,execution_date="2026-10-17",company="NVIDIA",fiscal_year=2026,period_end="2026-01-25",prior_period_end="2025-01-26",filing_date="2026-02-25",source_scope="Approved official annual-report PDF, mechanical extraction, supplied Q2/Q3/Q4 releases and SEC filing index only. No reference outputs or other demos read.",sources=source_manifest,source_map=sources,input_provenance=provenance,page_mapping=dict(full_pdf_pages=len(pages),ten_k_cover_pdf_page=89,ten_k_cover_pdf_index=88,cover_logical_printed_page=1,cover_number_visibly_printed=False,pdf_page_formula="printed_page + 88",pdf_index_formula="printed_page + 87",verified_numbered_pages=[51,53,55,77,78,79]),metric_count=len(rows),status_counts={st:sum(r["status"]==st for r in rows) for st in ("reported","calc","not disclosed")},checks=checks,all_numeric_checks_passed=all(c["passed"] for c in checks),precision_observations=rounding_notes,caveats=caveats,handoff_decisions=["Stage 2 starts only after parent review.","Use annual report for annual GAAP table values, releases for non-GAAP, FCF and quarters/guidance.","All Other is analytical calc, not a reported third segment.","Headquarters geography is recast and not billing or end-use.","Q4 FY2026 is historical, not latest as of execution.","Q1 FY2027 guidance uses changed non-GAAP definition; full-year tax guidance stays FY2027.","No unsupported private/customer identity attribution.","Missing comparative commitments/prepaid balances remain not disclosed.","Do not attribute margin residual wholly to Blackwell.","Parent performs independent rendered-page verification; this script did not inspect parent evidence or any downstream output."],artifacts=["financials.md","evidence/stage1-validation.json","scripts/stage1_extract.py"])
(BASE/"evidence"/"stage1-validation.json").write_text(json.dumps(validation,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"metric_rows":len(rows),"checks_passed":len(checks),"status_counts":validation["status_counts"],"output_bytes":(BASE/"financials.md").stat().st_size,"files":validation["artifacts"]}))

