#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

ROOTDIR = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path = [os.path.join(ROOTDIR, "lib")] + sys.path

# Set your own model path
#MODELDIR = os.path.join(ROOTDIR, "./ltp_data")
MODELDIR = os.path.join(ROOTDIR, "/data/ftp/models/ltp/ltp_data_v3.4.0/")

from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

if __name__ == '__main__':
    paragraph = """
机器人提问:！！您好，我是大塘街社区卫生服务中心的智能助手，;请问您是李朝生本人或他家属吗
居民回复:
机器人提问:我这边没有听到，;我是大塘街社区卫生服务中心的智能助手,；请问您是不是 李朝生本人或他家属呢
居民回复:那什么。
机器人提问:我是大塘街社区卫生服务中心的智能助手,；请问您是不是 李朝生本人或他家属呢
居民回复:我参加什么这个活动？
机器人提问:我中心现举办一年一度的国家免费老年人健康体检，65岁及以上老年人都可参加，（仅限2023年未参加过体检的人群）。现诚邀您参加体检，时间是：逢周二至周五（节假日除外），上午：8:00-10:00，体检地址是：德政中路拾桂坊16号，，请问您愿意参加吗
居民回复:对，那。
机器人提问:请按时过来体检。时间是：逢周二至周五，上午：8:00-10:00，地址是：德政中路拾桂坊16号大塘街社区卫生服务中心，体检当天早上需空腹，携带本人有效身份证，高血压、糖尿病患者请带上现用药的药盒，感谢您的接听，再见！
居民回复:
    """

    # --------------------- 断句 ------------------------
    sentence = SentenceSplitter.split(paragraph)[0]

    # -------------------- Context Manager -------------
    with Segmentor(os.path.join(MODELDIR, "cws.model")) as s:
        words = s.segment(sentence)
        print("\t".join(words))

    # --------------------- 分词 ------------------------
    segmentor = Segmentor(os.path.join(MODELDIR, "cws.model"))

    # segmentor_with_vocab = Segmentor(
    #     os.path.join(MODELDIR, "cws.model"),
    #     lexicon_path='lexicon.txt',  # 分开的会合并在一起
    # )
    #
    # segmentor_with_force_vocab = Segmentor(
    #     os.path.join(MODELDIR, "cws.model"),
    #     force_lexicon_path='lexicon.txt'  # 除上述功能外，原本合并在一起的亦会拆分
    # )

    # --------------------- 词性标注 ------------------------
    postagger = Postagger(os.path.join(MODELDIR, "pos.model"))
    # # --------------------- 命名实体识别 ------------------------
    # recognizer = NamedEntityRecognizer(os.path.join(MODELDIR, "ner.model"))
    # # --------------------- 语义依存分析 ------------------------
    # parser = Parser(os.path.join(MODELDIR, "parser.model"))
    # # --------------------- 语义角色标注 ------------------------
    # labeller = SementicRoleLabeller(os.path.join(MODELDIR, "pisrl.model"))

    result = []
    for sentence in SentenceSplitter.split(paragraph):
        words = segmentor.segment(sentence)
        print("\t".join(words))

        # words_with_vocab = segmentor_with_vocab.segment(sentence)
        # print("\t".join(words_with_vocab), "\t\t| With Vocab")
        #
        # words_with_force_vocab = segmentor_with_force_vocab.segment(sentence)
        # print("\t".join(words_with_force_vocab), "\t| Force Vocab")

        postags = postagger.postag(words)
        # list-of-string parameter is support in 0.1.5
        # postags = postagger.postag(["中国","进出口","银行","与","中国银行","加强","合作"])
        print("\t".join(postags))

        # arcs = parser.parse(words, postags)
        #
        # print("\t".join("%d:%s" % (head, relation) for (head, relation) in arcs))

        # netags = recognizer.recognize(words, postags)
        # print("\t".join(netags))

        # roles = labeller.label(words, postags, arcs)
        #
        # for index, arguments in roles:
        #     print(index, " ".join(["%s: (%d,%d)" % (name, start, end) for (name, (start, end)) in arguments]))
        tag_cnt = len(postags)
        for i in range(tag_cnt):
            if postags[i] in ("nh", "nz", "ns"):
                result.append((words[i], postags[i]))

    print(result)

    segmentor.release()
    # segmentor_with_vocab.release()
    # segmentor_with_force_vocab.release()
    postagger.release()
    # parser.release()
    # recognizer.release()
    # labeller.release()