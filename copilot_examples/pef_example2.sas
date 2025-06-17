/******************************************************************************\
* $Id$
*
* Copyright(c) 2019 SAS Institute Inc., Cary, NC, USA. All Rights Reserved.
*
* Name: cf_hicams_scoring_2.sas
*
* Purpose: Scoring projects from cashflow to predict Contract Cost and Calendar Days
*
* Author: kebaug
*
* Support: SAS(r) Solutions OnDemand
*
* Input: &input
*
* Output: (1) &out_cdays_rf
*         (2) &out_cost_rf
*         (3) &out_score_combined
*
* Parameters: 
*
* Dependencies/Assumptions: (1) %cf_score_hicams_inactive_duration
*
* Usage: Analysis
*
* History:
* 03Mar2020 kebaug | Initial creation 
* 01AUG2022 malima | NDT-12396: Changing hardcoded libname references to macros 
* 12AUG2022 malima | Comment out random forest binary filepaths and add them to master setup program
* 17AUG2022 jostov | Adding in ID variable for scoring code
* 11NOV2022 jostov | (C001) Adding business rule that predicted cost should not be less than the contract_bid_sa_amt. Related to NDT-11199
*                    Creating new variable amt_pc_wo_lm representing the actuals for a project but setting current month actual to 0 
*                       as to not affect remaining forecast amount.
* 09DEC2022 jostov | NDT-12999: Adding bill_paid_date_min_con_wo and bill_paid_date_max_con_wo to hicams_billing_new output dataset
* 06MAR2023 jostov | NDT-13455:(C002) Adding test code to top of program to be able to run independently in users playpen
*                    Changes all input/output datasets to be macro variables defined at the top of the program
*                    Updated post model output logic for determining pred_cal_days
* 28MAR2023 tawate | NDT-12652:(C003) Change fuel_adj to fuel_adj_cume
* 22APR2023 jostov | NDT-13523:(C004) Removing calculated item for amt_pc_wo_lm (actuals as of last month) since hicams_base_billing is now 
*                       being filtered to the forecast start date so no actuals in the current month will appear
* 23JAN2024 tawate | NDT-14634:(C005) Remove unnecessary proc esm code creating predicted non construction factors. 
* 19APR2024 jostov | (C006) Making output dataset hicams_model_noncume_con only have one row per contract
* 22JUL2024 jostov | NDT-16026:(C007) Temporary manual override of predicted cost and duration of C204953
* 22AUG2024 ayziau | NDT-14622:(C008) Remove old application variables we no longer need + remove other variables no longer used causing warnings
* 02DEC2024 parach | NDT-16341:(C009) Add macro call to cf_score_hicams_inactive_duration, removed calls to old inactive contract scoring macros
* 12DEC2024 tawate | NDT-14638:(C010) Creating hicams_scoring_2 as dedicated scoring code for cash_flow2.
*                    Remove static decision tree scoring macros. Remove scoring outputs from RF2 and RF4 models. 
*                    Remove post processing buisness rules related to pred_cal_days and pred_cost that did not improve accuracy.
* 05FEB2025 tawate | NDT-14638: Adding back the RD1 predicted calendar day adjustments.
* 17FEB2025 jostov | NDT-16827: Removing all code associated with the one-off adjustment of C204953 (NDT-16026 (C007))
* 24FEB2025 jostov | NDT-16810:(C011) Adjusting percent paid out cutoff from .5 to .75 for determining predicted cost (update from C002)
* 19MAY2025 tawate | NDT-16620: Remove all code associated with WBS model scoring.
\******************************************************************************/

