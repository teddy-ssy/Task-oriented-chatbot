import tensorflow as tf


from NLU.model import Model
import numpy as np
from NLU.preprocessing import *
from NLU.fileutil import *
from NLU.string_matching import *
from NLU import constants
from NLU import NER_rawquestion

index_seq2slot = lambda s, index2slot: [index2slot[str(i)] for i in s]
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class NLU():

    def __init__(self):
        self.input_steps = constants.intent_size

        self.hidden_size = constants.hidden_size
        self.n_layers = constants.n_layers
        self.batch_size = 1
        self.vocab_size = constants.vocab_size
        self.slot_size = constants.slot_size
        self.intent_size = constants.intent_size
        self.epoch_num = constants.epoch_num

        def get_model(mode):
            model = Model(self.input_steps, self.hidden_size, self.vocab_size, self.slot_size,
                          self.intent_size, self.epoch_num, self.batch_size, self.n_layers, mode)
            model.build()
            return model

        # get model
        self.model = get_model("train")
        # get sess
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.sess.run(tf.local_variables_initializer())

        self.model.restore(self.sess)


        self.entity_dict= csv2dictionary(constants.entiry_dict_path)

    def predict(self,sentence):


        word2index=restore_dict(constants.index_path+"word2index")
        index2intent=restore_dict(constants.index_path+"index2intent")
        index2slot = restore_dict(constants.index_path+"index2slot")
        sin = []
        sentence= preprocessing(sentence)
        #seq_in = sentence
        seq_in = sentence.split(" ")

        temp = seq_in
        if len(temp) < self.input_steps:
            temp.append('<EOS>')
            while len(temp) < self.input_steps:
                temp.append('<PAD>')
        else:
            temp = temp[:self.input_steps]
            temp[-1] = '<EOS>'
        sin.append(temp)
        sin_ = list(map(lambda i: word2index[i] if i in word2index else word2index["<UNK>"],
                        sin[0]))
        true_length = sin[0].index("<EOS>")

        # predict
        #print([sin_])
        decoder_prediction, intent = self.model.step(self.sess, "test", zip([sin_], [true_length]))
        decoder_prediction = np.transpose(decoder_prediction, [1, 0])

        _, slot = matching(sentence, self.entity_dict)
        Ner = NER_rawquestion.NER()
        slot2 =Ner.predict(output_dir=constants.ner_model_path, sentence=(sentence))

        for i in range(len(slot)):
            if slot[i]=='O':
                #ner
                slot[i]=slot2[i]

        print("sentence          : " + str(sentence.split(" ")))
        print("intent from model : " + str(index2intent[str(intent[0])]))
        print("slot from model   : " + str(index_seq2slot(decoder_prediction[0], index2slot)[:true_length]))
        print("slot plus matching: " + str(slot))
        print("\n")


        return slot, index2intent[str(intent[0])],sentence.split(" ")


NLU = NLU()

print("start model")

print("start predict")
test1 = "i want to know the level of Graphic Multimedia in"  # wrong
test2 = "show me the course code of Introduction to Programming"  # wrong
test3 = "Could I select COMP5799 in last year"  # ok
test4 = "Can I choose Enterprise Healthcare Information Systems this year I am a Software Mid-Year student"  # ok
test5 = "could you tell me the campus of COMP5799"  # ok

test6 = "what's the assignemnt of introduction to programming"
test7 = "the code of object oriented programming"
test8 = "the description and lecturer of introduction to computer systems"

test9 = "where is the location of object oriented programming"
test10 = "what textbook dose computing 1a professionalism recommend"
test11 = "when is the due time of quiz in introduction to computer systems"

slots, intent, sentence = NLU.predict(test1)
slots, intent, sentence = NLU.predict(test2)
slots, intent, sentence = NLU.predict(test3)
slots, intent, sentence = NLU.predict(test4)
slots, intent, sentence = NLU.predict(test5)
slots, intent, sentence = NLU.predict(test6)
slots, intent, sentence = NLU.predict(test7)
slots, intent, sentence = NLU.predict(test8)
slots, intent, sentence = NLU.predict(test9)
slots, intent, sentence = NLU.predict(test10)
slots, intent, sentence = NLU.predict(test11)




