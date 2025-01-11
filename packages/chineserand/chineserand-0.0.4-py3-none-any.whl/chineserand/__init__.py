# -*- coding: utf8 -*-


"""
通过中文语料库，生成随机中文
"""
import os.path
import random


def raw(size: int = 0):
    """
    生成随机中文，指定中文字数
    :param size:
    :return:
    """
    data_file = os.path.join(os.path.dirname(__file__), 'global_word.rst')
    with open(data_file, 'r', encoding='utf8') as f:
        chinese_words = f.readline()
    return_str = ''
    length = len(chinese_words)
    for i in range(size):
        idx = random.randint(0, length - 1)
        word = chinese_words[idx]
        return_str += word
    return return_str


def sentences(many: int = 1):
    """
    随机生成几句话
    :param size:
    :return:
    """
    data_file = os.path.join(os.path.dirname(__file__), 'sentences.rst')
    with open(data_file, 'r', encoding='gbk') as f:
        chinese_sentences = f.readlines()
        chinese_sentences = [sentence for sentence in chinese_sentences if not sentence.startswith("#")]
    return_sentences = ''
    for i in range(many):
        rand_idx = random.randint(0, len(chinese_sentences) - 1)
        return_sentences += chinese_sentences[rand_idx]
    return return_sentences


if __name__ == '__main__':
    # print(raw(10))
    print(sentences(3))
