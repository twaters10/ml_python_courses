/* First create the input dataset */
data input;
    input value;
    datalines;
10
15
20
25
30
;
run;

/* Calculate cumulative sum using SET statement */
data example;
    retain cume_sum 0;    /* Explicitly initialize cume_sum to 0 */
    set input;
    cume_sum = cume_sum + value;
run;

/* View the results */
proc print data=example;
    var value cume_sum;
run;

/* Run non-parametric smoothing using PROC LOESS */
proc loess data=example;
    model y = x;
    /* Default smoothing parameter selection method is used */
run;
/* Output the training model to a dataset */
ods output OutputStatistics=train_pred;

/* Create a scoring dataset */
data scoring;
    input x;
    datalines;
12
17
22
27
32
;
run;

/* Score new data using PROC LOESS */
proc loess data=example;
    model y = x;
    score data=scoring;
    ods output ScoreResults=score_pred;
run;

/* Print the scoring results */
proc print data=score_pred;
run;