/********** (C002) Run the code below if you want to run this independently ************/
/*%let _test_user = &sysuserid.; */
/**/
/*options nomlogic nomprint nosymbolgen; */
/*%include "/ndt/projects/cash_flow/&_test_user./sas/sasautos/util_interactive_setup.sas"; */
/*%util_interactive_setup(customer=ndt, project=cash_flow, user=&_test_user., cas=NO); */
/*%put _ALL_; */
/**/
/*libname uworklib "/ndt/warehouse/cash_flow/&_test_user./worklib/"; */
/*libname uwhouse "/ndt/warehouse/cash_flow/&_test_user./whouse/"; */
/*libname worklib "/ndt/warehouse/cash_flow2/ndtrun/worklib/" access = readonly; */
/*libname whouse "/ndt/warehouse/cash_flow2/ndtrun/whouse/" access = readonly; */
/*libname extract "/ndt/warehouse/cash_flow/ndtrun/extract/" access = readonly; */
/*libname nncstin "/ndt/warehouse/cash_flow2/ndtrun/whouse/nn_con_inact_cost";*/
/**/
/*%let rfdurin = /ndt/warehouse/cash_flow2/ndtrun/whouse/rf_con_inact_dur;*/
/**/
/*%let worklib = worklib; */
/*%let whouse = whouse; */
/*%let uwhouse = uwhouse; */
/*%let uworklib = uworklib; */
/*%let extract = extract; */
/*%let nncstin = nncstin; */
/**/
/**Input - prescore data (for calendar days and contract cost);*/
/*%let input              = &worklib..hicams_cume_modeling_prescore_v1;*/
/*%let dsin_model_enddate = &whouse..hicams_enddates;*/
/*%let dsin_hicams_con_lu = &worklib..hicams_contract_lookup;*/
/*%let dsin_billing_base  = &uworklib..hicams_billing_base;*/
/*%let dsin_cume_wo       = &worklib..hicams_cume_wo;*/
/*%let dsin_app_totals    = &worklib..cf_app_totals_by_date;*/
/**/
/**Output (scored) data;*/
/*%let out_score_combined          = &uworklib..hicams_score_combined_v1;*/
/*%let out_hicams_model_con        = &uwhouse..hicams_model_con;*/
/*%let out_hicams_model_noncum_con = &uwhouse..hicams_model_noncume_con;*/
/*%let out_hicams_bill_new         = &uwhouse..hicams_billing_new;*/
/*%let out_apps_by_date            = &uwhouse..apps_by_date;*/
/*%let out_apps_by_dt_comp         = &uwhouse..cf_apps_by_date_exp_compare;*/
/**/
/**Random Forest scoring data;*/
/*%let RF_score_cmos_pd       = "/ndt/warehouse/cash_flow2/ndtrun/whouse/rf_con_pd_cmos/forest_con_pd_last.sashdat";*/
/*%let RF_score_totcost_pd     = "/ndt/warehouse/cash_flow2/ndtrun/whouse/rf_con_pd_totcost/forest_con_pd_last.sashdat";*/
/*%let RF_score_cumecost_a_all = "/ndt/warehouse/cash_flow2/ndtrun/whouse/rf_wo_all_cumecost_01/forest_wo_a_last.sashdat";*/
/*%let RF_score_cumecost_f_all = "/ndt/warehouse/cash_flow2/ndtrun/whouse/rf_wo_all_cumecost_01/forest_wo_f_last.sashdat";*/
/**/
/*%let eff_date = ;*/
/**********************End of independent code setup****************************/

/*********************/
/* Define Parameters */
/*********************/

/* (C002) Comment out Input/Output datasets if running in playpen */
*Input - prescore data (for calendar days and contract cost);
%let input              = &worklib..hicams_cume_modeling_prescore_v1;
%let dsin_model_enddate = &whouse..hicams_enddates;
%let dsin_hicams_con_lu = &worklib..hicams_contract_lookup;
%let dsin_billing_base  = &worklib..hicams_billing_base;
%let dsin_cume_wo       = &worklib..hicams_cume_wo;
%let dsin_app_totals    = &worklib..cf_app_totals_by_date;

*output (scored) data;
%let out_score_combined          = &worklib..hicams_score_combined_v1;
%let out_hicams_model_con        = &whouse..hicams_model_con;
%let out_hicams_model_noncum_con = &whouse..hicams_model_noncume_con;
%let out_hicams_bill_new         = &whouse..hicams_billing_new;
%let out_apps_by_date            = &whouse..apps_by_date;
%let out_apps_by_dt_comp         = &whouse..cf_apps_by_date_exp_compare;

