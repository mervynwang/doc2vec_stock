#!/bin/php
<?php


$list = [];
exec("find . -iname '*.log' | sort ", $list);

$exps = [];

class MyDB extends SQLite3
{
    function __construct()
    {
        $date = date("Ymd");
        $this->open('stock_'.$date.'.db');
    }
}

$db = new MyDB();
$db->exec(
    'CREATE TABLE result (
        ymd STRING,
        model STRING,
        pre_trained  STRING,
        input STRING,
        sw INTEGER,
        dataset STRING,
        batch   INTEGER,
        feq   INTEGER,
        p     INTEGER,
        acc_2020 REAL,
        acc_val REAL,
        info_2020 STRING,
        report_2020 STRING,
        info_val STRING,
        info_rand STRING,
        report_rand STRING,
        inClass INTEGER,
        vs   STRING,
        TimeUsage STRING,
        fn  STRING,
        args  STRING
    )'
);



foreach ($list as $fn) {
    $json = file_get_contents($fn);
    $info = json_decode($json, true);
    if (!$info) continue;

    $fnp = explode('/', $fn);
    $fnp[3] = str_replace('TextRNN_Att', 'TextRNN-Att', $fnp[3]);
    $ffp = explode('_', $fnp[3]);

    $vec = $ffp[1];
    $dd = date('Y-m-d_H:i:s', filemtime($fn));

    $tmp = [];
    $tmp["info_rand"] = [];
    $tmp["info_2020"] = [];
    $tmp["info_val"] = [];
    $tmp["dataset"] = $fnp[2]; // all ft usat
    $tmp["input"] = $ffp[2]; // title | arti
    $tmp["p"] = $ffp[3];    // 1 , 7 , 30
    $tmp['fn'] = $fnp[3];

    $tmp['feq'] = str_replace('mf', '', $ffp[5]);
    $tmp['inClass'] = ($ffp[7][0] == 'i')? str_replace('i', '', $ffp[7]) : 5 ;

    $tmp['ymd'] = $dd;
    $tmp['model'] = $ffp[0]; // CNN RNN
    $tmp['pre_trained'] = $ffp[1]; // d2v w2v
    $tmp["TimeUsage"] = '';
    $tmp["args"] = '';
    $tmp["acc_2020"] = 0;
    $tmp["acc_val"] = 0;
    $tmp['sw'] = 1;
    $tmp['vs'] = 500;
    $tmp['batch'] = 128;
    $tmp["report_2020"] = '';
    $tmp["report_rand"] = '';


    // echo "\n\n $ds $model : ". date('Y-m-d H:i:s', filemtime($fn)). " \n";
    $val = [];
    foreach ($info as $node) {
        if (isset($node['argv'])) {
            $tmp['args'] = $node['argv'];
            if ($tmp['pre_trained'] == 'd2v') {
                $tmp['sw'] = (strpos($node['argv'], '_sw') !== false)? 1 : 0;
            } else {
                $tmp['sw'] = 1;
            }

            $m = [];
            if(preg_match('/vs(\d+)/', $tmp['args'], $m)) {
                $tmp['vs'] = $m[1];
            }

            $m = [];
            if(preg_match('/-b (\d+)/', $tmp['args'], $m)) {
                $tmp['batch'] = $m[1];
            } else {
                $tmp['batch'] = 128;
            }
        }

        if (isset($node["i"])) {
            $val[] = $node["ValAcc"] ;
        }
        if (isset($node["TotalTimeUsage"])) {
            $tmp["TimeUsage"] = $node["TotalTimeUsage"];
        }

        if (isset($node["TestLoss"])) {
            $tmp2 = [];
            foreach ($node["ConfusionMatrix"] as $row) {
                $tmp2[] = join(" , ", $row);
            }
            // echo $tmp;
            $node["ConfusionMatrix"] = $tmp2;


            if (isset($node["tag"])) {
                $tmp["info_2020"] = json_encode($node, JSON_PRETTY_PRINT);
                $tmp["acc_2020"] = $node["TestAcc"]*100;
                $tmp["report_2020"] = $node["Report"];
            } else {
                $tmp["info_rand"]= json_encode($node, JSON_PRETTY_PRINT);
                $tmp["report_rand"] = $node["Report"];
            }

        }

    }

    if (!$tmp['args'] && ($tmp['pre_trained'] == 'd2v')) {
        $tmp['sw'] = 0;
    }

    $tmp["acc_val"] = (array_sum($val)/ count($val) * 100 );
    $tmp["info_val"] = json_encode($val);

    // insert;
    $stmt = $db->prepare(
        "INSERT INTO result (
            info_rand, info_2020, info_val,
            dataset, feq, inClass,
            input, sw, p, fn, batch,
            ymd, model ,pre_trained ,TimeUsage ,args,
            acc_2020 ,acc_val, vs,
            report_2020, report_rand
            ) VALUES (
            :info_rand, :info_2020, :info_val,
            :dataset, :feq, :inClass,
            :input, :sw , :p , :fn, :batch,
            :ymd , :model ,
            :pre_trained ,
            :TimeUsage ,
            :args ,
            :acc_2020 ,
            :acc_val, :vs,
            :report_2020, :report_rand
        )"
    );

    $intType = ['p', 'feq', 'inClass', 'sw', 'batch'];
    foreach ($tmp as $key => $value) {

        if (strpos($key, 'acc') !== false) {
            $stmt->bindParam(':'. $key, $tmp[$key], SQLITE3_FLOAT);
        } else if ( in_array($key, $intType) ) {
            $stmt->bindParam(':'. $key, $tmp[$key], SQLITE3_INTEGER);
        } else {
            $stmt->bindParam(':'. $key, $tmp[$key], SQLITE3_TEXT);
        }
    }
    // var_dump($stmt->getSQL(true));
    $stmt->execute();
}

?>