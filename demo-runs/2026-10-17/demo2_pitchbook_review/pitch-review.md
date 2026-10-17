# GraspLoop AI pitch review

**FICTIONAL COMPANY AND DATA - TEACHING MATERIAL**

Review date: October 17, 2026 (America/Los_Angeles). Data room: September 2025 through September 2026, 13 monthly records. All amounts USD. Source: supplied 11-page pitch deck, KPI CSV and data-room README. No external verification or live company lookup was appropriate for this invented company.

## Verdict

**Conditional go for a focused founder diligence meeting; no-go for investment approval on this evidence.** The CSV supports $1.932M paying ARR, 6.57x paying YoY growth and improving fleet performance. Those are sufficient reasons to explore the product. The deck nevertheless presents unpaid pilots within ARR and customers, best-site performance without scope, and a 68% gross margin inconsistent with the September 41%. The stated 4-month CAC payback and 24-month funded runway cannot be established from the supplied aggregate data. Proceed only if founders can reconcile the commercial definitions, acquisition economics and cash-funded deployment plan. The panel does not infer intent or dishonesty.

## Scorecard

Scores use the bundled 1-5 Series A teaching rubric. These are the lead's reasoned dimension scores, not averages of reviewer opinions. No numerical disagreement is invented: the narrative reviewer retained its initial 2/2/3/2 scores after adding qualifications. The numbers reviewer scores traction 2 and unit economics 1.

| Dimension | Score / 5 | Basis |
|---|---:|---|
| Problem & insight | 2 | Specific warehouse pain; p2 percentages and cost-per-pick lack underlying study. |
| Product & technology | 3 | CSV shows an operating fleet and improving outcomes. SKU-learning, installation and causal model claims remain unverified (pp3,6). |
| Traction | 2 | Strong paying growth is real within the fictional CSV, but p6 combines paying/pilot and best-site/fleet metrics. |
| Unit economics | 1 | p7 margin conflicts with current CSV; acquisition-cohort CAC and hardware accounting are missing. |
| Market & competition | 2 | p5 is top-down sizing; p8 uses categories instead of named, evidenced alternatives. |
| Team | 3 | Named complementary roles, but institution, contribution and outcome details are vague on p9. |
| Plan & ask | 2 | p10 targets and p11 budget percentages are legible; monthly deployment, hiring and cash drivers are absent. |

## Claim checks and source convention

CSV references count the header as physical row 1; rows 2-14 cover September 2025-September 2026. The PDF's printed page numbers match its physical pages 1-11. `claims.json` is the machine-readable inventory of 42 quantitative, time-bound and planned claims. Page labels, diagram sequence labels and page 1's presentation date are metadata, not performance claims. A missing underlying source means **unverifiable**, not false. Projection arithmetic can be checked without validating the projection.