/* Target variables */
%let p_target_cmos_log  = p_target_cal_mos_log;
%let p_target_cost      = p_target_ratio_cost_cba_sa;

/* Adjustment factors */
%let factor_cost  = 1.005;
%let factor_cdays = 1.02; 

%let effective_date = &eff_date;

%if &effective_date. = %then %do;
	data _NULL_;
		format today date.;
		today = today();
		day   = day(today);
		month = month(today);
		year  = year(today);
		call symputx('today', put(today, date.));
	run; %put &today.;

	%let effective_date = &today;
%end;

/**************/
/* Score Code */
/**************/

data input_w_id;
	set &input.;
	%if %index(%upcase(&RF_score_cmos_pd.),.SASHDAT) %then %do; /*(C010) Changed to calendar months scoring path */
	ID = _N_;
	%end;
run;

/* Calendar days (RF - v1) */
%model_random_forest(
	dsin         = input_w_id,
	idvar        = contract_nbr,
	dsout_scored = rf_scored_con_pd_cmos,
	scorefilein  = &RF_score_cmos_pd. /*(C010)*/
	);

/* Contract cost (RF - v1) */
%model_random_forest(
	dsin         = input_w_id,
	idvar        = contract_nbr,
	dsout_scored = rf_scored_con_pd_totcost,
	scorefilein  = &RF_score_totcost_pd.
	);

/******************************/
/* Final Combined Scored Data */
/******************************/

/* Merge all scored datasets together */
proc sql; 
	create table temp_scored_combined_01 as 
	select 
        a.*
        ,ceil(10**b.&p_target_cmos_log.) as p_target_cmos_rf /*(C010) convert log of predicted calendar months to months*/
		,c.&p_target_cost.            	 as p_target_ratio_cost_cba_sa_rf
	from &input. a 
		left join rf_scored_con_pd_cmos     b on a.contract_nbr = b.contract_nbr
		left join rf_scored_con_pd_totcost  c on a.contract_nbr = c.contract_nbr
	;
quit;

