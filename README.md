# Task-Oriented chatbot
<img src="https://cdn.technologyadvice.com/wp-content/uploads/2018/02/friendly-chatbot-700x408.jpg">

The project focuses on using NLP and other technologies to build a dialog system to analyse and answer the questions that students ask in terms of course units on University of Sydney education system.

|project start date|6/ 3/ 2019|
|:---:|:---:|

In this project my task is the natural language understand part, specifice the data preprocessing, intent classification and slot filling. about the intent classification and slot filling part, we consider a seq2seq method. 

In terms of the data prrprocessing, we consider the lower case and number word processing.

We introduce the NER for unit name and degree inforamtion.


## Dependency Packages for Chatbox
|package|version|
|:---:|:---:|
|||
|||

## feature

### the first step is to preprocess the input text

it is important to choose the necessary steps and make sure the result is useful for the
intent classification and slot filler part. For Cassandra project, The purpose of
preprocessing the text is to omit the length of the sentence, leaving the more
important part of the sentence to omit the less useful part of the sentence.

First, we need to convert all letters to lower case. In this step, we first unify the
text format so that we can follow the string matching and database operations.  
E.g  
The user's input is `"Hi, I want to know the lecturer address of COMP5426."`  
The output of this step is `"hi, i want to know the lecturer address of comp5426."`



## Architecture

## Preview

## Roadmap

## Discussion