| ID / page | Deck claim | Finding and evidence | Status |
|---|---|---|---|
| P2-01 / p2 | Peak-season picker turnover >100% | No supporting market/customer study in supplied room Source: Deck p2 only. | unverifiable |
| P2-02 / p2 | Order growth 3x headcount growth since 2020 | No supporting market/customer study in supplied room Source: Deck p2 only. | unverifiable |
| P2-03 / p2 | Fully loaded cost per pick $0.42 | No supporting market/customer study in supplied room Source: Deck p2 only. | unverifiable |
| P2-04 / p2 | Cost per pick rising 9%/yr | No supporting market/customer study in supplied room Source: Deck p2 only. | unverifiable |
| P2-05 / p2 | Vendors serve top 1%; other 99% left with clipboards | No supporting market/customer study in supplied room Source: Deck p2 only. | unverifiable |
| P3-01 / p3 | Off-the-shelf 6-axis arm | Product/system evidence absent Source: Deck p3 only. | unverifiable |
| P3-02 / p3 | Installs in one day | Product/system evidence absent Source: Deck p3 only. | unverifiable |
| P3-03 / p3 | New SKU learned in 10 minutes | Product/system evidence absent Source: Deck p3 only. | unverifiable |
| P3-04 / p3 | New SKU learned from 20 picks | Product/system evidence absent Source: Deck p3 only. | unverifiable |
| P3-05 / p3 | Remote operators resolve picks in seconds | Product/system evidence absent Source: Deck p3 only. | unverifiable |
| P4-01 / p4 | Foundation models made generalist grasping practical in 2025-26 | No dated evaluation or purchase quote supplied Source: Deck p4 only. | unverifiable |
| P4-02 / p4 | Collaborative arms below $25,000 | No dated evaluation or purchase quote supplied Source: Deck p4 only. | unverifiable |
| P5-01 / p5 | $120B TAM in 2030 | Market sizing and share assumptions absent Source: Deck p5 only. | unverifiable |
| P5-02 / p5 | $9B SAM US/EU mid-size piece-picking | Market sizing and share assumptions absent Source: Deck p5 only. | unverifiable |
| P5-03 / p5 | $450M SOM reachable by 2030 | Market sizing and share assumptions absent Source: Deck p5 only. | unverifiable |
| P6-01 / p6 | $2.4M ARR | Paying ARR $1,932,000; pilot-inclusive metric $2,436,000 Source: CSV row 14 (2026-09), README. Formula: `161000 * 12; (46 + 12) * 3500 * 12`. | contradicted as paying arr |
| P6-02 / p6 | 8x YoY ARR growth | Paying 6.5714x (+557.14%); pilot-inclusive 8.2857x Source: CSV rows 2 and 14 (2025-09,2026-09). Formula: `161000 / 24500; 2436000 / 294000`. | needs qualification |
| P6-03 / p6 | 14 customers | 11 paying + 3 unpaid pilots = 14 total Source: CSV row 14 (2026-09). Formula: `11 + 3`. | needs qualification |
| P6-04 / p6 | Includes 3 Fortune 500 retailers | Customer identities unavailable Source: Deck p6 only. | unverifiable |
| P6-05 / p6 | 99.7% pick success | 99.7% best site single SKU; 97.2% fleet mixed SKU Source: CSV row 14 (2026-09), README. Formula: `Read distinct success columns`. | needs qualification |
| P6-06 / p6 | 160% NRR | 157.14% for starting n=3 only; 160% is rough rounding Source: CSV rows 2 and 14; README cohort definition. Formula: `38500 / 24500 * 100`. | needs qualification |
| P7-01 / p7 | $3,500 per robot per month | Matches all 13 paying MRR rows Source: CSV rows 2-14; README. Formula: `mrr_usd / robots_live_paying = 3500`. | supported |
| P7-02 / p7 | 3-year term | No executed contracts supplied Source: Deck p7 only. | unverifiable |
| P7-03 / p7 | 68% gross margin | September 41%; no month reaches 68%; trailing-12 revenue-weighted 33.78% Source: CSV rows 2-14 (2025-09 to 2026-09). Formula: `Read monthly gross_margin_pct; sum(MRR * GM) / sum(MRR)`. | contradicted as current |
| P7-04 / p7 | 4-month CAC payback | Net-new-MRR proxies: Sept 29.62; Q3 26.27; TTM 27.87 months Source: CSV rows 2-14; interval details in calculations.json. Formula: `matching-window S&M / (net new MRR * ending GM)`. | unverifiable and inconsistent with available proxy |
| P7-05 / p7 | 9-month pilot-to-contract sales cycle | Monthly stocks cannot identify elapsed cohort conversion time Source: Deck p7 and CSV customer stocks. | unverifiable |
| P7-06 / p7 | $42,000 hardware cost per robot | No bill of materials or invoices supplied Source: Deck p7 only. | unverifiable |
| P9-01 / p9 | CEO has 2 prior exits | Fictional biographies have no supporting records Source: Deck p9 only. | unverifiable |
| P9-02 / p9 | VP Customer Ops ran 14 fulfillment centers | Fictional biographies have no supporting records Source: Deck p9 only. | unverifiable |
| P10-2026 / p10 | $2.4M ARR in 2026 | Requires 58 paying robots at current price; 2026 point is ambiguous actual vs year-end target Source: Deck p10; CSV row 14 current baseline. Formula: `ceil(target ARR / (3500 * 12))`. | projection unvalidated |
| P10-2027 / p10 | $9M ARR in 2027 | Requires 215 paying robots at current price; 2026 point is ambiguous actual vs year-end target Source: Deck p10; CSV row 14 current baseline. Formula: `ceil(target ARR / (3500 * 12))`. | projection unvalidated |
| P10-2028 / p10 | $30M ARR in 2028 | Requires 715 paying robots at current price; 2026 point is ambiguous actual vs year-end target Source: Deck p10; CSV row 14 current baseline. Formula: `ceil(target ARR / (3500 * 12))`. | projection unvalidated |
| P10-2029 / p10 | $100M ARR in 2029 | Requires 2381 paying robots at current price; 2026 point is ambiguous actual vs year-end target Source: Deck p10; CSV row 14 current baseline. Formula: `ceil(target ARR / (3500 * 12))`. | projection unvalidated |
| P11-01 / p11 | $18M raise | $18M is an ask, not cash received Source: Deck p11 only. | stated plan unvalidated |
| P11-02 / p11 | $90M pre-money | $108M simple post-money; 16.67% simple new-money ownership Source: Deck p11 only. Formula: `90M + 18M; 18M / 108M`. | stated plan unvalidated |
| P11-03 / p11 | 50% R&D | $9M allocation Source: Deck p11 only. Formula: `18M * .50`. | stated plan unvalidated |
| P11-04 / p11 | 30% go-to-market | $5.4M allocation Source: Deck p11 only. Formula: `18M * .30`. | stated plan unvalidated |
| P11-05 / p11 | 20% operations | $3.6M allocation Source: Deck p11 only. Formula: `18M * .20`. | stated plan unvalidated |
| P11-06 / p11 | 12 AEs, 3 regions | Deployment/hiring plan unvalidated Source: Deck p11 only. | stated plan unvalidated |
| P11-07 / p11 | LoopBrain v2 | Product version milestone; no roadmap supplied Source: Deck p11 only. | stated plan unvalidated |
| P11-08 / p11 | Headcount 38 to 85 | 38 matches September; 85 is a hiring target (+123.68%) Source: CSV row 14 (2026-09); deck p11. Formula: `85 / 38 - 1`. | baseline supported plan unvalidated |
| P11-09 / p11 | 24 months runway | Current cash / September burn = 8.46 months; immediate $18M raise, flat burn = 33.67 months; 24 months needs average burn <= $1,001,592 Source: CSV row 14; deck p11. Formula: `cash / forward burn; scenarios in calculations.json`. | unverifiable |

