$ErrorActionPreference='Stop'
$run=Split-Path -Parent $MyInvocation.MyCommand.Path
$file=Join-Path $run 'GOOGL_DCF_Valuation.xlsx'
$report=[ordered]@{engine='Microsoft Excel COM'; completed_at='2026-10-17'; timezone='America/Los_Angeles'; checks=@(); scenarios=@(); limitations=@('Native Excel calculation tested programmatically; no interactive UI walkthrough was performed.')}
$excel=$null
$book=$null
function Add-Check($name,$passed,$evidence) { $report.checks += [ordered]@{name=$name;status=$(if($passed){'pass'}else{'fail'});evidence=$evidence} }
function Calc { $excel.CalculateFullRebuild(); if($excel.CalculationState -ne 0){throw 'Excel calculation did not complete'} }
try {
 $excel=New-Object -ComObject Excel.Application
 $excel.Visible=$false
 $excel.DisplayAlerts=$false
 $excel.AskToUpdateLinks=$false
 $excel.AutomationSecurity=3
 $report.excel_version=$excel.Version
 $book=$excel.Workbooks.Open($file,0,$false)
 $excel.Calculation=-4105
 $a=$book.Worksheets.Item('Assumptions');$s=$book.Worksheets.Item('Summary');$h=$book.Worksheets.Item('Historicals');$p=$book.Worksheets.Item('Projections');$d=$book.Worksheets.Item('DCF');$sen=$book.Worksheets.Item('Sensitivity');$m=$book.Worksheets.Item('Multiples')
 Calc
 $base=[double]$s.Range('E9').Value2
 $historicalRevenue=[double]$h.Range('F15').Value2
 $original=[double]$a.Range('E84').Value2
 $a.Range('E84').Value2=0.36
 Calc
 $changed=[double]$s.Range('E9').Value2
 $expected=[double]$p.Range('E15').Value2*($original-0.36)/([math]::Pow(1+[double]$d.Range('D15').Value2,[double]$d.Range('E21').Value2))/[double]$d.Range('D50').Value2
 Add-Check '2027 capex 46% to 36% flows to Summary' (($changed -gt $base) -and ([math]::Abs(($changed-$base)-$expected) -lt 0.000001)) @{cell='Assumptions!E84';before=$base;after=$changed;delta=$changed-$base;expected_delta=$expected;output='Summary!E9'}
 $a.Range('E84').Value2=$original;Calc
 Add-Check 'Base restored after capex test' ([math]::Abs([double]$s.Range('E9').Value2-$base) -lt 0.000001) @{capex=$a.Range('E84').Value2;value=$s.Range('E9').Value2}
 foreach($case in 1,2,3){$a.Range('D4').Value2=[double]$case;Calc;$report.scenarios += [ordered]@{selector=$case;name=$a.Range('F4').Value2;dcf=$s.Range('E9').Value2;revenue2030=$p.Range('H15').Value2;capex2027=$p.Range('E33').Value2};Add-Check "Historical actuals unchanged in case $case" ([double]$h.Range('F15').Value2 -eq $historicalRevenue) @{reported_FY2025_revenue=$h.Range('F15').Value2}}
 $a.Range('D4').Value2=1.0;Calc
 Add-Check 'Bull / base / bear change valuation in expected order' (($report.scenarios[1].dcf -gt $report.scenarios[0].dcf) -and ($report.scenarios[0].dcf -gt $report.scenarios[2].dcf)) $report.scenarios
 $later=[double]$a.Range('H49').Value2;$a.Range('H49').Value2=$later+0.05;Calc
 Add-Check '2030 Cloud input flows through forecast and DCF' ([double]$s.Range('E9').Value2 -ne $base) @{before=$base;after=$s.Range('E9').Value2;cell='Assumptions!H49'}
 $a.Range('H49').Value2=$later;Calc
 $bullCapex=$a.Range('E85').Value2;$a.Range('E85').ClearContents();Calc
 Add-Check 'Blank unselected driver does not block Base' ([math]::Abs([double]$s.Range('E9').Value2-$base) -lt 0.000001) @{blank_cell='Assumptions!E85';selected='Base'}
 $a.Range('D4').Value2=2.0;Calc
 Add-Check 'Selecting missing case exposes missing input' ($a.Range('E83').Value2 -eq 'Missing input') @{active=$a.Range('E83').Text;summary=$s.Range('E9').Text}
 $a.Range('E85').Value2=$bullCapex;$a.Range('D4').Value2=1.0;Calc
 $a.Range('E84').Value2=0.0;Calc
 Add-Check 'Zero capex is a valid driver, not missing' (([double]$a.Range('E83').Value2 -eq 0) -and ([double]$s.Range('E9').Value2 -gt $base)) @{active_capex=$a.Range('E83').Value2;value=$s.Range('E9').Value2}
 $a.Range('E84').Value2=$original;Calc
 $tie=@();foreach($c in 'D','E','F','G','H'){foreach($r in 16,24){$tie+=@{cell="Historicals!$c$r";difference=$h.Range("$c$r").Value2}}}
 Add-Check 'Historical revenue and EBIT tie-outs' (($tie|Where-Object{[math]::Abs([double]$_.difference)-gt 0.000001}).Count -eq 0) $tie
 Add-Check 'Sensitivity center equals DCF' ([math]::Abs([double]$sen.Range('D19').Value2) -lt 0.000001) @{difference=$sen.Range('D19').Value2}
 $alloc=@();foreach($c in 'D','E','F','G','H'){$alloc+=@{cell="Projections!${c}90";difference=$p.Range("${c}90").Value2}}
 Add-Check 'Segment cash-flow allocations reconcile' (($alloc|Where-Object{[math]::Abs([double]$_.difference)-gt 0.000001}).Count -eq 0) $alloc
 Add-Check '2026 capex equals guidance midpoint' ([double]$p.Range('D33').Value2 -eq 200000) @{actual=$p.Range('D33').Value2;source='Company Q2 2026 call: $195–205bn'}
 Add-Check 'Stub excludes elapsed 2026 period' (($d.Range('D19').Text -eq '2026-10-17') -and ([double]$d.Range('D20').Value2 -lt 0.22)) @{start=$d.Range('D19').Text;years=$d.Range('D20').Value2;full_year_fcf=$d.Range('D22').Value2;valued_fcf=$d.Range('D23').Value2}
 Add-Check 'WACC capital weights sum to one' ([math]::Abs([double]$d.Range('D12').Value2+[double]$d.Range('D13').Value2+[double]$d.Range('D14').Value2-1)-lt 0.000001) @{equity=$d.Range('D12').Value2;debt=$d.Range('D13').Value2;preferred=$d.Range('D14').Value2}
 $forward=@();foreach($c in 'D','E','F','G'){$forward+=@{ticker=$m.Range("${c}6").Value2;eps=$m.Range("${c}77").Value2;pe=$m.Range("${c}48").Value2;date=$m.Range("${c}78").Text;difference=[double]$m.Range("${c}48").Value2-[double]$m.Range("${c}8").Value2/[double]$m.Range("${c}77").Value2}}
 Add-Check 'Forward P/E uses dated CY2027 EPS for all four companies' (($forward|Where-Object{[math]::Abs($_.difference)-gt 0.000001 -or $_.eps -le 0 -or $_.date -ne '2026-10-16'}).Count -eq 0) $forward
 Add-Check 'Microsoft fiscal estimates calendarize to CY2027' ([math]::Abs([double]$m.Range('E77').Value2-21.75)-lt 0.000001) @{fy2027=$m.Range('E73').Value2;fy2028=$m.Range('E75').Value2;calendar2027=$m.Range('E77').Value2}
 $msftLater=[double]$m.Range('E75').Value2;$msftEPS=[double]$m.Range('E77').Value2;$m.Range('E75').Value2=$msftLater+1.0;Calc
 Add-Check 'Forward EPS change propagates through calendarization and multiple' (([math]::Abs([double]$m.Range('E77').Value2-$msftEPS-0.5)-lt 0.000001) -and ([math]::Abs([double]$m.Range('E48').Value2-[double]$m.Range('E8').Value2/($msftEPS+0.5))-lt 0.000001)) @{eps_before=$msftEPS;eps_after=$m.Range('E77').Value2;pe_after=$m.Range('E48').Value2}
 $m.Range('E75').Value2=$msftLater;Calc
 Add-Check 'Forward peer median excludes Alphabet and flows to Summary' ([math]::Abs([double]$s.Range('E13').Value2-[double]$m.Range('E57').Value2*[double]$m.Range('D77').Value2)-lt 0.000001) @{peer_median=$m.Range('E57').Value2;implied_value=$s.Range('E13').Value2;median_formula=$m.Range('E57').Formula}
 Add-Check 'Peer edits do not change the DCF' ([math]::Abs([double]$s.Range('E9').Value2-$base)-lt 0.000001) @{dcf=$s.Range('E9').Value2}
 $report.forward_comparables=$forward
 $bridge=@();$ppeExpected=@(25237,34300,21550,49741);$i=0
 foreach($c in 'D','E','F','G'){$bridge+=@{ticker=$m.Range("${c}6").Value2;ebit=$m.Range("${c}85").Value2;ppe=$m.Range("${c}86").Value2;ebitd=$m.Range("${c}87").Value2;multiple=$m.Range("${c}88").Value2;ppe_difference=[double]$m.Range("${c}86").Value2-$ppeExpected[$i];bridge_difference=$m.Range("${c}89").Value2};$i++}
 Add-Check 'All four EBITD denominators use EBIT plus reported PPE depreciation' (($bridge|Where-Object{[math]::Abs($_.ppe_difference)-gt 0.000001 -or [math]::Abs($_.bridge_difference)-gt 0.000001}).Count -eq 0) $bridge
 Add-Check 'EBITD peer median excludes Alphabet and flows to Summary' ([math]::Abs([double]$s.Range('E12').Value2-([double]$m.Range('E56').Value2*[double]$m.Range('D87').Value2+[double]$d.Range('D48').Value2)/[double]$m.Range('D9').Value2)-lt 0.000001) @{median=$m.Range('E56').Value2;value=$s.Range('E12').Value2;formula=$m.Range('E56').Formula}
 $originalPPE=[double]$m.Range('G37').Value2;$originalEbitd=[double]$m.Range('G87').Value2;$originalPeerValue=[double]$s.Range('E12').Value2;$m.Range('G37').Value2=$originalPPE+1000.0;Calc
 $editedPeerValue=[double]$s.Range('E12').Value2
 Add-Check 'PPE source edit flows through TTM EBITD and peer valuation' (([math]::Abs([double]$m.Range('G87').Value2-$originalEbitd-1000)-lt 0.000001) -and ($editedPeerValue-lt $originalPeerValue) -and ([math]::Abs([double]$s.Range('E9').Value2-$base)-lt 0.000001)) @{edited='Multiples!G37';peer_before=$originalPeerValue;peer_after=$editedPeerValue;dcf=$s.Range('E9').Value2}
 $m.Range('G37').Value2=$originalPPE;Calc
 Add-Check 'Peer source restored after propagation test' ([math]::Abs([double]$s.Range('E12').Value2-$originalPeerValue)-lt 0.000001) @{source_restored=$m.Range('G37').Value2;peer_value=$s.Range('E12').Value2}
 Add-Check 'Lecture comparison is labeled EBITD, not EBITDA' (($s.Range('C12').Value2 -eq 'EV / EBITD') -and ($m.Range('C50').Value2 -eq 'EV / EBITD')) @{summary_label=$s.Range('C12').Value2;multiple_label=$m.Range('C50').Value2}
 $report.ebitd_bridge=$bridge
 $quote=[double]$a.Range('D7').Value2;$a.Range('D7').Value2=$quote+10.0;Calc
 Add-Check 'One Alphabet quote drives DCF, peer multiples and Summary' (([double]$m.Range('D8').Value2-eq [double]$a.Range('D7').Value2) -and ([double]$s.Range('G6').Value2-eq [double]$a.Range('D7').Value2) -and ([math]::Abs([double]$m.Range('D10').Value2-[double]$d.Range('D6').Value2)-lt 0.000001) -and ([math]::Abs([double]$m.Range('D48').Value2-($quote+10.0)/[double]$m.Range('D77').Value2)-lt 0.000001)) @{quote=$a.Range('D7').Value2;peer_price=$m.Range('D8').Value2;dcf_equity=$d.Range('D6').Value2;peer_equity=$m.Range('D10').Value2;forward_pe=$m.Range('D48').Value2}
 $a.Range('D7').Value2=$quote;Calc
 Add-Check 'Meta market value uses period-end Class A plus Class B shares' (([double]$m.Range('F9').Value2-eq 2548) -and ([math]::Abs([double]$m.Range('F10').Value2-2548*[double]$m.Range('F8').Value2)-lt 0.000001)) @{class_a=$m.Range('F68').Value2;class_b=$m.Range('F69').Value2;total=$m.Range('F9').Value2;formula=$m.Range('F9').Formula}
 $baseGrowth=[double]$a.Range('D14').Value2;$baseRF=[double]$a.Range('D9').Value2;$equityWeight=[double]$d.Range('D12').Value2;$gridTests=@()
 foreach($test in @(@('E12',-0.005,-0.005),@('G14',0.005,0.005))){$gridExpected=[double]$sen.Range($test[0]).Value2;$a.Range('D9').Value2=$baseRF+[double]$test[1]/$equityWeight;$a.Range('D14').Value2=$baseGrowth+[double]$test[2];Calc;$gridTests+=@{grid_cell=$test[0];grid_value=$gridExpected;native_dcf=$s.Range('E9').Value2;difference=[double]$s.Range('E9').Value2-$gridExpected};$a.Range('D9').Value2=$baseRF;$a.Range('D14').Value2=$baseGrowth;Calc}
 Add-Check 'Noncentral WACC-growth grid cells match native model edits' (($gridTests|Where-Object{[math]::Abs($_.difference)-gt 0.000001}).Count-eq 0) $gridTests
 foreach($excess in 0.0,0.005){$a.Range('D14').Value2=[double]$d.Range('D15').Value2+$excess;Calc;Add-Check "Gordon model rejects growth at WACC plus $excess" (($d.Range('D35').Text-eq '#N/A') -and ($s.Range('E9').Text-eq '#N/A') -and ($sen.Range('F13').Text-eq '#N/A') -and ($s.Range('D24').Value2-eq 'Growth must be below WACC')) @{growth=$a.Range('D14').Value2;wacc=$d.Range('D15').Value2;summary=$s.Range('E9').Text;message=$s.Range('D24').Value2}}
 $a.Range('D14').Value2=$baseGrowth;Calc
 $terminalRatio=[double]$a.Range('D15').Value2;$a.Range('D15').Value2=1.5;Calc
 $terminalStress=[double]$s.Range('E9').Value2
 $terminalExpected=-[double]$d.Range('D31').Value2*(1.5-$terminalRatio)/([double]$d.Range('D15').Value2-$baseGrowth)/[math]::Pow(1+[double]$d.Range('D15').Value2,[double]$d.Range('D36').Value2)/[double]$d.Range('D50').Value2
 Add-Check 'Terminal capex stress matches independent valuation impact' (([math]::Abs(($terminalStress-$base)-$terminalExpected)-lt 0.000001) -and ($terminalStress-lt $base)) @{base_ratio=$terminalRatio;stress_ratio=1.5;before=$base;after=$terminalStress;delta=$terminalStress-$base;expected_delta=$terminalExpected}
 $a.Range('D15').Value2=$terminalRatio;Calc
 Add-Check 'All review edits restored to the dated lecture state' (([math]::Abs([double]$s.Range('E9').Value2-$base)-lt 0.000001) -and ([double]$a.Range('D7').Value2-eq $quote) -and ([double]$a.Range('D14').Value2-eq $baseGrowth) -and ([double]$a.Range('D15').Value2-eq $terminalRatio)) @{dcf=$s.Range('E9').Value2;quote=$a.Range('D7').Value2;growth=$a.Range('D14').Value2;terminal_capex_ratio=$a.Range('D15').Value2}
 $errors=@();$formulas=0
 foreach($sheet in $book.Worksheets){try{$cells=$sheet.UsedRange.SpecialCells(-4123);foreach($cell in $cells){$formulas++;if($cell.Text -match '^#(REF!|DIV/0!|VALUE!|NAME\?|N/A|NUM!|NULL!|SPILL!|CALC!)$'){$errors+=@{sheet=$sheet.Name;cell=$cell.Address();error=$cell.Text}}}}catch{if($_.Exception.Message -notmatch 'No cells were found'){throw}}}
 Add-Check 'Zero final Excel formula errors' ($errors.Count -eq 0) @{errors=$errors;formula_cells=$formulas}
 Add-Check 'Scenario selector and native bar chart exported' (($a.Range('D4').Validation.Type -eq 3) -and ($s.ChartObjects().Count -eq 1)) @{validation_type=$a.Range('D4').Validation.Type;charts=$s.ChartObjects().Count}
 $report.summary=[ordered]@{base_dcf=$s.Range('E9').Value2;low_dcf=$s.Range('D9').Value2;high_dcf=$s.Range('F9').Value2;market=$s.Range('G6').Value2;wacc=$d.Range('D15').Value2;terminal_growth=$a.Range('D14').Value2;terminal_share=$d.Range('D40').Value2;revenue2030=$p.Range('H15').Value2;capex2027=$p.Range('E33').Value2;cloud_share2030=[double]$p.Range('H12').Value2/[double]$p.Range('H15').Value2;required_terminal_fcf_ratio=$sen.Range('D23').Value2;peer_pe=$s.Range('E10').Value2;peer_sales=$s.Range('E11').Value2;peer_ebitd_verified=$s.Range('E12').Value2;fcf=@($p.Range('D40').Value2,$p.Range('E40').Value2,$p.Range('F40').Value2,$p.Range('G40').Value2,$p.Range('H40').Value2)}
 $report.summary.peer_forward_pe=$s.Range('E13').Value2
 $report.summary.terminal_capex_stress=$terminalStress
 $report.summary.terminal_capex_stress_ratio=1.5
 $s.Activate();$s.Range('C2').Select()
 $book.Save()
 $book.Close($false);$book=$null
 $book=$excel.Workbooks.Open($file,0,$true)
 Add-Check 'Saved workbook reopens with restored Base' (([double]$book.Worksheets.Item('Assumptions').Range('D4').Value2 -eq 1) -and ([math]::Abs([double]$book.Worksheets.Item('Summary').Range('E9').Value2-$base)-lt 0.000001)) @{saved_value=$book.Worksheets.Item('Summary').Range('E9').Value2}
 Add-Check 'Workbook opens on the lecture Summary' ($book.ActiveSheet.Name-eq 'Summary') @{active_sheet=$book.ActiveSheet.Name}
 $report.status=$(if(($report.checks|Where-Object status -eq 'fail').Count -eq 0){'pass'}else{'fail'})
} catch { $report.status='failed';$report.error=$_.Exception.Message;throw }
finally {if($book){$book.Close($false)};if($excel){$excel.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)};$report|ConvertTo-Json -Depth 15|Set-Content -LiteralPath (Join-Path $run 'validation-report.json') -Encoding utf8}
$report.summary|ConvertTo-Json
if($report.status -ne 'pass'){exit 1}
