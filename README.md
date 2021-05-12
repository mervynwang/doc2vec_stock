
https://clay-atlas.com/blog/2020/01/16/pytorch-chinese-tutorial-sentiments-analyze-classification/
https://clay-atlas.com/blog/2020/01/21/python-chinese-pytorch-tutorial-reviews-sentiments-classification/


https://www.ft.com/todaysnewspaper/archive


https://www.wsj.com/market-data/quotes/GOOGL


use '' in cli


https://medium.com/swlh/sentiment-classification-using-word-embeddings-word2vec-aedf28fbb8ca


https://clay-atlas.com/blog/2020/01/17/python-chinese-tutorial-gensim-word2vec/


https://github.com/Currie32/Predicting-the-Dow-Jones-with-Headlines.git
https://medium.com/@Currie32/predicting-the-stock-market-with-the-news-and-deep-learning-7fc8f5f639bc


nn.Embedding() 讀取 Gensim 模型的方法
https://clay-atlas.com/blog/2020/07/05/pytorch-cn-note-how-to-load-pre-train-gensim-model-nn-embedding/


BOW + SVM / BOW + Naive Bayes
https://nlp.stanford.edu/pubs/sidaw12_simple_sentiment.pdf

Bayes -> good at snippets
svm -> full text

https://towardsdatascience.com/implementing-multi-class-text-classification-with-doc2vec-df7c3812824d

https://towardsdatascience.com/multi-class-text-classification-with-doc2vec-logistic-regression-9da9947b43f4


https://towardsdatascience.com/using-word2vec-to-analyze-news-headlines-and-predict-article-success-cdeda5f14751

refer:
https://arxiv.org/pdf/1408.5882v2.pdf
https://clay-atlas.com/blog/2019/10/20/pytorch-chinese-tutorial-classifier-cifar-10/
https://www.analyticsvidhya.com/blog/2020/01/first-text-classification-in-pytorch/
https://www.analyticsvidhya.com/blog/2019/09/introduction-to-pytorch-from-scratch/?utm_source=blog&utm_medium=building-image-classification-models-cnn-pytorch
https://github.com/graykode/xlnet-Pytorch

https://medium.com/analytics-vidhya/fine-tuning-xlnet-language-model-to-get-better-results-on-text-classification-8dfb96eb49ab


https://towardsdatascience.com/lstm-text-classification-using-pytorch-2c6c657f8fc0

***
https://pytorch.org/tutorials/beginner/text_sentiment_ngrams_tutorial.html
https://github.com/pytorch/text/tree/master/examples/text_classification
***


py train.py bayes -t ./result/bow_ft_tag.pkl -b ./result/bow_ft_title.pkl -e 'ft_title' >> ./result/train.log

stop word:
https://medium.com/@sfhsu29/nlp-%E5%85%A5%E9%96%80-1-2-stop-words-da3d311d29bc



py preprocess.py bar -p ./data/news_wsj.csv  -s ./result/wsj -a 30

py  preprocess.py doc2vec -p ./data/news_ft.csv -s ./models/ft_doc2vec 2>&1 >ft_d2v.log; \
py  preprocess.py doc2vec -p ./data/news_usat.csv -s ./models/usat_doc2vec 2>&1 >usat_d2v.log; \
py  preprocess.py doc2vec -p ./data/news_wsj.csv -s ./models/wsj_doc2vec 2>&1 >wsj_d2v.log


py  preprocess.py word2vec -p ./data/news_ft.csv -s ./models/ft_word2vec 2>&1 >ft_w2v.log; \
py  preprocess.py word2vec -p ./data/news_usat.csv -s ./models/usat_word2vec 2>&1 >usat_w2v.log; \
py  preprocess.py word2vec -p ./data/news_wsj.csv -s ./models/wsj_word2vec 2>&1 >wsj_w2v.log


py  preprocess.py doc2vec -p ./data/news_wsj.csv ./data/news_ft.csv ./data/news_usat.csv  -s ./models/all_doc2vec 2>&1 >all_d2v.log ; \
py  preprocess.py word2vec -p ./data/news_wsj.csv ./data/news_ft.csv ./data/news_usat.csv  -s ./models/all_word2vec 2>&1 >all_w2v.log &



py  preprocess.py bow -p ./data/news_ft.csv -s ./models/ft_bow 2>&1 >ft_bow.log & ; \
py  preprocess.py bow -p ./data/news_usat.csv -s ./models/usat_bow 2>&1 >usat_bow.log & ; \
py  preprocess.py bow -p ./data/news_wsj.csv -s ./models/wsj_bow 2>&1 >wsj_bow.log &



py  preprocess.py bar_ym -p ./data/news_ft.csv -s ./result/ft_ym -a 7 &
py  preprocess.py bar_ym -p ./data/news_usat.csv -s ./result/usat_ym -a 7 &
py  preprocess.py bar_ym -p ./data/news_wsj.csv -s ./result/wsj_ym  -a 7 &


124M Jan  6 12:48 ./log/all/saved_dict/TextRNN_d2v_a_7_ps4500_mf2_b128_i5.ckpt








1.

