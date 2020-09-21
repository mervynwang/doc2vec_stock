


https://www.ft.com/todaysnewspaper/archive


https://www.wsj.com/market-data/quotes/GOOGL


use '' in cli


https://medium.com/swlh/sentiment-classification-using-word-embeddings-word2vec-aedf28fbb8ca


https://clay-atlas.com/blog/2020/01/17/python-chinese-tutorial-gensim-word2vec/


https://github.com/Currie32/Predicting-the-Dow-Jones-with-Headlines.git
https://medium.com/@Currie32/predicting-the-stock-market-with-the-news-and-deep-learning-7fc8f5f639bc



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



py train.py bayes -t ./result/bow_ft_tag.pkl -b ./result/bow_ft_title.pkl -e 'ft_title' >> ./result/train.log

stop word:
https://medium.com/@sfhsu29/nlp-%E5%85%A5%E9%96%80-1-2-stop-words-da3d311d29bc



py preprocess.py bar -p ./data/news_wsj.csv  -s ./result/wsj -a 30