/* Postprocessing for cost and duration on final combined dataset. (C010) Remove pred_cost and pred_cal_days post processing buiness rules */
data &out_score_combined.;*(drop=_rd1);
	set temp_scored_combined_01;

	/* Contract - Cost */
	pred_cost_rf    = p_target_ratio_cost_cba_sa_rf  * contract_bid_sa_amt;

    /* Adjust predicted cost if less than the current amount paid out */
	if pred_cost_rf < total_estimate_amount then do;
		pred_cost = total_estimate_amount * &factor_cost.; 
		flg_cost_pred_not_used = 1;
	end;
    else pred_cost = pred_cost_rf;

    /* (C002) When the project is less than 50% paid out, make sure the cost prediction is at least equal to the contract bid sa amt*/
    /* (C011) Adjusting percent paid out cutoff from 50% to 75% */
	if (total_estimate_amount/contract_bid_sa_amt) < .75 and pred_cost < contract_bid_sa_amt then pred_cost = contract_bid_sa_amt;
	
	pred_cost = round(pred_cost);

	format remaining_cost pred_cos: DOLLAR32.;
	remaining_cost    = pred_cost - total_estimate_amount;
	ratio_cost_remain = remaining_cost / contract_bid_sa_amt;

	/* Contract - Calendar Days */
    cal_days_final = coalesce(revised_calendar_days_up, calendar_days); *(C002)(C010);

    pred_cal_days = round(p_target_cmos_rf * 365/12); *(C010) convert predicted cal months to predicted cal days;
	pred_cal_days = coalesce(pred_cal_days, cal_days_final);
    
    /* Adjust predicted calendar days if much larger than revised calendar days*/
	if ^missing(revised_calendar_days_up) and pred_cal_days > 2 * revised_calendar_days_up then pred_cal_days = mean(revised_calendar_days_up, pred_cal_days);

    /* Adjust predicted calendar days if less than calendar days to date*/
	if pred_cal_days < calendar_days_to_date then do;
		pred_cal_days = calendar_days_to_date * &factor_cdays.; 
        flg_dur_pred_not_used = 1;
	end;
    pred_cal_days_org = pred_cal_days;

	_rd = pred_cal_days - calendar_days_to_date;
	if _rd ne . AND _rd < 20 then pred_cal_days = pred_cal_days + 20;
	remaining_dur = pred_cal_days - calendar_days_to_date;

	ratio_cost_per_day_p = remaining_cost        / remaining_dur;
	ratio_cost_per_day   = total_estimate_amount / calendar_days_to_date;
	ratio_cpd            = ratio_cost_per_day_p  / ratio_cost_per_day;
	format ratio_cost_per_da: DOLLAR32.2;

    /* (C002) The formulas/adjustments in this section are not explained as to what they were based on. 
    The calculation in the else if sometimes caused the pred_cal_days to get lower, making the problem worse. 
    Using the same adjustment (sqrt(2*ratio_cpd)) for all obs that meet this criteria as it always increased the duration.*/
	if ratio_cpd ge 1.5 AND ratio_cost_remain le 0.95 AND ratio_cost_remain ge 0.05 AND total_estimate_amount > 5000 then do;
		_F2    = 1 - (1 / exp(1/sqrt(ratio_cost_remain)));
        _rd1 = _F2 * remaining_dur * sqrt(2*ratio_cpd);
        rd1_org = _F2 * remaining_dur * sqrt(2*ratio_cpd);
        remaining_dur_org = remaining_dur;
		flg_dur_ratio_adj = 1;
	end;

	_rd1 = round(coalesce(_rd1, remaining_dur));

	if _rd1 > 3500 then do;
        _rd1 = remaining_dur;
        flg_rd1_3500 = 1;
    end;

	pred_cal_days_rd1 = pred_cal_days - remaining_dur + _rd1;
	pred_cal_days = pred_cal_days - remaining_dur + _rd1;

    /* (C002) Additional adjustments looking at percent complete and applying to projects that are in their earlier stages. 
    More detailed description in NDT-13455.*/
    cost_pct_complete = total_estimate_amount/contract_bid_sa_amt;
    cdays_pct_complete = calendar_days_to_date/cal_days_final;
    cost_to_days_pct_diff = cost_pct_complete - cdays_pct_complete;
    sum_pct_cost_cdays = sum(cost_pct_complete,cdays_pct_complete);

    pred_pct_complete_days = cal_days_final*(1-cost_to_days_pct_diff);
    p_cal_to_p_pct_ratio = (pred_cal_days - pred_pct_complete_days) / cal_days_final;
    abs_p_cal_to_p_pct_ratio = abs(p_cal_to_p_pct_ratio);

    if sum_pct_cost_cdays < 0.66 then do;
        if abs_p_cal_to_p_pct_ratio > 0.10 then do;
            flg_dur_pct_comp_adj = 1;
            if revised_calendar_days ne . then do;
                pred_cal_days_2 = round(((1-abs_p_cal_to_p_pct_ratio) * pred_cal_days) + (abs_p_cal_to_p_pct_ratio * pred_pct_complete_days));
            end;
            else do;
                pred_cal_days_3 = round(((1-(abs_p_cal_to_p_pct_ratio/2)) * pred_pct_complete_days) + ((abs_p_cal_to_p_pct_ratio/2) * pred_cal_days));
            end;
        end;
    end;
    
    pred_cal_days = coalesce(pred_cal_days_3, pred_cal_days_2, pred_cal_days);
	pred_cal_days = round(pred_cal_days);
	remaining_dur = _rd1; 

run;

proc sql; 
	create table &out_hicams_model_con. as 
		select distinct a.contract_nbr, a.flg_finished, round(a.pred_cal_days) as pred_cal_days, a.pred_cost, b.next_bill_day
			from &out_score_combined. a left join &dsin_model_enddate. b on a.contract_nbr = b.contract_nbr
	;
quit;

