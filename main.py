import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import string

nltk.download('punkt')
nltk.download('stopwords')

# Read input data
df = pd.read_excel('Input.xlsx')
df = df.drop('URL_ID', axis=1)

# Initialize the URL ID
url_id = 1

# Function to read stopwords
def read_stopwords(filepath):
    with open(filepath, 'r', encoding="ISO-8859-1") as file:
        stopwords = file.read().splitlines()
    return pd.DataFrame(stopwords, columns=['stopword'])

# Read stopwords from files
StopWords_Auditor = read_stopwords("./StopWords-20240612T123345Z-001/StopWords/StopWords_Auditor.txt")
StopWords_Currencies = read_stopwords("./StopWords-20240612T123345Z-001/StopWords/StopWords_Currencies.txt")
StopWords_DatesandNumbers = read_stopwords("./StopWords-20240612T123345Z-001/StopWords/StopWords_DatesandNumbers.txt")
StopWords_Generic = read_stopwords("./StopWords-20240612T123345Z-001/StopWords/StopWords_Generic.txt")
StopWords_GenericLong = read_stopwords("./StopWords-20240612T123345Z-001/StopWords/StopWords_GenericLong.txt")
StopWords_Geographic = read_stopwords("./StopWords-20240612T123345Z-001/StopWords/StopWords_Geographic.txt")
StopWords_Names = read_stopwords("./StopWords-20240612T123345Z-001/StopWords/StopWords_Names.txt")

# Function to process text
def text_process(text):
    punc = [punc for punc in string.punctuation]
    nopunc = [char for char in text if char not in punc or char not in [':', ',', '(', ')', '’', '?']]
    nopunc = ''.join(nopunc)
    txt = ' '.join([word for word in nopunc.split() if word.lower() not in StopWords_Auditor['stopword'].values])
    txt1 = ' '.join([word for word in txt.split() if word.lower() not in StopWords_Currencies['stopword'].values])
    txt2 = ' '.join([word for word in txt1.split() if word.lower() not in StopWords_DatesandNumbers['stopword'].values])
    txt3 = ' '.join([word for word in txt2.split() if word.lower() not in StopWords_Generic['stopword'].values])
    txt4 = ' '.join([word for word in txt3.split() if word.lower() not in StopWords_GenericLong['stopword'].values])
    txt5 = ' '.join([word for word in txt4.split() if word.lower() not in StopWords_Geographic['stopword'].values])
    return ' '.join([word for word in txt5.split() if word.lower() not in StopWords_Names['stopword'].values])

# Process each URL and calculate scores
for i in range(len(df)):
    j = df.iloc[i].values
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    page = requests.get(j[0], headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.findAll(attrs={'class': 'td-post-content'})
    if content:
        content_text = content[0].text.replace('\xa0', "  ").replace('\n', "  ")
    else:
        content_text = "Content not found"
    title = soup.findAll(attrs={'class': 'entry-title'})
    if title:
        if len(title) > 16:
            title_text = title[16].text.replace('\n', "  ").replace('/', "")
        else:
            title_text = "Title not found"
    else:
        title_text = "Title not found"
    text = title_text + '.' + content_text
    df1 = pd.Series([text])
    url_id += 1

# Convert text to pandas Series
text = pd.Series(text)

# Splitting and cleaning text
a = text.str.split(r'(?<=[.])\s', expand=False)
b = a.explode()
b = pd.DataFrame(b, columns=['abc'])

def abcd(x):    
    nopunc =[char for char in x if char != '.']
    return ''.join(nopunc)

b['abc'] = b['abc'].apply(abcd)
c = b.replace('', np.nan, regex=True)
c = c.mask(c == " ")
c = c.dropna()
c.reset_index(drop=True, inplace=True)
c['abc'] = c['abc'].apply(text_process)

# Read positive and negative words
def read_words(filepath, encoding=None):
    with open(filepath, 'r', encoding=encoding) as file:
        words = file.read().splitlines()
    return pd.DataFrame(words, columns=['word'])

positive = read_words("./MasterDictionary-20240612T123345Z-001/MasterDictionary/positive-words.txt")
negative = read_words("./MasterDictionary-20240612T123345Z-001/MasterDictionary/negative-words.txt", encoding="ISO-8859-1")

positive.columns = ['abc']
negative.columns = ['abc']
positive['abc'] = positive['abc'].astype(str)
negative['abc'] = negative['abc'].astype(str)

# Process positive and negative words
positive['abc'] = positive['abc'].apply(text_process)
negative['abc'] = negative['abc'].apply(text_process)

# Create positive and negative word lists
positive_words = positive['abc'].tolist()
negative_words = negative['abc'].tolist()

# Convert cleaned text to list and tokenize
txt_list = [' '.join([word for word in c.iloc[i]]) for i in range(c.shape[0])]
tokenize_text = [word_tokenize(i) for i in txt_list]
tokenize_text = [word for sublist in tokenize_text for word in sublist]

# Calculate scores
positive_score = sum(1 for word in tokenize_text if word.lower() in positive_words)
negative_score = sum(1 for word in tokenize_text if word.lower() in negative_words)
Polarity_Score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
subjectivity_score = (positive_score + negative_score) / (len(tokenize_text) + 0.000001)

# Average sentence length
avg_sentence_length = sum(len(c['abc'].iloc[i]) for i in range(c.shape[0])) / c.shape[0]

# Percentage of complex words
vowels = 'aeiou'
complex_word_count = sum(1 for word in tokenize_text if sum(1 for char in word if char in vowels) > 2)
percentage_of_complex_words = complex_word_count / len(tokenize_text)

# Fog index
fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)

# Average number of words per sentence
avg_words_per_sentence = sum(len(sentence.split()) for sentence in c['abc']) / len(c)

# Complex word count
complex_word_count = sum(1 for word in tokenize_text if sum(1 for char in word if char in vowels) > 2)

# Word count
word_count = len(tokenize_text)

# Syllables per word
syllable_count = sum(1 for word in tokenize_text for char in word if char in vowels)

# Personal pronouns
pronouns = ['i', 'we', 'my', 'ours', 'us']
personal_pronouns = sum(1 for word in tokenize_text if word.lower() in pronouns)

# Average word length
avg_word_length = sum(len(word) for word in tokenize_text) / len(tokenize_text)

# Compile data into DataFrame and save to CSV
data = {
    'positive_score': positive_score,
    'negative_score': negative_score,
    'Polarity_Score': Polarity_Score,
    'subjectivity_score': subjectivity_score,
    'avg_sentence_length': avg_sentence_length,
    'Percentage_of_Complex_words': percentage_of_complex_words,
    'Fog_Index': fog_index,
    'avg_words_per_sentence': avg_words_per_sentence,
    'complex_word_count': complex_word_count,
    'word_count': word_count,
    'syllable_count': syllable_count,
    'personal_pronouns': personal_pronouns,
    'avg_word_length': avg_word_length
}

output = pd.DataFrame([data])
output.to_csv('output.csv', index=False)
