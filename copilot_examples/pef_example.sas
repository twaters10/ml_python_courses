/******************************************************************************\
* $Id$
*
* Copyright(c) 2023 SAS Institute Inc., Cary, NC, USA. All Rights Reserved.
*
* Name: cf_payouts_03_clusmem_train.sas
*
* Purpose: Train cluster membership models
*
* Author: Taylor Waters (tawate)
*
* Support: SAS(r) Solutions OnDemand
*
* Input: 
*
* Output: 
*
* Parameters: 
*
* Dependencies/Assumptions: cash_flow/sasautos/cf_payouts_clusmem_train_wrapper.sas
*
* Usage: Analytics
*
* History:
* 25APR2025 tawate | NDT-16620: Initial creation 
* 19MAY2025 tawate | NDT-16620: Add proc loess model for NA projects
\******************************************************************************/

%if &cf_payouts_good_to_train. = 1 %then %do;

    * Output Datasets;
    %let dsout_db_loess_lkup = &whouse..cf_payouts_db_loess_lkup;
    %let dsout_na_loess_lkup = &whouse..cf_payouts_na_loess_lkup;
    
    * STIP (C-Let) ;
    %cf_payouts_clusmem_train_wrapper( 
        _clusgroup_             = clet,
        _idvar_                 = contract_nbr,
        _input_attributes_      = &input_attributes_clet.,
        _input_hierarchy_       = &input_hierarchy_clet.,
        _roletable_             = CF_CUME_analysis_roles_wo_1st_int.csv,
        _modelpathname_         = bin_clet_wo_25pct,
        _model_output_table_    = model_param_RF_MCLMC_clet_wo_25pct.csv);

    %cf_payouts_clusmem_train_wrapper( 
        _clusgroup_             = clet,
        _idvar_                 = contract_nbr,
        _input_attributes_      = &input_attributes_clet.,
        _input_hierarchy_       = &input_hierarchy_clet.,
        _roletable_             = CF_CUME_analysis_roles_w_25pct.csv,
        _modelpathname_         = bin_clet_w_25pct,
        _model_output_table_    = model_param_RF_MCLMC_clet_w_25pct.csv);


    * STIP (D-Let) ;
    %cf_payouts_clusmem_train_wrapper( 
        _clusgroup_             = dlet,
        _idvar_                 = contract_nbr,
        _input_attributes_      = &input_attributes_dlet.,
        _input_hierarchy_       = &input_hierarchy_dlet.,
        _roletable_             = CF_CUME_analysis_roles_wo_1st_int.csv,
        _modelpathname_         = bin_dlet_wo_1st_int,
        _model_output_table_    = model_param_RF_MCLMC_dlet_wo_1st_int.csv);

    %cf_payouts_clusmem_train_wrapper( 
        _clusgroup_             = dlet,
        _idvar_                 = contract_nbr,
        _input_attributes_      = &input_attributes_dlet.,
        _input_hierarchy_       = &input_hierarchy_dlet.,
        _roletable_             = CF_CUME_analysis_roles_w_1st_int.csv,
        _modelpathname_         = bin_dlet_w_1st_int,
        _model_output_table_    = model_param_RF_MCLMC_dlet_w_1st_int.csv);


    * CR/PP ;
    %cf_payouts_clusmem_train_wrapper( 
        _clusgroup_             = crpp,
        _idvar_                 = contract_nbr,
        _input_attributes_      = &input_attributes_crpp.,
        _input_hierarchy_       = &input_hierarchy_crpp.,
        _roletable_             = CF_CUME_analysis_roles_wo_1st_int.csv,
        _modelpathname_         = bin_crpp_wo_1st_int,
        _model_output_table_    = model_param_RF_MCLMC_crpp_wo_1st_int.csv);

    %cf_payouts_clusmem_train_wrapper( 
        _clusgroup_             = crpp,
        _idvar_                 = contract_nbr,
        _input_attributes_      = &input_attributes_crpp.,
        _input_hierarchy_       = &input_hierarchy_crpp.,
        _roletable_             = CF_CUME_analysis_roles_w_1st_int.csv,
        _modelpathname_         = bin_crpp_w_1st_int,
        _model_output_table_    = model_param_RF_MCLMC_crpp_w_1st_int.csv);


    * BP/BPR ;
    %cf_payouts_clusmem_train_wrapper( 
        _clusgroup_             = bpbpr,
        _idvar_                 = contract_nbr,
        _input_attributes_      = &input_attributes_bpbpr.,
        _input_hierarchy_       = &input_hierarchy_bpbpr.,
        _roletable_             = CF_CUME_analysis_roles_wo_1st_int.csv,
        _modelpathname_         = bin_bpbpr_wo_1st_int,
        _model_output_table_    = model_param_RF_MCLMC_bpbpr_wo_1st_int.csv);

    %cf_payouts_clusmem_train_wrapper( 
        _clusgroup_             = bpbpr,
        _idvar_                 = contract_nbr,
        _input_attributes_      = &input_attributes_bpbpr.,
        _input_hierarchy_       = &input_hierarchy_bpbpr.,
        _roletable_             = CF_CUME_analysis_roles_w_1st_int.csv,
        _modelpathname_         = bin_bpbpr_w_1st_int,
        _model_output_table_    = model_param_RF_MCLMC_bpbpr_w_1st_int.csv);


    /* Design Build Loess Curve */
    data pct_dur_lkup;
        do pct_dur = 0.001 to 1.000 by 0.001;
            output;
        end;
    run;

    data cf_payouts_db_loess_prep;
        set &permlib94..cf_payouts_prep_db;
        * Use Percent Dur and Cumulative Payouts vars after payout curves are trimmed for anomolies;
        pct_dur = pct_dur_post_cutoff;
        payout_ratio_cume = payout_ratio_cume_cutoff;
    run;

    /* Train and Score with Proc Loess */
    proc loess data=cf_payouts_db_loess_prep plots=none;
        model payout_ratio_cume = pct_dur / select=AICC;                * AICC-based smoothing selection;
        output out=db_fit_cost_train predicted=p_payout_ratio_cume;
        score data=pct_dur_lkup;                                        * apply model to new data;
        ods Output scoreresults = cf_payouts_db_lkup_tmp;               * output scoring file;
    run;

    /* Reassign predicted cumulative ratios vars if > 1 or missing */
    proc sql;
        create table &dsout_db_loess_lkup. as
        select
            'DB' as clus_group 
            ,round(t1.pct_dur,.001) as pct_dur
            ,t1.p_payout_ratio_cume as p_payout_ratio_cume_orig
            ,case   when t1.p_payout_ratio_cume > 1 then 1 
                    when t1.p_payout_ratio_cume = . and t1.pct_dur < t2.pct_dur then t2.min_payout_ratio_cume 
                    else t1.p_payout_ratio_cume end as p_payout_ratio_cume
            ,t2.min_payout_ratio_cume
            ,t2.pct_dur as min_pct_dur
        from cf_payouts_db_lkup_tmp t1
        inner join (select distinct scoredata, pct_dur, p_payout_ratio_cume, min(p_payout_ratio_cume) as min_payout_ratio_cume 
                    from cf_payouts_db_lkup_tmp having min_payout_ratio_cume = p_payout_ratio_cume) t2 on t1.scoredata = t2.scoredata
        ;
    quit;

    /* N/A Loess Curve Data Prep*/
    data cf_payouts_na_df_loess_prep cf_payouts_na_oth_loess_prep;
        set &permlib94..cf_payouts_prep_na;
        * Use Percent Dur and Cumulative Payouts vars after payout curves are trimmed for anomolies;
        pct_dur = pct_dur_post_cutoff;
        payout_ratio_cume = payout_ratio_cume_cutoff;

        if project_type = 'Disaster' then do;
            project_type_disaster = 'Y';
            output cf_payouts_na_df_loess_prep;
        end; 
        else do;
            project_type_disaster = 'N';
            output cf_payouts_na_oth_loess_prep;
        end;
    run;
    
    /* Train and Score with Proc Loess */
    proc loess data=cf_payouts_na_df_loess_prep plots=none;
        model payout_ratio_cume = pct_dur / select=AICC;                * AICC-based smoothing selection;
        output out=na_df_fit_cost_train predicted=p_payout_ratio_cume;
        score data=pct_dur_lkup;                                        * apply model to new data;
        ods Output scoreresults = cf_payouts_na_df_lkup_tmp;            * output scoring file;
    run;

    proc loess data=cf_payouts_na_oth_loess_prep plots=none;
        model payout_ratio_cume = pct_dur / select=AICC;                * AICC-based smoothing selection;
        output out=na_oth_fit_cost_train predicted=p_payout_ratio_cume;
        score data=pct_dur_lkup;                                        * apply model to new data;
        ods Output scoreresults = cf_payouts_na_oth_lkup_tmp;           * output scoring file;
    run;

    /* Reassign predicted cumulative ratios vars if > 1 or missing for Disaster Project Types and Other Projet Types separately*/
    /* Disaster Project Types */
    proc sql;
        create table cf_payouts_na_df_lkup_tmp2 as
        select
            'N/A' as clus_group
            ,'Y' as project_type_disaster 
            ,round(t1.pct_dur,.001) as pct_dur
            ,t1.p_payout_ratio_cume as p_payout_ratio_cume_orig
            ,case   when t1.p_payout_ratio_cume > 1 then 1 
                    when t1.p_payout_ratio_cume = . and t1.pct_dur < t2.pct_dur then t2.min_payout_ratio_cume 
                    else t1.p_payout_ratio_cume end as p_payout_ratio_cume
            ,t2.min_payout_ratio_cume
            ,t2.pct_dur as min_pct_dur
        from cf_payouts_na_df_lkup_tmp t1
        inner join (select distinct scoredata, pct_dur, p_payout_ratio_cume, min(p_payout_ratio_cume) as min_payout_ratio_cume 
                    from cf_payouts_na_df_lkup_tmp having min_payout_ratio_cume = p_payout_ratio_cume) t2 on t1.scoredata = t2.scoredata
        ;
    quit;

    /* Non-Disaster Project Types */
    proc sql;
        create table cf_payouts_na_oth_lkup_tmp2 as
        select
            'N/A' as clus_group
            ,'N' as project_type_disaster 
            ,round(t1.pct_dur,.001) as pct_dur
            ,t1.p_payout_ratio_cume as p_payout_ratio_cume_orig
            ,case   when t1.p_payout_ratio_cume > 1 then 1 
                    when t1.p_payout_ratio_cume = . and t1.pct_dur < t2.pct_dur then t2.min_payout_ratio_cume 
                    else t1.p_payout_ratio_cume end as p_payout_ratio_cume
            ,t2.min_payout_ratio_cume
            ,t2.pct_dur as min_pct_dur
        from cf_payouts_na_oth_lkup_tmp t1
        inner join (select distinct scoredata, pct_dur, p_payout_ratio_cume, min(p_payout_ratio_cume) as min_payout_ratio_cume 
                    from cf_payouts_na_oth_lkup_tmp having min_payout_ratio_cume = p_payout_ratio_cume) t2 on t1.scoredata = t2.scoredata
        ;
    quit;

    /* Combine NA group predicted loess curves */
    data &dsout_na_loess_lkup.;
        set cf_payouts_na_df_lkup_tmp2 cf_payouts_na_oth_lkup_tmp2;
    run;

    /* Copy Design Build and NA payout lookup tables to cash flow 1*/
    libname cf1 "/ndt/warehouse/cash_flow/&_USERID./whouse";
    proc copy in=&whouse. out=cf1;
       select   cf_payouts_db_loess_lkup
                cf_payouts_na_loess_lkup;
    run;
    libname cf1 clear;

%end;

%else %do;
    %put RUN CONDITIONS NOT MET: WILL NOT TRAIN CLUSTER MEMBERSHIP MODEL;
%end;
