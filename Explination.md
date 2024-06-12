## Explanation of the Solution Approach

#### Libraries and Data Preparation
1. **Importing Libraries**: 
   - We started by importing necessary libraries such as `pandas`, `numpy`, `requests`, `BeautifulSoup`, and `nltk` for data manipulation, web scraping, and natural language processing.
   - We downloaded necessary NLTK resources like 'punkt' and 'stopwords' for tokenizing and stopword removal.

2. **Reading Input Data**:
   - Read the input data containing URLs using `pandas` `read_excel` function and dropping the `URL_ID` column.

#### Web Scraping
3. **Scraping Content and Title**:
   - For each URL in the DataFrame, we used `requests` to fetch the content and `BeautifulSoup` to parse the HTML.
   - We extracted the content and title using the appropriate HTML tags and classes. In cases where content or title is not found, we handled it by setting a default message.

4. **Combining Title and Content**:
   - Combined the title and content into a single string for further processing.

#### Text Processing
5. **Splitting and Cleaning Text**:
   - Converted the combined text into a pandas Series and split it into sentences based on the period (`.`) using regex to ensure proper sentence boundaries.
   - Exploded the list of sentences into individual rows in a DataFrame.
   - Cleaned the text by removing punctuation and empty rows.

6. **Reading Stopwords**:
   - Created a function to read stopwords from multiple files and stored them in DataFrames.

7. **Stopword Removal**:
   - Defined a function `text_process` to remove stopwords and punctuation from the text.

8. **Reading Positive and Negative Words**:
   - Created a function to read positive and negative words from provided files and processed them similarly to the stopwords.

#### Scoring Metrics Calculation
9. **Tokenization**:
   - Tokenized the cleaned text into words using NLTK's `word_tokenize`.

10. **Positive and Negative Scores**:
    - Calculated the positive and negative scores by comparing each word with the lists of positive and negative words respectively.

11. **Polarity and Subjectivity Scores**:
    - Calculated Polarity Score using the formula: `(Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)`
    - Calculated Subjectivity Score using the formula: `(Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)`

12. **Average Sentence Length**:
    - Calculated the average sentence length by averaging the lengths of each sentence in the cleaned text.

13. **Percentage of Complex Words**:
    - Defined complex words as those having more than two syllables and calculated their percentage in the text.

14. **Fog Index**:
    - Calculated the Fog Index using the formula: `0.4 * (avg_senetence_length + Percentage_of_Complex_words)`

15. **Average Number of Words per Sentence**:
    - Calculated the average number of words per sentence.

16. **Word Count and Syllables per Word**:
    - Counted the total number of words and syllables per word in the tokenized text.

17. **Personal Pronouns**:
    - Counted occurrences of personal pronouns like 'I', 'we', 'my', 'ours', 'us'.

18. **Average Word Length**:
    - Calculated the average word length in the tokenized text.

#### Output Generation
19. **Data Compilation and Export**:
    - Compiled all the calculated metrics into a DataFrame.
    - Exported the DataFrame to a CSV file named 'output.csv'.

## How to Run
Firstly, install all the Dependencies using the below command.

``` bash
pip install -r requirements.txt
```

Now you can directly run the ``` main.py ```
script

``` bash
python main.py
```
