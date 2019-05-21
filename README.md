# Task-Oriented chatbot
<img src="https://cdn.technologyadvice.com/wp-content/uploads/2018/02/friendly-chatbot-700x408.jpg">

|project start date|6/ 3/ 2019|
|:---:|:---:|

The project focuses on using NLP and other technologies to build a dialog system to analyse and answer the questions that students ask in terms of course units on University of Sydney education system.  

In this project my task is the natural language understand part, specifice the data preprocessing, intent classification and slot filling. about the intent classification and slot filling part, we consider a seq2seq method.   
In terms of the data prrprocessing, we consider the lower case and number word processing.  
We introduce the NER for unit name and degree inforamtion.

## Dependency Packages for Chatbox
|package|version|
|:---:|:---:|
|||
|||

## feature

### preprocess the input text

it is important to choose the necessary steps and make sure the result is useful for the intent classification and slot filler part. For Cassandra project, The purpose of preprocessing the text is to omit the length of the sentence, leaving the more important part of the sentence to omit the less useful part of the sentence.

First, we need to convert all letters to lower case. In this step, we first unify the text format so that we can follow the string matching and database operations.  
E.g  
The user's input is `"Hi, I want to know the lecturer address of COMP5426."`  
The output of this step is `"hi, i want to know the lecturer address of comp5426."`
<img src="https://github.com/teddy-ssy/Task-oriented-chatbot/blob/master/reademe/preprocessing%201.png">

Second, converting numbers words into numbers, 
for the convenience of back slot matching, so in the preprocessing we need to convert numbers words into
numbers.  
E.g
`"comp five four two six"` appears in the user's question,So in the ability of people to understand, we know that users want to express`"comp5426"`, but it is more convenient to query numbers in the database than words,so you need to turn such digital words into numbers in the process of processing.

Third, removing stop words, 
when the user enters a sentence, although thesewords are necessary grammatically, they are not necessary for understanding thesentence. So in order to shorten the length of the sentence as much as possible, we
will remove stop words in this step.
E.g
The user's input is `"hi, i want to know the lecturer address of comp5426."`  
The output is `['hi', 'want', 'know', 'lecturer', 'address', 'comp5426']`  
In this sentence we can identify some components that appear frequently but have no meaning to the whole sentence, such as `“to”` and `“the”`.
<img src="https://github.com/teddy-ssy/Task-oriented-chatbot/blob/master/reademe/processing2.png">

To ensure the stop words set can conclude all stop word, It is necessary to select a open source stop words package. For this project, we downloaded the `NLTK stop word package`.

<img src="https://github.com/teddy-ssy/Task-oriented-chatbot/blob/master/reademe/preprocessing3.png">

### intent classification


## Architecture

## Preview

## Roadmap

## Discussion