/* (C009) */
%cf_score_hicams_inctv_cost_dur(
                        dsin_hicams=&dsin_hicams_con_lu.,
                        dsout_hicams=temp_hicams_dur_cost_score,
                        min_months=1,
                        overwrite_model_date=
                        );

/* Non-cume HiCAMS */
data temp_hicams_noncume_score_01;
	set temp_hicams_dur_cost_score;
	format pred_cost DOLLAR32.;
	pred_cal_days = P_target_cal_days;
    /* Keep line below */
	if revised_calendar_days > 10 then pred_cal_days = coalesce(revised_calendar_days, pred_cal_days);
	pred_cost = round(min(P_target_ratio_cost_cba*contract_bid_amt, contract_bid_amt*1.1));
run;
proc sql; 
    create table temp_hicams_noncume_score_02 as 
        select distinct contract_nbr, calendar_days, revised_calendar_days, pred_cal_days, pred_cost
        from temp_hicams_noncume_score_01
        order by contract_nbr, pred_cal_days, pred_cost
	;    
quit;
data &out_hicams_model_noncum_con.;
    set temp_hicams_noncume_score_02;
    by contract_nbr pred_cal_days pred_cost;
    if last.contract_nbr;
run;

/* Global: Set max/min date macro vars from paid_date and end_date */
%hicams_global_dates(&dsin_billing_base.); %put Max end_date -> &max_end_date  Max paid_date -> &max_paid_date;

/* (C008): Update sql statement to remove warnings */
proc sql;
	create table temp_hicams_billing (drop = contract_nbr_temp flg_finished_temp) as 
		select a.*
			, b.*
			, a.ratio_con_cost_rec * b.pred_cost as pred_cost_wo format=DOLLAR32.
			/* (C001) Setting current month actuals to 0. Current month should not factor into remaining forecast amount on the project.  */
            /* (C004) Commenting out calculation for amt_pc_wo_lm */
/*			,case */
/*				when intnx("month", paid_date, 0, "B") = intnx("month", "&effective_date."d, 0, "B") then 0*/
/*				else amt_pc_wo*/
/*				end as amt_pc_wo_lm format=DOLLAR32.*/
		from &dsin_billing_base. a 
			left join &out_hicams_model_con. (rename = (contract_nbr = contract_nbr_temp flg_finished = flg_finished_temp) where=(flg_finished_temp ne 1)) b 
				on a.contract_nbr = b.contract_nbr_temp
		order by a.contract_nbr, a.estimate_nbr, a.estimate_wo_ident
	;
quit;


