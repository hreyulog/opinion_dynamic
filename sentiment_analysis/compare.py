import keras
from snownlp import SnowNLP
from keras.preprocessing.sequence import pad_sequences
from gensim.models import KeyedVectors
import re
import jieba
import numpy as np
from matplotlib import pyplot as plt

cn_model = KeyedVectors.load_word2vec_format('sgns.weibo.bigram',
                                             binary=False)
model = keras.models.load_model("sentiment")


def predict_sentiment(text, cn_model, model):
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）:]+", "", text)
    # 分词
    cut = jieba.cut(text)
    cut_list = [i for i in cut]
    for i, word in enumerate(cut_list):
        try:
            cut_list[i] = cn_model.key_to_index[word]
        except KeyError:
            cut_list[i] = 0
    # padding
    tokens_pad = pad_sequences([cut_list], maxlen=107,
                               padding='pre', truncating='pre')
    # 预测
    result = model.predict(x=tokens_pad, verbose=0)
    return result[0][0]


def tptnfpfn(predict_score, fact, threshold):
    if fact == '0':
        if predict_score < threshold:
            return 'TN'
        else:
            return 'FP'
    elif fact == '1':
        if predict_score < threshold:
            return 'FN'
        else:
            return 'TP'


def TPR(dict_type):
    return dict_type['TP'] / (dict_type['TP'] + dict_type['FN'])


def FPR(dict_type):
    return dict_type['FP'] / (dict_type['TN'] + dict_type['FP'])


def accurancy(dict_type):
    return (dict_type['TP'] + dict_type['TN']) / (dict_type['TP'] + dict_type['FP'] + dict_type['TN'] + dict_type['FN'])


def compute(pos_list, neg_list, threshold):
    dict_type = {'TN': 0, 'FP': 0, 'FN': 0, 'TP': 0}
    for st in pos_list:
        dict_type[tptnfpfn(st, '1', threshold)] += 1
    for st in neg_list:
        dict_type[tptnfpfn(st, '0', threshold)] += 1
    return dict_type


def cont(type_method):
    pos_list = []
    neg_list = []
    with open('pos_test.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            if type_method == 'snow':
                pos_list.append(SnowNLP(row).sentiments)
                # dict_type[tptnfpfn(SnowNLP(row).sentiments, '1', threshold)] += 1
            elif type_method == 'bilstm':
                pos_list.append(predict_sentiment(row, cn_model, model))
                # dict_type[tptnfpfn(predict_sentiment(row, cn_model, model), '1', threshold)] += 1
    with open('neg_test.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            if type_method == 'snow':
                neg_list.append(SnowNLP(row).sentiments)
                # dict_type[tptnfpfn(SnowNLP(row).sentiments, '0', threshold)] += 1
            elif type_method == 'bilstm':
                neg_list.append(predict_sentiment(row, cn_model, model))
                # dict_type[tptnfpfn(predict_sentiment(row, cn_model, model), '0', threshold)] += 1
    return pos_list, neg_list


if __name__ == "__main__":
    x_snow = []
    y_snow = []
    x_bilstm = []
    y_bilstm = []
    thresholds = np.arange(0, 1, 0.1)
    snow_pos, snow_neg = cont('snow')
    bilstm_pos, bilstm_neg = cont('bilstm')
    all_list_snow=snow_pos+snow_neg
    all_list_bilstm=bilstm_pos+bilstm_neg
    plt.hist(x=all_list_snow, bins=20)
    plt.show()
    plt.hist(x=all_list_bilstm, bins=20)
    plt.show()

    for threshold in thresholds:
        dict_type_snow = compute(snow_pos, snow_neg, threshold)
        dict_type_bilstm = compute(bilstm_pos, bilstm_neg, threshold)
        y_snow.append(TPR(dict_type_snow))
        x_snow.append(FPR(dict_type_snow))
        x_bilstm.append(FPR(dict_type_bilstm))
        y_bilstm.append(TPR(dict_type_bilstm))
    print(np.array(x_snow), np.array(y_snow), np.array(x_bilstm), np.array(y_bilstm))
    fig, ax = plt.subplots()
    ax.set_xlabel('false positive rate')
    ax.set_ylabel('true positive rate')
    ax.plot(np.array(x_snow), np.array(y_snow), label='naive bayes')
    ax.plot(np.array(x_bilstm), np.array(y_bilstm), label='BiLSTM')
    ax.legend()
    plt.show()

# model = keras.models.load_model("sentiment")
# result = model.evaluate(X_test, y_test)
# print('Accuracy:{0:.2%}'.format(result[1]))