## Key calculations and methodological limits

**Paying versus pilot-inclusive ARR (p6).** September MRR is $161,000, so paying ARR is $161,000 x 12 = **$1,932,000**. The column called `booked_arr_incl_pilots_usd` is (46 paying robots + 12 unpaid pilot robots) x $3,500 x 12 = **$2,436,000**. Its $504,000 gap is annualized unpaid pilot capacity, not evidenced contracted revenue. Calling the column "booked" does not supply signed contracts. The pilot-inclusive metric is 26.09% above paying ARR. Actual contracted ARR is unverifiable without contract dates, terms and billing start dates. The 14 customer total comprises 11 paying and 3 unpaid pilots (row 14, September 2026).

**Growth (p6).** $161,000 / $24,500 = **6.5714x**, or **+557.14%**, paying YoY (rows 2 and 14). The pilot-inclusive series gives $2,436,000 / $294,000 = 8.2857x, explaining the approximately 8x headline but changing its basis. Recent MRR growth slows from +15.15% in July to +10.53% in August and +9.52% in September (rows 11-14). This is slower positive growth, not stalled growth. Q3 endpoint growth is 39.39% and 12-month compound monthly growth is 16.99%.

**Margin and operating scope (pp6-7).** September GM is **41%**, gross profit $66,010 and implied COGS $94,990. None of the 13 monthly margins reaches 68%; it is not labelled a target on p7. Twelve-month revenue-weighted GM is 33.78%. September 99.7% success is the best single site on single-SKU lanes; fleet mixed-SKU success is 97.2%. The fleet series improves from 94.1% to 97.2% and interventions fall from 41 to 14 per 1,000 picks (rows 2 and 14), but this does not isolate the model's causal effect from site/SKU changes or human support. COGS composition and human-operator cost are unavailable.

**CAC payback (p7): why approximately 26 can be demonstrated.** The deck actually says **4 months**. The demo prompt's approximately 26-month correction is reproducible for **Q3 2026** using ending gross margin:

`($155,000 + $165,000 + $170,000) / (($161,000 - $115,500) x 41%) = 26.2664 months`

The numerator is July-September spending (rows 12-14); the denominator uses September less June MRR (rows 14 and 11). This is a **net-new-MRR proxy**. A trailing-year interval uses October 2025-September 2026 spending of $1.56M (rows 3-14), net MRR additions of $136,500 (rows 14 minus 2) and the same 41% margin, producing **27.8746 months**. September alone yields **29.6167 months**. None corroborates 4 months, but none proves an acquisition-cohort CAC payback either: new-logo MRR, expansion, contraction, churn, attributable acquisition spend and sales-lag alignment are absent.

