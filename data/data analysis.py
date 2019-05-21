
import random
import numpy as np


flatten = lambda l: [item for sublist in l for item in sublist]  # 二维展成一维
index_seq2slot = lambda s, index2slot: [index2slot[i] for i in s]
index_seq2word = lambda s, index2word: [index2word[i] for i in s]


def data_pipeline(data, length=50):
    data = [t[:-1] for t in data]
    data = [[t.split("\t")[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]] for t in
            data]
    data = [[t[0][1:-1], t[1][1:], t[2]] for t in data]  #
    seq_in, seq_out, intent = list(zip(*data))
    sin = []
    sout = []
    #
    for i in range(len(seq_in)):
        temp = seq_in[i]
        if len(temp) < length:
            temp.append('<EOS>')
            while len(temp) < length:
                temp.append('<PAD>')
        else:
            temp = temp[:length]
            temp[-1] = '<EOS>'
        sin.append(temp)

        temp = seq_out[i]
        if len(temp) < length:
            while len(temp) < length:
                temp.append('<PAD>')
        else:
            temp = temp[:length]
            temp[-1] = '<EOS>'
        sout.append(temp)
        data = list(zip(sin, sout, intent))
    return data




if __name__ == '__main__':
    # train(is_debug=True)
    # test_data()
    train_data = open("/Users/sunshengyuan/PycharmProjects/capstone/week9/data/final_raw_question_V2.iob",
                      "r").readlines()
    #train_data = open("/Users/sunshengyuan/PycharmProjects/capstone/week1/data/atis-2.train.w-intent.iob","r").readlines()
    train_data_ed = data_pipeline(train_data)

    intent_list = []
    for k in range(len(train_data_ed)):
        if train_data_ed[k][2] not in intent_list:
            intent_list.append(train_data_ed[k][2])
            #print(train_data_ed[k][2])
            slots_list=[]
            question_list=[]
            for i in range(len(train_data_ed)):
                slots = train_data_ed[i][1]
                if train_data_ed[i][2] == train_data_ed[k][2]:
                    temp = []
                    for item in slots:
                        if item not in slots_list and not item.__contains__("I-") and not item.__contains__("<PAD>") and not item.__contains__("O"):
                            slots_list.append(item)
                        if item not in temp and not item.__contains__("I-") and not item.__contains__("<PAD>") and not item.__contains__("O"):
                            temp .append(item)
                    temp.sort()
                    if temp not in question_list:

                        question_list.append(temp)
            print(train_data_ed[k][2])

            question_list.sort()
            print("\nquestion type for this intent")
            for item in question_list:
                print((item))
            print("\nnum of the question type for this intent =" + str(len(question_list)))

            print("\nslot type for this intent")
            print(slots_list)

            print("\nslot realation in this intent")
            for slot in slots_list :
                print(slot)
                list_relation =[]
                num=0
                for question in question_list:
                    if question.__contains__(slot):
                        num+=1
                        for item in question:
                            if not list_relation.__contains__(item):
                                list_relation.append(item)
                list_relation.sort()
                print(str(list_relation)+"  time :"+ str(num))

            print("\n")
            print("\n")



