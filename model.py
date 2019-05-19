import tensorflow as tf
import numpy as np
from tensorflow.contrib.rnn import LSTMCell, LSTMStateTuple,DropoutWrapper
import sys
from week9.fileutil import *
from week9 import constants

class Model:
    def __init__(self, input_steps,  hidden_size, vocab_size, slot_size,
                 intent_size, epoch_num, batch_size=16, n_layers=1, model='train'):
        self.input_steps = input_steps
        #self.embedding = embedding
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        self.batch_size = batch_size
        self.vocab_size = vocab_size#useless
        self.slot_size = slot_size
        self.intent_size = intent_size
        self.epoch_num = epoch_num
        self.model = model

        if self.model == 'train':
            self.batch_size = batch_size
        else:
            self.batch_size = 1

        self.encoder_inputs = tf.placeholder(tf.int32, [input_steps, batch_size], name='encoder_inputs')

        # 每句输入的实际长度，除了padding
        self.encoder_inputs_actual_length = tf.placeholder(tf.int32, [batch_size],
                                                           name='encoder_inputs_actual_length')
        self.decoder_targets = tf.placeholder(tf.int32, [batch_size, input_steps],
                                              name='decoder_targets')
        self.intent_targets = tf.placeholder(tf.int32, [batch_size],
                                             name='intent_targets')


    def build(self):

        train_index2vector=restore_dict(constants.index_path+"train_index2vevtor")
        #restore the embedding

        embedding = []
        for i in sorted(train_index2vector.keys()):
            embedding.append(train_index2vector[i])

        self.embeddings = tf.Variable(embedding, dtype=tf.float32, name="embedding" )

        self.encoder_inputs_embedded = tf.nn.embedding_lookup(self.embeddings, self.encoder_inputs)

        # Encoder
        encoder_f_cell_0 = LSTMCell(self.hidden_size)
        encoder_b_cell_0 = LSTMCell(self.hidden_size)
        encoder_f_cell = DropoutWrapper(encoder_f_cell_0,output_keep_prob=0.5)
        encoder_b_cell = DropoutWrapper(encoder_b_cell_0,output_keep_prob=0.5)

        (encoder_fw_outputs, encoder_bw_outputs), (encoder_fw_final_state, encoder_bw_final_state) = \
            tf.nn.bidirectional_dynamic_rnn(cell_fw=encoder_f_cell,
                                            cell_bw=encoder_b_cell,
                                            inputs=self.encoder_inputs_embedded,
                                            sequence_length=self.encoder_inputs_actual_length,
                                            dtype=tf.float32, time_major=True)

        encoder_outputs = tf.concat((encoder_fw_outputs, encoder_bw_outputs), 2)

        encoder_final_state_c = tf.concat(
            (encoder_fw_final_state.c, encoder_bw_final_state.c), 1)

        encoder_final_state_h = tf.concat(
            (encoder_fw_final_state.h, encoder_bw_final_state.h), 1)

        self.encoder_final_state = LSTMStateTuple(
            c=encoder_final_state_c,
            h=encoder_final_state_h
        )
        print("encoder_outputs: ", encoder_outputs)
        print("encoder_outputs[0]: ", encoder_outputs[0])
        print("encoder_final_state_c: ", encoder_final_state_c)

        # Decoder
        decoder_lengths = self.encoder_inputs_actual_length
        self.slot_W = tf.Variable(tf.random_uniform([self.hidden_size * 2, self.slot_size], -1, 1),
                             dtype=tf.float32, name="slot_W")
        self.slot_b = tf.Variable(tf.zeros([self.slot_size]), dtype=tf.float32, name="slot_b")
        intent_W = tf.Variable(tf.random_uniform([self.hidden_size * 2, self.intent_size], -0.1, 0.1),
                               dtype=tf.float32, name="intent_W")
        intent_b = tf.Variable(tf.zeros([self.intent_size]), dtype=tf.float32, name="intent_b")

        # 求intent
        intent_logits = tf.add(tf.matmul(encoder_final_state_h, intent_W), intent_b)
        # intent_prob = tf.nn.softmax(intent_logits)
        self.intent = tf.argmax(intent_logits, axis=1)

        sos_time_slice = tf.ones([self.batch_size], dtype=tf.int32, name='SOS') * 2
        sos_step_embedded = tf.nn.embedding_lookup(self.embeddings, sos_time_slice)
        pad_step_embedded = tf.zeros([self.batch_size, self.hidden_size*2+300],
                                     dtype=tf.float32)

        def initial_fn():
            initial_elements_finished = (0 >= decoder_lengths)  # all False at the initial step
            initial_input = tf.concat((sos_step_embedded, encoder_outputs[0]), 1)
            return initial_elements_finished, initial_input

        def sample_fn(time, outputs, state):
            print("outputs", outputs)
            prediction_id = tf.to_int32(tf.argmax(outputs, axis=1))
            return prediction_id

        def next_inputs_fn(time, outputs, state, sample_ids):
            # 上一个时间节点上的输出类别，获取embedding再作为下一个时间节点的输入
            pred_embedding = tf.nn.embedding_lookup(self.embeddings, sample_ids)
            # 输入是h_i+o_{i-1}+c_i
            next_input = tf.concat((pred_embedding, encoder_outputs[time]), 1)
            elements_finished = (time >= decoder_lengths)  # this operation produces boolean tensor of [batch_size]
            all_finished = tf.reduce_all(elements_finished)  # -> boolean scalar
            next_inputs = tf.cond(all_finished, lambda: pad_step_embedded, lambda: next_input)
            next_state = state
            return elements_finished, next_inputs, next_state

        my_helper = tf.contrib.seq2seq.CustomHelper(initial_fn, sample_fn, next_inputs_fn)

        def decode(helper, scope, reuse=None):
            with tf.variable_scope(scope, reuse=reuse):
                #attention cell
                memory = tf.transpose(encoder_outputs, [1, 0, 2])

                # 定义要使用的attention机制。
                attention_mechanism = tf.contrib.seq2seq.BahdanauAttention(
                    num_units=self.hidden_size, memory=memory,
                    memory_sequence_length=self.encoder_inputs_actual_length)

                # 定义decoder阶段要是用的LSTMCell，然后为其封装attention wrapper
                cell = tf.contrib.rnn.LSTMCell(num_units=self.hidden_size * 2)
                attn_cell = tf.contrib.seq2seq.AttentionWrapper(
                    cell, attention_mechanism, attention_layer_size=self.hidden_size)
                #返回一个带有OutputProjectionLayer的cell(s)
                out_cell = tf.contrib.rnn.OutputProjectionWrapper(
                    attn_cell, self.slot_size, reuse=reuse)
                #basic decoder
                decoder = tf.contrib.seq2seq.BasicDecoder(
                    cell=out_cell, helper=helper,
                    initial_state=out_cell.zero_state(
                        dtype=tf.float32, batch_size=self.batch_size))
                # initial_state=encoder_final_state)

                #dynamic decoder
                final_outputs, final_state, final_sequence_lengths = tf.contrib.seq2seq.dynamic_decode(
                    decoder=decoder, output_time_major=True,
                    impute_finished=True, maximum_iterations=self.input_steps
                )
                return final_outputs

        outputs = decode(my_helper, 'decode')
        print("outputs: ", outputs)
        print("outputs.rnn_output: ", outputs.rnn_output)
        print("outputs.sample_id: ", outputs.sample_id)
        # weights = tf.to_float(tf.not_equal(outputs[:, :-1], 0))
        self.decoder_prediction = outputs.sample_id
        decoder_max_steps, decoder_batch_size, decoder_dim = tf.unstack(tf.shape(outputs.rnn_output))
        self.decoder_targets_time_majored = tf.transpose(self.decoder_targets, [1, 0])
        self.decoder_targets_true_length = self.decoder_targets_time_majored[:decoder_max_steps]
        print("decoder_targets_true_length: ", self.decoder_targets_true_length)
        # 定义mask，使padding不计入loss计算
        self.mask = tf.to_float(tf.not_equal(self.decoder_targets_true_length, 0))
        # 定义slot标注的损失
        loss_slot = tf.contrib.seq2seq.sequence_loss(
            outputs.rnn_output, self.decoder_targets_true_length, weights=self.mask)
        # 定义intent分类的损失
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
            labels=tf.one_hot(self.intent_targets, depth=self.intent_size, dtype=tf.float32),
            logits=intent_logits)
        loss_intent = tf.reduce_mean(cross_entropy)

        self.loss = loss_slot + loss_intent
        optimizer = tf.train.AdamOptimizer(name="a_optimizer")
        self.grads, self.vars = zip(*optimizer.compute_gradients(self.loss))
        print("vars for loss function: ", self.vars)
        self.gradients, _ = tf.clip_by_global_norm(self.grads, 5)  # clip gradients
        self.train_op = optimizer.apply_gradients(zip(self.gradients, self.vars))


    def step(self, sess, mode, batch):
        """ perform each batch"""
        if mode not in ['train', 'test', 'predict']:
            print >> sys.stderr, 'mode is not supported'
            sys.exit(1)
        unziped = list(zip(*batch))

        if mode == 'train':
            output_feeds = [self.train_op, self.loss, self.decoder_prediction,
                            self.intent, self.mask, self.slot_W]
            feed_dict = {self.encoder_inputs: np.transpose(unziped[0], [1, 0]),
                         self.encoder_inputs_actual_length: unziped[1],
                         self.decoder_targets: unziped[2],
                         self.intent_targets: unziped[3]}

        if mode in ['test']:
            output_feeds = [self.decoder_prediction, self.intent]
            feed_dict = {self.encoder_inputs: np.transpose(unziped[0], [1, 0]),
                         self.encoder_inputs_actual_length: unziped[1]}
        if mode == 'predict':
            output_feeds = [self.decoder_prediction, self.intent]
            feed_dict = {self.encoder_inputs: np.transpose(unziped[0], [1, 0]),
                         self.encoder_inputs_actual_length: unziped[1]}


        results = sess.run(output_feeds, feed_dict=feed_dict)
        return results

    def save(self,sess):
        saver = tf.train.Saver()
        #saver.save(sess, './params1/params1', write_meta_graph=False)
        saver.save(sess, constants.model_save_path, write_meta_graph=False)

    def restore(self,sess):
        saver = tf.train.Saver()
        #saver.restore(sess, './params1/params1')
        saver.restore(sess, constants.model_save_path)
        return sess
