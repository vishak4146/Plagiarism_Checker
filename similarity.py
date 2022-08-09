# Importing the necessary libraries
import nltk
import websearch
from difflib import SequenceMatcher
import pandas as pd
from gingerit.gingerit import GingerIt

# Using the nltk we are downloading the necessary libraries
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(nltk.corpus.stopwords.words('english'))


# Method declared to clean our string using EDA analysis
def cleanText(string):
    words = nltk.word_tokenize(string)
    return " ".join([word for word in words if word not in stop_words])


# Method declared to search our query passed from front end to all the matching sites after
# going through cleaning process
def verifyQuery(string, results_per_sentence):
    sentences = nltk.sent_tokenize(string)
    matching_sites = []
    n = 0
    for url in websearch.searchWeb(query=string, num=results_per_sentence):
        matching_sites.append(url)
        n += 1
        if n == 10:
            break
    for sentence in sentences:
        for url in websearch.searchWeb(query=sentence, num=results_per_sentence):
            matching_sites.append(url)
            break
    return list(set(matching_sites))


# Method declared to calculate the similarity score
def similarityScore(str1, str2):
    return (SequenceMatcher(None, str1, str2).ratio()) * 100


# Method for verifying our text with all the matching sites using websearch library
def report(text):
    matching_sites = verifyQuery(cleanText(text), 2)
    matches = {}
    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarityScore(text, websearch.extractionOfText(matching_sites[i]))
    matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}
    return matches


# Method to get the values from dictionary
def returnMatchingSites(dictionary):
    df = pd.DataFrame({'Similarity (%)': dictionary})
    return dictionary


# Method for obtaining the grammar module
def getGrammarCorrections(text_input):
    parser = GingerIt()
    resultText = parser.parse(text_input)
    return resultText['result']


if __name__ == '__main__':
    report('This is a pure test')
