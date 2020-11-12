
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