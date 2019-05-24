import csv
from NLU.constants import *

def csv2dictionary(filename):
    with open(filename, newline='') as csvfile:
        title = 0
        dict={}
        title_list=[]
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            #print(row)
            #print("\n")
            if title ==1:
                for item in range(len(row)):
                    if row[item] != '':
                        dict[row[item].lower()]=title_list[item].lower()
            else:
                for item in row:
                    item = item.lower()
                    #dict[item]=[]
                    title_list.append(item)
                    dict[item]=item

                title=1

    return dict

def matching(sentence,dict):
    #dict={'level dose': 'weeks', 'COMP5703': 'unitcode'}
    sentence = sentence.lower()
    sentence_list = sentence.split(' ')
    sentence_slot = []
    for item in sentence_list:
        sentence_slot.append('O')

    for item in dict.keys():
        #print(item)
        num=sentence.find(item)
        #print(num)
        if num != -1:
            #print("y")
            start=0
            for iter in item.split(' '):
                for i in range(len(sentence_list)):
                    #print(sentence_list[i])
                    if sentence_list[i].__contains__(iter):
                        if dict[item]=="unitcode":
                            num=False
                            for k in range(10):
                                if sentence_list[i].__contains__(str(k)):
                                    num=True
                            if num==True:

                                if start == 0:
                                    sentence_slot[i] = "B-" + dict[item]
                                    start = 1
                                else:
                                    sentence_slot[i] = "I-" + dict[item]
                        else:
                            if start==0:
                                sentence_slot[i]="B-"+ dict[item]
                                start = 1
                            else:
                                sentence_slot[i]="I-"+ dict[item]


    return sentence_list,sentence_slot

def test():
    test1 = "which level dose Graphics and Multimedia in"  # wrong
    test2 = "show me the course code of Introduction to Programming"  # wrong
    test3 = "Could I select COMP5799 in last year"  # ok
    test4 = "Can I choose Enterprise Healthcare Information Systems this year I am a Software Mid-Year student"  # ok
    test5 = "could you tell me the campus of COMP5425"  # ok

    test6 = "what's the assignemnt of introduction to programming"
    test7 = "the code of object oriented programming"
    test8 = "the description and lecturer of introduction to computer systems"

    test9 = "where is the location of object oriented programming"
    test10 = "what textbook dose computing 1a professionalism recommend"
    test11 = "when is the due time of quiz in introduction to computer systems"

    filename = entiry_dict_path
    dict = csv2dictionary(filename)
    #print(dict)

    sentence, slot = matching(test5, dict)
    print(sentence)
    print(slot)

test()
