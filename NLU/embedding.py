import numpy as np
from gensim.models import KeyedVectors
from NLU import constants

class Word_embedding_Model:

    def __init__(self):
        # Creating the model
        model_loc = constants.word2vector_path
        self.en_model = KeyedVectors.load_word2vec_format(model_loc)
        self.PAD = np.zeros(300).tolist()
        self.UNK = np.ones(300).tolist()
        self.SOS = np.zeros(300).tolist()
        for i in range(300):
            self.SOS[i] = 2

        self.EOS = np.zeros(300).tolist()
        for i in range(300):
            self.EOS[i] = 3

    def get_word_vector(self, word):
        try:
            result = self.en_model[word]
            # Print out the vector of a word
            # print("Vector components of a word: {}".format(self.en_model[word]))

            return result.tolist()
        except:
            # print("Vector components of a word: {}".format(self.UNK))
            return self.UNK