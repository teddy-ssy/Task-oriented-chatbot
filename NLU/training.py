import tensorflow as tf
from NLU.metrics import *
from NLU.model import Model
from tensorflow.python import debug as tf_debug
import numpy as np
from NLU.pipeline import *
from NLU.fileutil import *
from NLU import constants


input_steps =constants.intent_size
word_vector_length=constants.word_vector_length
embedding_size = constants.embedding_size
hidden_size = constants.hidden_size
n_layers = constants.n_layers
batch_size = constants.batch_size
#test_batch_size = 1
vocab_size = constants.vocab_size
slot_size = constants.slot_size
intent_size = constants.intent_size
epoch_num = constants.epoch_num

def get_model(mode):

    model = Model(input_steps, hidden_size, vocab_size, slot_size,
                 intent_size, epoch_num, batch_size, n_layers,mode)
    model.build()
    return model

def train(is_debug=False):

    # print(tf.trainable_variables())trainSamples

    train_data = open(constants.taining_data_path, "r").readlines()
    test_data = open(constants.taining_data_path, "r").readlines()
    #test_data = open("/Users/sunshengyuan/PycharmProjects/capstone/NLU/data/trainSamples.iob","r").readlines()

    train_data_ed = data_pipeline(train_data)
    test_data_ed = data_pipeline(test_data)
    word2index, index2word, slot2index, index2slot, intent2index, index2intent, word2vector = get_info_from_training_data(
        train_data_ed)
    #_, _, _, _, _, _, testword2v = get_info_from_data(test_data_ed)
    train_index2vector = get_index2vector(word2index, word2vector)

    index_train = to_index(train_data_ed,  slot2index, intent2index,word2index)
    index_test = to_index(test_data_ed, slot2index, intent2index,word2index)

    #save index
    save_dict(constants.index_path+"word2index",word2index)
    save_dict(constants.index_path+"index2word",index2word)
    save_dict(constants.index_path+"slot2index",slot2index)
    save_dict(constants.index_path+"index2slot",index2slot)
    save_dict(constants.index_path+"intent2index",intent2index)
    save_dict(constants.index_path+"index2intent",index2intent)
    save_dict(constants.index_path+"train_index2vevtor",train_index2vector)

    #save word2indx

    model = get_model("train")

    sess = tf.Session()
    if is_debug:
        sess = tf_debug.LocalCLIDebugWrapperSession(sess)
        sess.add_tensor_filter("has_inf_or_nan", tf_debug.has_inf_or_nan)
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())

    for epoch in range(epoch_num):
        mean_loss = 0.0
        train_loss = 0.0

        #print(index_train[0])

        for i, batch in enumerate(getBatch(batch_size, index_train)):
            # 执行一个batch的训练
            _, loss, decoder_prediction, intent, mask, slot_W = model.step(sess, "train", batch)
        train_loss /= (i + 1)
        print("[Epoch {}] Average train loss: {}".format(epoch, train_loss))

        # 每训一个epoch，测试一次
        pred_slots = []
        slot_accs = []
        intent_accs = []

        for j, batch in enumerate(getBatch(batch_size, index_test)):

            decoder_prediction, intent = model.step(sess, "test", batch)
            decoder_prediction = np.transpose(decoder_prediction, [1, 0])
            if j == 0:
                index = random.choice(range(len(batch)))
                # index = 0
                sen_len = batch[index][1]

                print("Input Sentence        : ", index_seq2word(batch[index][0], index2word)[:sen_len])
                print("Slot Truth            : ", index_seq2slot(batch[index][2], index2slot)[:sen_len])
                print("Slot Prediction       : ", index_seq2slot(decoder_prediction[index], index2slot)[:sen_len])
                print("Intent Prediction     : ", index2intent[intent[index]])
            slot_pred_length = list(np.shape(decoder_prediction))[1]
            pred_padded = np.lib.pad(decoder_prediction, ((0, 0), (0, input_steps-slot_pred_length)),
                                     mode="constant", constant_values=0)
            pred_slots.append(pred_padded)
            # print("slot_pred_length: ", slot_pred_length)
            true_slot = np.array((list(zip(*batch))[2]))
            true_length = np.array((list(zip(*batch))[1]))
            true_slot = true_slot[:, :slot_pred_length]
            # print(np.shape(true_slot), np.shape(decoder_prediction))
            # print(true_slot, decoder_prediction)
            slot_acc = accuracy_score(true_slot, decoder_prediction, true_length)
            intent_acc = accuracy_score(list(zip(*batch))[3], intent)
            # print("slot accuracy: {}, intent accuracy: {}".format(slot_acc, intent_acc))
            slot_accs.append(slot_acc)
            intent_accs.append(intent_acc)
        #print(pred_slots)
        pred_slots_a = np.vstack(pred_slots)
        # print("pred_slots_a: ", pred_slots_a.shape)
        true_slots_a = np.array(list(zip(*index_test))[2])[:pred_slots_a.shape[0]]
        # print("true_slots_a: ", true_slots_a.shape)
        print("Intent accuracy for epoch {}: {}".format(epoch, np.average(intent_accs)))
        print("Slot accuracy for epoch {}: {}".format(epoch, np.average(slot_accs)))
        print("Slot F1 score for epoch {}: {}".format(epoch, f1_for_sequence_batch(true_slots_a, pred_slots_a)))
        #save_path = saver.save(sess, "/tmp/model.ckpt")
    model.save(sess)

#train()