Margin conventions also matter. Multiplying each Q3 monthly MRR increment by its own monthly margin gives $17,990 of incremental gross-profit proxy and **27.24 months**. Applying Q3 revenue-weighted margin to total net new MRR gives **27.08 months** (independently calculated by the numbers reviewer). These methods answer slightly different approximation questions. Do not call all of them "the actual CAC." See `calculation-results.md`, `calculations.json` and the numbers review for inputs and alternatives.

**NRR (p6).** $38,500 / $24,500 = **157.14%** for the three customers paying in September 2025 (rows 2 and 14; README). A coarse 160% headline needs both its rounding and n=3 disclosure. Aggregate cohort MRR does not establish zero logo churn or representative retention across later cohorts. Customer-level bridges and concentration are missing.

**Runway and forward burn (pp10-11).** September end cash is **$6,038,215** and monthly burn is **$713,990**, giving **8.46 months** only if this burn remains constant and no raise occurs. If the full $18M closes immediately, no fees are paid and burn stays flat, the same arithmetic gives **33.67 months**. These are illustrative cases, not a test that disproves p11's 24-month plan. To achieve 24 months with all $24,038,215 available immediately, average net cash use must not exceed **$1,001,592 per month**, including hardware, working capital and fees.

The CSV burn exactly equals opex minus reported gross profit in all 13 rows. No separate hardware/capex series is identifiable; this does not prove capex is zero or excluded from every reported cost. A stress case that scales all September opex by 85/38 while holding September gross profit constant yields burn of **$1,678,727/month** and **14.32 months** after the hypothetical raise. A linear 24-month headcount ramp under the same opex scaling assumption exhausts cash around **month 20.85**, before separate capex. Scaling all opex with headcount is an analyst assumption, not a payroll forecast. See `forward-burn-sensitivity.csv` for the full 24-month schedule.

At $3,500 per month, $9M ARR requires at least **215 paying robots**, and $100M requires **2,381**. If every increment above today's 46 paying robots requires a new unit at the deck's unverified $42,000 cost, reaching $9M implies $7.098M of hardware purchases. This scenario assumes no conversion/reuse of the 12 existing pilot robots, no spare inventory, no leasing or vendor financing. It is not an asserted funding shortfall. The same $42,000 price divided by monthly revenue gives 12 months of hardware revenue recovery, or 29.27 months at 41% gross margin, neither of which is customer acquisition payback; accounting double counting must be resolved first.

## Narrative findings

The deck follows the expected sequence: identity (p1), problem (p2), product (p3), why now (p4), market (p5), traction (p6), business model (p7), competition (p8), team (p9), growth plan (p10) and ask (p11). The core problem is evidence and definitions, not slide order. Use a concrete customer workflow on p2, qualify the arm/model/teleoperation loop on p3, and move verified paying traction into the opening hook. Pair best-site performance with fleet context on p6. Replace the unsupported economics on p7, name evidence-backed alternatives on p8, specify each fictional executive's actual contribution on p9, and connect robot deployments to revenue and cash on pp10-11. Full page-by-page notes and score revisions are in `review-narrative.md`.

## Devil's advocate: five reasons to pass now

1. **Metric presentation prevents a reliable read (p6).** Paid/pilot and fleet/best-site definitions materially change the impression. This raises a diligence burden, not a finding of dishonesty.
2. **The current economics do not support the stated efficiency story (p7).** September margin is weaker and available payback proxies are longer. Acquisition-cohort economics and cost composition remain unverified.
3. **The ask has no funded deployment bridge (pp10-11).** Hiring, robot purchases, conversions, receipts and financing need a monthly cash model. Current cash/current burn alone cannot invalidate post-raise runway.
4. **The learning advantage is unproven (pp3,6,8).** Off-the-shelf arms do not prove the model is rented; improved fleet outcomes do not prove a proprietary causal moat. Request controlled results and training-data/IP rights.
5. **Attainable demand and competition are unsubstantiated (pp5,8).** Top-down TAM and a category-only chart do not establish reachable customers, differentiated performance or sales conversion. Unsupported market size is not proven false.

The devil reviewer would change its mind for a reconciled, customer-level commercial and cash model corroborated by contracts and deployment evidence. See `review-devils-advocate.md`.

## Conflicts and challenges

