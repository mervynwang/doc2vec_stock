#!/bin/bash

# collect
# pip3 install fake_useragent dateutil selenium bs4

# preprocess
# pip3 install nltk wordcloud matplotlib

# for run.py
pip3 install gensim numpy importlib argparse tqdm datetime pandas sklearn tensorboardX nltk

python -c "import nltk; nltk.download('punkt')"
python -c "import nltk; nltk.download('stopwords')"

# no gpu
pip3 install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html


