#!/bin/bash

if [ -f ./vecs/all_d2v_f2_sw_vs500 ]; then
	echo "d2v_sw"
	python3 -u preprocess.py doc2vec -o 1 -s ./vecs/ft_d2v_f2_sw_vs500 -p ./data/news_ft.csv
	python3 -u preprocess.py doc2vec -o 1 -s ./vecs/usat_d2v_f2_sw_vs500 -p ./data/news_usat.csv
	python3 -u preprocess.py doc2vec -o 1 -s ./vecs/wsj_d2v_f2_sw_vs500 -p ./data/news_wsj.csv
	python3 -u preprocess.py doc2vec -o 1 -s ./vecs/all_d2v_f2_sw_vs500 -p ./data/news_ft.csv ./data/news_usat.csv ./data/news_wsj.csv
fi

if [ ! -f ./vecs/all_d2v_f2_vs500 ]; then
	echo "d2v"
	python3 -u preprocess.py doc2vec -s ./vecs/all_d2v_f2_vs500 -p ./data/news_ft.csv ./data/news_usat.csv ./data/news_wsj.csv  ./data/news_wsj.csv
	python3 -u preprocess.py doc2vec -s ./vecs/usat_d2v_f2_vs500 -p ./data/news_usat.csv
	python3 -u preprocess.py doc2vec -s ./vecs/ft_d2v_f2_vs500 -p ./data/news_ft.csv
	python3 -u preprocess.py doc2vec -s ./vecs/wsj_d2v_f2_vs500 -p ./data/news_wsj.csv
fi

if [ ! -f ./vecs/all_w2v_f2_sw_vs500 ]; then
	echo "w2v"
	python3 -u preprocess.py word2vec -s ./vecs/all_w2v_f2_sw_vs500 -p ./data/news_ft.csv ./data/news_usat.csv ./data/news_wsj.csv  ./data/news_wsj.csv
	python3 -u preprocess.py word2vec -s ./vecs/usat_w2v_f2_sw_vs500 -p ./data/news_usat.csv
	python3 -u preprocess.py word2vec -s ./vecs/ft_w2v_f2_sw_vs500 -p ./data/news_ft.csv
fi


# #-----------------------------------------------------------------------

date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_w2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 1 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_w2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 1 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_w2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 1 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_w2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 1 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_w2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 1 --model TextRNN_Att


date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_w2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 1 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_w2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 1 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_w2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 1 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_w2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 1 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_w2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 1 --model TextRNN_Att


date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_w2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 1 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_w2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 1 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_w2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 1 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_w2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 1 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_w2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 1 --model TextRNN_Att


#-----------------------------------------------------------------------
json="{\"text\":\"w2v_f2_sw local ok \"}"
curl -X POST -H 'Content-type: application/json' --data "$json" "https://hooks.slack.com/services/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"

#-----------------------------------------------------------------------

date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_sw_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model TextRNN_Att


date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_sw_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model TextRNN_Att


date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_sw_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model TextRNN_Att


#-----------------------------------------------------------------------
json="{\"text\":\"d2v_f2_sw local ok \"}"
curl -X POST -H 'Content-type: application/json' --data "$json" "https://hooks.slack.com/services/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"
#-----------------------------------------------------------------------

date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/all_d2v_f2_vs500 -d all -p 30 -a 4500 -m 2 -n 2 --model TextRNN_Att


date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/usat_d2v_f2_vs500 -d usat -p 30 -a 4500 -m 2 -n 2 --model TextRNN_Att

date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model TextCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model TextRNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model FastText
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model TextRCNN
date ; sleep 15 ; python3 -u run.py  -e ./vecs/ft_d2v_f2_vs500 -d ft -p 30 -a 4500 -m 2 -n 2 --model TextRNN_Att


# #-----------------------------------------------------------------------

json="{\"text\":\"d2v_f2 local ok \"}"
curl -X POST -H 'Content-type: application/json' --data "$json" "https://hooks.slack.com/services/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"

# #-----------------------------------------------------------------------