/* Create HiCAMs Billing New output data set */
data &out_hicams_bill_new.(rename=(latest_con_total_amt=total_con_amt)); 
	format key contract_nbr contract_wo_nbr type_of_contract 
		   application application_code app_abv  
		   primary_work_order_nbr work_order_nbr cnt_bill_dist_wo cnt_bill_dist_participating_cd 
           contract_type_desc contract_desc contract_type_cd est_day_cd location_desc physical_len 
		   billing_status flg_finished flg_active flg_wo_finished flg_wo_active
           proj_code_prim proj_code_prim_grp tip_nbr_primary tip_nbr tip_nbr2 tip_nbr3 tip_nbr4 
		   div division state_funded_indicator calendar_days revised_calendar_days total_cal_days
		   contract_bid_amt sa_amt contract_bid_sa_amt contract_bid_amt_wo contract_bid_sa_amt_wo 
		   latest_con_total_amt total_con_wo_amt hicams_my_date_min_con_wo hicams_my_date_max_con_wo hicams_end_date_min_con_wo hicams_end_date_max_con_wo hicams_paid_date_min_con_wo hicams_paid_date_max_con_wo
		   max_date_end max_date_paid
           bill_end_date_min_con_wo bill_end_date_max_con_wo bill_paid_date_min_con_wo bill_paid_date_max_con_wo
		   let_month let_year letting_dt letting_date 
		   acceptance_date contract_authorized_dt contract_execution_date work_start_date completion_date revised_completion_date actual_availability_date
           end_date paid_date my_date my_paid_date my_end_date 
		   estimate_type_cd participating_cd estimate_nbr estimate_ident calendar_days_to_date ratio_cume_cal_days_revised ratio_cume_cal_days_orig
           total_estimate_amount estimate_amt estimate_prev_amt fuel_adj_cume /*(C003)*/ 
		   estimate_wo_ident work_order_amt work_order_prev_amt work_order_retainage work_order_fuel_adj work_order_mpp_amt work_order_mpp_prev_amt work_order_pmt work_order_prev_pmt work_order_liq_damages
	;
	set temp_hicams_billing;
	keep key contract_n: contract_wo_nbr contract_desc location_desc tip: di: revise: work_order_n: flg_f: flg_a: contract_bid_: pred_: amt_pc_wo application_code application let: total_estimate_amount bill_end_date: bill_paid_date:
	     type_of_contract est_day_cd cale: estimate_nbr estimate_wo_ident estimate_type_cd total_con_wo_amt state_funded_indicator sa_amt acceptance_date contract_authorized_dt fuel_adj_cume /*(C003)*/ latest_con_total_amt
         contract_authorized_dt contract_execution_date end_date paid_date estimate_ident physical_len contract_type_desc contract_type_cd floating_avail_dt_ind
         proj_code_prim proj_code_prim_grp primary_work_order_nbr work_start_date estimate: work: purchase_order vegetation_ict_ind completion_date billing_status wo_days_since:
         incentive_bonus_ind participating_cd cnt_bill: hicams: flg_wo_: actual_availability_date contract_status_cd final_bill_rc:
		 /* (C008) */ application application_code app_abv project_type project_type_code group project_funding sub_type flag_express_db my_: total_cal_days wo_days: avail: max_date_end max_date_paid next_bill_day last_contract_bid_sa:
	;
	drop contract_bid_amt_0001 work_order_nbr_0001 calendar_days_0001 estimate_ident_0001 revised_calendar_days_0001;
run;


/*********/
/* OTHER */
/*********/
proc sql;
	create table WARN_amounts_wrong as 
		select distinct contract_nbr, sum(amt_pc_wo) as amt_pc_wo, total_con_amt, abs(sum(amt_pc_wo) - total_con_amt) as diff
			from &out_hicams_bill_new.
				group by contract_nbr
					having diff > 1
	;
	create table apps_by_date_end as 
		select distinct application, application_code, my_end_date as dt, sum(amt_pc_wo) as amt_end format=DOLLAR32.
			from &out_hicams_bill_new.
				where ^missing(application) 
					group by application, dt
                        order by application, dt
	;
	create table apps_by_date_paid_1 as 
		select distinct application, application_code, my_paid_date as dt, sum(amt_pc_wo) as amt_paid format=DOLLAR32.
			from &out_hicams_bill_new.
				where ^missing(application) 
					group by application, my_paid_date
                        order by application, dt
	;
quit;
data &out_apps_by_date.;
	merge apps_by_date_end apps_by_date_paid_1;
	by application dt;
run;

/***************************************************************/
/* (C005) Calculate non construction factors for maintenance projects */
/***************************************************************/
proc sql; 
	create table &out_apps_by_dt_comp.(where=(application_code in ('7839','7824','7841','7842') and ^missing(dt))) as 
	select a.*
		, month(a.dt) as month
		, b.total_expense - a.amt_paid as diff_zps_amt_paid format=DOLLAR32.
		, b.total_expense - a.amt_end  as diff_zps_amt_end  format=DOLLAR32.
		, b.total_expense as zps_amt_paid
		, amt_paid / b.total_expense as ratio_hicams_zps
		, 1 - (calculated ratio_hicams_zps) as prop_non_con
		, amt_end / b.total_expense as ratio_hicams_zps_end
		, 1 - (calculated ratio_hicams_zps_end) as prop_non_con_end
	from &out_apps_by_date. a 
		left join &dsin_app_totals.(where=(^missing(application_code))) b 
			on compress(upcase(a.application_code)) = compress(upcase(b.application_code)) and a.dt = b.date
	order by application, dt
;
quit;