SELECT model,
(CASE pre_trained WHEN 'd2v' THEN '句向量' ELSE '詞向量' END) AS pre_process,
 ROUND(acc_val, 5) AS '驗證',
 ROUND(acc_2020, 5 ) AS '測試',

 -- TimeUsage,
 -- (CASE input WHEN 'a' THEN '全文' ELSE '標題' END) AS '輸入',
 -- (CASE sw WHEN 1 THEN '是'  ELSE '否' END) AS '去除常用字',
 dataset,
  vs, sw, dataset, feq, p, ps , info_2020, info_rand, fn, args

FROM result
WHERE 1 = 1
AND dataset = 'all'
AND input = 'a'
AND inClass = 5
AND p > 3
AND ps = 4500
AND vs = 500
AND ((pre_trained = 'd2v' AND sw = 0) OR pre_trained = 'w2v')
ORDER BY p, acc_val DESC




2.  區隔資料來源進行預測比較

SELECT model,
(CASE pre_trained WHEN 'd2v' THEN '句向量' ELSE '詞向量' END) AS pre_process,
 ROUND(acc_val, 5) AS '驗證',
 ROUND(acc_2020, 5 ) AS '測試',
 TimeUsage,
 (CASE input WHEN 'a' THEN '全文' ELSE '標題' END) AS '輸入',

 -- (CASE sw WHEN 1 THEN '是'  ELSE '否' END) AS '去除常用字',
 dataset,
  vs, sw, dataset, feq, p, ps , info_2020, info_rand, fn, args
FROM result
WHERE 1 = 1
AND dataset = 'all'
AND input = 'a'
AND pre_trained = 'd2v'
AND inClass = 5
AND p > 3
AND ps = 4500
AND vs = 500
-- AND ((input = 't' AND ps = 150) OR (input = 'a' AND ps = 4500))
AND ((pre_trained = 'd2v' AND sw = 0) OR pre_trained = 'w2v')
ORDER BY p, acc_val DESC







3. 比較標題及內文對預測精準度影響


SELECT model,
(CASE pre_trained WHEN 'd2v' THEN '句向量' ELSE '詞向量' END) AS pre_process,
(CASE input WHEN 'a' THEN '全文' ELSE '標題' END) AS '輸入',

 ROUND(acc_val, 5) AS '驗證',
 ROUND(acc_2020, 5 ) AS '測試',


 (CASE dataset
 	WHEN 'ft' THEN '金融時報' WHEN 'usat' THEN '今日美國' ELSE '全部' END) AS '資料源',

 -- (CASE sw WHEN 1 THEN '是'  ELSE '否' END) AS '去除常用字',
 -- TimeUsage,

  vs, sw, dataset, feq, p, ps , info_2020, info_rand, dataset,fn, args
FROM result
WHERE 1 = 1
-- AND input = 'a'
AND inClass = 5
AND p > 3
-- AND ps = 4500
-- AND vs = 500
AND ((input = 't' AND ps = 150) OR (input = 'a' AND ps = 4500))
-- AND ((pre_trained = 'd2v' AND sw = 0) OR pre_trained = 'w2v')
ORDER BY p, acc_val DESC





4. 在句向量去除常用字其影響

SELECT model,
(CASE pre_trained WHEN 'd2v' THEN '句向量' ELSE '詞向量' END) AS pre_process,
(CASE sw WHEN 1 THEN '是'  ELSE '否' END) AS '去除常用字',
 ROUND(acc_val, 5) AS '驗證',
 ROUND(acc_2020, 5 ) AS '測試',
 TimeUsage,


 -- (CASE input WHEN 'a' THEN '全文' ELSE '標題' END) AS '輸入',
 dataset,
  vs, sw, dataset, feq, p, ps , info_2020, info_rand, fn, args
FROM result
WHERE 1 = 1
AND dataset = 'all'
AND input = 'a'
AND pre_trained = 'd2v'
AND inClass = 5
AND p > 3
AND ps = 4500
AND vs = 500
-- AND ((input = 't' AND ps = 150) OR (input = 'a' AND ps = 4500))
-- AND ((pre_trained = 'd2v' AND sw = 0) OR pre_trained = 'w2v')
ORDER BY p, acc_val DESC






chp2.
  38459 for 127 form 19991015 - 20000210 NB  time serire
9128 (sp500) from 20020401 - 20021231 10-folder (4class) 公司新聞稿 only
406 from 20050301 - 20060531 BHP (Australian Financial Review)
2809  (sp500)  from 20051026 - 20051128
Bloomberg & Reuters
671751 for 11 ltd. from 200701-201203 (8 source Fr News) TFIDF/BOW
Twitter
(6652,  3433), 3586  2002-2011-2012 from 8K fin-report
(442933[20060210-20120618], 110733[20120619-20130221], 110733[201302-201311] ) 200610 - 201311
released by Ding et al. [2014]1. Randinsky et al. [2012] and Ding et al.
[2014] show that news titles are more useful for prediction compared to news contents. This paper extracts events only from news titles.
106521+447145 200610-201312
 20120521-20130918
(50448 3M,  130195 Google,  53782 Apple )20061010 - 20131126  news titles
 (56666,236 & 1426 169) from 20010104-20061229
yahoo & twitter (Social Network based)
2001-2008 JP news titles
530813  201001 - 201911 (include comments) doc2vec vector, 100~200 windows 5 & 10  002044.SZ 38486 ; other 14 303632 ;


