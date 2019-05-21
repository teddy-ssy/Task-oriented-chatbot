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


## Architecture

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

### Word Embedding

we decided to use an open source word vector library. For the specific course name, the teacher name data is solved by the stream matching method.
<img src="https://github.com/teddy-ssy/Task-oriented-chatbot/blob/master/reademe/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-05-21%20%E4%B8%8B%E5%8D%8810.00.12.png">

### intent classification

Understanding user intent is the first step in the next steps. From the user's intent, we then choose which logic to use to get the desired result based on the logical logic of the backend. Based on the intent category and the raw question training set designed above. We decided to implement this model using the seq2seq method, the model is divided into two parts: encoder and decoder.
In encoder part, after review few method ,the Bi-LSTM structure is the most popular one structure used for encoder. At the beginning, it is need define two LSTM cell for forward and backward. We keep the output prob equal to 0.5, This is an effective regularization method that can effectively prevent overfitting.
<img src="https://github.com/teddy-ssy/Task-oriented-chatbot/blob/master/reademe/intent1.png">
Then we use the bidirectional_dynamic_rnn to train the input data to the finial
hidden layer state and the output of the structure.
<img src="https://github.com/teddy-ssy/Task-oriented-chatbot/blob/master/reademe/intent2.png">
The decoder part for intent classification is more simpler compared with the slot
filler. The output only one value, then it can be return by a argmax layer. The input of
the this layer is the final hidden layer state.
<img src="https://github.com/teddy-ssy/Task-oriented-chatbot/blob/master/reademe/intent3.png">





## Roadmap

## Discussion

