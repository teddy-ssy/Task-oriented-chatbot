from NLU.embedding import Word_embedding_Model
import random
from NLU import constants

flatten = lambda l: [item for sublist in l for item in sublist]  # 二维展成一维
index_seq2slot = lambda s, index2slot: [index2slot[i] for i in s]
index_seq2word = lambda s, index2word: [index2word[i] for i in s]
vector_seq2word = lambda s, vector2word: [vector2word[i] for i in s]

def data_pipeline(data, length=50):
    data = [t[:-1] for t in data]
    data = [[t.split("\t")[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]] for t in data]

    data = [[t[0][1:-1], t[1][1:], t[2]] for t in data]  # 将BOS和EOS去掉，并去掉对应标注序列中相应的标注


    seq_in, seq_out, intent = list(zip(*data))
    sin = []
    sout = []
    # padding，原始序列和标注序列结尾+<EOS>+n×<PAD>
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

def get_word2index(vocab):
    word2index = {'<PAD>': 0, '<UNK>': 1, '<SOS>': 2, '<EOS>': 3}
    for token in vocab:
        if token not in word2index.keys():
            word2index[token] = len(word2index)
    return word2index

def get_word2embedding(vocab):
    word_model = Word_embedding_Model()
    word2vector = {'<PAD>': word_model.PAD, '<UNK>': word_model.UNK, '<SOS>': word_model.SOS, '<EOS>': word_model.EOS}
    for token in vocab:
        word2vector[token] = word_model.get_word_vector(token)
    return word2vector

def get_slot2index(slot_tag):
    tag2index = {'<PAD>': 0, '<UNK>': 1, "O": 2}
    for tag in slot_tag:
        if tag not in tag2index.keys():
            tag2index[tag] = len(tag2index)
    return tag2index

def get_intent2index(intent_tag):
    intent2index = {'<UNK>': 0}
    for ii in intent_tag:
        if ii not in intent2index.keys():
            intent2index[ii] = len(intent2index)
    return intent2index

def get_info_from_training_data(data):
    seq_in, seq_out, intent = list(zip(*data))
    vocab = set(flatten(seq_in))
    slot_tag = set(flatten(seq_out))
    intent_tag = set(intent)

    # 生成word2index
    word2index = get_word2index(vocab)
    # 生成index2word
    index2word = {v: k for k, v in word2index.items()}

    # 生成word2vector
    word2vector= get_word2embedding(vocab)

    # 生成tag2index
    tag2index = get_slot2index(slot_tag)
    # 生成index2tag
    index2tag = {v: k for k, v in tag2index.items()}

    # 生成intent2index
    intent2index = get_intent2index(intent_tag)
    # 生成index2intent
    index2intent = {v: k for k, v in intent2index.items()}

    return word2index, index2word, tag2index, index2tag, intent2index, index2intent, word2vector

def to_index(train, slot2index, intent2index,word2index):
    new_train = []
    for sin, sout, intent in train:
        #vin_ix = list(map(lambda i: vector2index[i] if i in vector2index else vector2index["<UNK>"],
                          #sin))
        #print(sin_ix)
        sin_ix = list(map(lambda i: word2index[i] if i in word2index else word2index["<UNK>"],
                          sin))
        #vin_ix = sum(vin_ix, [])
        #sin_xi = sin_xi.flatting()
        true_length = sin.index("<EOS>")
        sout_ix = list(map(lambda i: slot2index[i] if i in slot2index else slot2index["<UNK>"],
                           sout))
        intent_ix = intent2index[intent] if intent in intent2index else intent2index["<UNK>"]

        new_train.append([sin_ix, true_length, sout_ix, intent_ix, ])
    return new_train

def get_index2vector(word2index, word2vector):
    index2vector={}
    for w, i in word2index.items():
        index2vector[i] = word2vector[w]
    return index2vector


def pipeline(file):
    data = open(file, "r").readlines()
    data_ed = data_pipeline(data)
    word2index, index2word, slot2index, index2slot, intent2index, index2intent, word2vector = get_info_from_training_data(data_ed)
    index_data = to_index(data_ed, word2vector, slot2index, intent2index, word2index)

    index2vector = get_index2vector(word2index,word2vector)

    return word2index, index2word, slot2index, index2slot, intent2index, index2intent, word2vector, index_data, index2vector


def getBatch(batch_size, index_data):
    random.shuffle(index_data)
    sindex = 0
    eindex = batch_size
    while eindex < len(index_data):
        batch = index_data[sindex:eindex]
        temp = eindex
        eindex = eindex + batch_size
        sindex = temp
        yield batch

def get_info_from_data(data):
    seq_in, seq_out, intent = list(zip(*data))
    vocab = set(flatten(seq_in))
    slot_tag = set(flatten(seq_out))
    intent_tag = set(intent)

    # 生成word2index
    word2index = get_word2index(vocab)
    # 生成index2word
    index2word = {v: k for k, v in word2index.items()}

    # 生成tag2index
    tag2index = get_slot2index(slot_tag)
    # 生成index2tag
    index2tag = {v: k for k, v in tag2index.items()}

    # 生成intent2index
    intent2index = get_intent2index(intent_tag)
    # 生成index2intent
    index2intent = {v: k for k, v in intent2index.items()}

    return word2index, index2word, tag2index, index2tag, intent2index, index2intent

def test():
    train_data = open(constants.taining_data_path,"r").readlines()
    # train_data = open("/Users/sunshengyuan/PycharmProjects/capstone/NLU/data/trainSamples.iob", "r").readlines()
    train_data_ed = data_pipeline(train_data)
    word2index, index2word, slot2index, index2slot, intent2index, index2intent = get_info_from_data(train_data_ed)
    print(word2index)
    print(slot2index)
    print(intent2index)
    print(len(word2index))
    print(len(slot2index))
    print(len(intent2index))

#test()