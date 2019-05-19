from nltk.tokenize import RegexpTokenizer

def lower_string(str):
    input_str = str.lower()
    #print(input_str)
    return input_str

def remove_punctuation(str):
    tokenizer = RegexpTokenizer(r'\w+')
    result = tokenizer.tokenize(str)
    #print(result)
    return ' '.join(result)

def preprocessing(str):
    return remove_punctuation(lower_string(str))