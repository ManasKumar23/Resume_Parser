import email
import nltk
import re
import subprocess
from pdfminer.high_level import extract_text
import requests
import docx2txt

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Extracting from the pdf
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

#Extracting email address
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

def extract_skills(input_text, SKILLS_DB):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
 
    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
 
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
 
    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
 
    # we create a set to keep the results in.
    found_skills = set()
 
    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)
 
    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram)
 
    return found_skills

# Create your views here.
def reader(request):
    if request.method == 'POST':
        SKILLS_DB = request.POST.get('SKILLS_DB')
        print(SKILLS_DB)
        pdffile=request.FILES['pdffile']
        print(pdffile)
        text = extract_text_from_pdf(pdffile)
        skills = extract_skills(text, SKILLS_DB)
        emails = extract_emails(text)
        
        #Print Emails
        if emails:
            print(emails[0])     

        #Print Skills
        if skills:
            print('skills' + str(skills))
        return HttpResponse(emails, skills)