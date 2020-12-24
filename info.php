#!/bin/php
<?php


$list = [];
exec("find . -iname '*.log' | sort ", $list);

$exps = [];

class MyDB extends SQLite3
{
    function __construct()
    {
        $date = date("Ymd_H");
        $this->open('stock_'.$date.'.db');
    }
}

$db = new MyDB();
$db->exec(
    'CREATE TABLE result (
        ymd STRING,
        fn  STRING,
        args  STRING,
        model STRING,
        pretrian  STRING,
        input STRING,
        dateset STRING,
        p     INTEGER,
        TimeUsage STRING,
        acc_2020 REAL,
        acc_val REAL,
        info STRING
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
    $tmp["info"] = [];
    $tmp["dateset"] = $fnp[2]; // all ft usat
    $tmp["input"] = $ffp[2]; // title | arti
    $tmp["p"] = $ffp[3];    // 1 , 7 , 30
    $tmp['fn'] = $fnp[3];
    $tmp['ymd'] = $dd;
    $tmp['model'] = $ffp[0]; // CNN RNN
    $tmp['pretrian'] = $ffp[1]; // d2v w2v
    $tmp["TimeUsage"] = '';
    $tmp["args"] = '';
    $tmp["acc_2020"] = 0;
    $tmp["acc_val"] = 0;


    // echo "\n\n $ds $model : ". date('Y-m-d H:i:s', filemtime($fn)). " \n";
    $val = [];
    foreach ($info as $node) {
        if (isset($node['argv'])) {
            $tmp['args'] = $node['argv'];
        }

        if (isset($node["i"])) {
            $val[] = $node["ValAcc"];
        }
        if (isset($node["TotalTimeUsage"])) {
            $tmp["TimeUsage"] = $node["TotalTimeUsage"];
        }

        if (isset($node["TestLoss"])) {
            $tmp2 = "";
            foreach ($node["ConfusionMatrix"] as $row) {
                $tmp2 .= join(" , ", $row)."\n";
            }
            // echo $tmp;
            $node["ConfusionMatrix"] = $tmp2;

            if (isset($node["tag"])) {
                $tmp["info"]["Anl2"] = $node;
                $tmp["acc_2020"] = $node["TestAcc"]*100;
            } else {
                $tmp["info"]["Anl"] = $node;
            }

        }

    }
    $tmp["acc_val"] = (array_sum($val)/ count($val) * 100 );
    $tmp["info"]["batch"] = join(', ', $val);
    $tmp["info"] = json_encode($tmp["info"]);

    // insert;
    $stmt = $db->prepare(
        "INSERT INTO result (info, dateset, input, p, fn,
            ymd, model ,pretrian ,TimeUsage ,args
            ,acc_2020 ,acc_val
            ) VALUES (
            :info,
            :dateset ,
            :input ,
            :p ,
            :fn ,
            :ymd ,
            :model ,
            :pretrian ,
            :TimeUsage ,
            :args ,
            :acc_2020 ,
            :acc_val
        )"
    );
    foreach ($tmp as $key => $value) {
        if (strpos($key, 'acc') !== false) {
            $stmt->bindParam(':'. $key, $tmp[$key], SQLITE3_FLOAT);
        } else if ($key == 'p') {
            $stmt->bindParam(':'. $key, $tmp[$key], SQLITE3_INTEGER);
        } else {
            $stmt->bindParam(':'. $key, $tmp[$key], SQLITE3_TEXT);
        }
    }
    // var_dump($stmt->getSQL(true));
    $stmt->execute();
}

?>