The panel ran as three independent subagents, then exchanged direct messages. The following is a factual paraphrase of those exchanges; exact sent/received text is preserved in the reviewer files. Agreement is recorded as agreement, not manufactured conflict.

| From -> to | Challenge | Resolution / remaining tension |
|---|---|---|
| Narrative -> Numbers | Can p6's $2.4M, 8x, 14 customers, 99.7% and 160% lead the story? | Numbers supplied paying/pilot, fleet/site and n=3 distinctions. Narrative rewrote the proposed hook and retained its rubric scores. |
| Numbers -> Narrative | The corrected story still has 6.57x paying growth; do not imply stalled growth. | Narrative preserves strong growth and distinguish deceleration from stagnation. |
| Devil -> Narrative | Improved fleet outcomes do not demonstrate a causal learning flywheel. | Narrative accepted the causal limit and requests controlled results and data rights. No assertion of a rented moat. |
| Numbers -> Devil | 24 months on p11 belongs to the raise and hiring plan; 8.46 pre-raise months alone cannot disprove it. | Devil narrowed its claim to an unverified forward cash plan. Flat post-raise and hiring sensitivities are explicitly assumptions. |
| Narrative -> Devil | Separate business-risk pass reasons from proof of misconduct, and preserve a possible conditional meeting. | Devil supports a conditional diligence meeting while arguing no investment approval yet. No founder-intent allegation. |
| Narrative and Devil -> Numbers | Verify CAC and distinguish the proposed approximately 26-month correction from p7's actual 4-month claim. | Q3 ending-GM proxy 26.27; TTM 27.87; September 29.62. Exact CAC remains unverifiable. |
| Lead -> Numbers | Different margin weighting methods generate different proxy answers. | Monthly-increment GM and revenue-weighted period GM remain distinctly labelled; no forced numerical consensus. |

Remaining difference is emphasis: narrative sees a repairable, coherent product story, while the devil requires reconciled evidence before investment advocacy. The lead adopts conditional diligence, not an average of enthusiasm and skepticism. Detailed handoff record: `conflicts-log.md`.

## Top five fixes, ranked by investor impact

1. **Repair the metric definitions on p6.** Show $1.932M paying ARR, $504k annualized unpaid pilot capacity separately, 11 paying plus 3 pilots, 6.57x paying YoY, best-site/fleet success, and the three-customer NRR cohort.
2. **Rebuild p7 around auditable economics.** Show actual 41% September GM and COGS composition; show acquisition-cohort CAC with sales-lag and gross-new-MRR inputs. Label 68% as a target only if a supported target model exists.
3. **Replace pp10-11 with a monthly deployment and funding bridge.** Tie paying robots, pilots, hires, pricing, retention, hardware ownership, capex, working capital and financing to cash. Explain the 24-month runway under actual closing assumptions.
4. **Evidence the product advantage and comparison (pp3,6,8).** Show controlled mixed-SKU performance, operator cost, deployment time, data rights and named competitor alternatives.
5. **Make the addressable market and team evidence concrete (pp2,5,8,9).** Build SAM from eligible sites and realistic contract values; disclose comparable alternatives and attributable executive experience.

## Four questions for the founders

1. Which robots and customers are currently paying, which have signed but not commenced contracts, and which are unpaid pilots? Provide the customer-level revenue and cohort bridge, including identities and churn.
2. What is included in gross margin, what assumptions produce 68%, and what acquisition cohort and spend/new-MRR timing supports the stated 4-month payback?
3. What controlled results demonstrate SKU learning, installation time and fleet performance, how much teleoperation is required, and who owns the models and training data?
4. After the raise's actual closing date, how do monthly deployments, the 38-to-85 hiring plan, hardware purchases/financing and collections produce 24 months of cash runway?

## Execution and verification

Lead and numbers reviewer independently calculated the key metrics from the original CSV. `calculate.py` writes 53 source-identity/cash-roll-forward checks, all passing, plus claim and sensitivity artifacts. Passing reconciliation checks prove internal arithmetic consistency, not authenticity. Every source PDF page was extracted and rendered. The supplied reference output was preserved and was not used as the basis of this review. Source hashes are recorded in `evidence/source-manifest.json`.

The source period is September 2025-September 2026 even though this review runs October 17, 2026. No current external company data, contract authenticity, native PowerPoint execution or live financial-system test is claimed. `founder-email.md` is an unsent local draft. No communications, schedules or external publishing occurred.
