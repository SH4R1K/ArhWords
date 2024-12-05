#!/usr/bin/env python
"""
Word Cloud with Custom Shape and Stop Words from NLTK
========================================================

Generating a word cloud from the US constitution using a custom shape and stop words from NLTK.
"""
import os
from os import path
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import nltk
from nltk.corpus import stopwords
import text_module as tm


# Загрузка стоп-слов NLTK
nltk.download('stopwords')

# get data directory
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
text = open(path.join(d, 'constitution.txt'), encoding="utf8").read()
# Load the mask image
mask_image = np.array(Image.open(path.join(d, 'black.png')))  # Замените 'black.png' на имя вашего файла маски

# Получение стоп-слов на русском языке
russian_stopwords = set(stopwords.words('russian'))

# Определение пользовательских стоп-слов (опционально)
custom_stopwords = set(STOPWORDS).union(russian_stopwords).union({"и", "в", "на", "с", "что", "как", "это", "по", "к", "для", "из", "но", "так", "же", "от", "то", "все", "также"})

# Generate a word cloud image with the mask and stop words
wordcloud = WordCloud(mask=mask_image, contour_color='black', contour_width=1,
                      stopwords=custom_stopwords, max_words=100).generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Save the word cloud image to a file
wordcloud.to_file(path.join(d, 'wordcloud_shape.png'))