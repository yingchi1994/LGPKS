from collections import Counter
import collections
import jieba.analyse
import re
from pyecharts import *
import numpy as np
import jieba
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv


class Statistic():

    # 分词模板
    def cut_word(job_desc):
        string = job_desc
        print(type(string))
        # 对文件中的非法字符进行过滤
        data = re.sub(r"[\s+\.\!\/_,$%^*(【】：\]\[\-:;+\"\']+|[+——！，。？、~@#￥%……&*（）]+|[0-9]+", "", string)
        word_list = jieba.cut(data)
        print(word_list)
        return word_list


    # 词频统计模块
    def statistic_word(word_list):
        result = dict(Counter(word_list))
        sortlist = sorted(result.items(), key=lambda item: item[1], reverse=True)
        return sortlist

    def show_cloud(self):
        # 读取文件
        fn = open('job.txt')  # 打开文件
        string_data = fn.read()  # 读出整个文件
        fn.close()  # 关闭文件

        # 文本预处理
        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
        string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除

        # 文本分词
        seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
        object_list = []

        # # 去除模式
        # remove_words = [u'；', u'：', u'\xa0', u'有', u'数据', u'开发', u'经验', u'大',
        #                 u'熟悉', u'/', u'。', u' ', u'、', u'技术', u'能力', u'了',u'的',
        #                 u'和',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0',
        #                 u'等',u'相关',u'学习',u'或',u'了',u'进行',u'者',u'要求',u'描述',
        #                 u'任职',u'以上',u'项目',u'应用',u'业务',u'平台',u'沟通',u'对',u'产品',
        #                 u'设计',u'年',u'优先',u'，',u'’',u'‘',u'及',u'负责',u'工作',u'职位',
        #                 u'具备',u'具有',u'系统',u'良好',u'团队',u'以上学历',u'使用',u'精通',u'公司',
        #                 u'通常', u'如果', u'我们', u'需要']  # 自定义去除词库
        #
        # for word in seg_list_exact:  # 循环读出每个分词
        #     if word not in remove_words:  # 如果不在去除词库中
        #         object_list.append(word)  # 分词追加到列表

        filter_words = [u'Hadoop', u'Spark', u'Hive', u'Flink', u'Hbase', u'hdfs', u'Python']  # 自定义需要统计的关键词
        # 保留模式
        for word in seg_list_exact:  # 循环读出每个分词
            if word in filter_words:  # 如果不在去除词库中
                object_list.append(word)  # 分词追加到列表

        # 词频统计
        word_counts = collections.Counter(object_list)  # 对分词做词频统计
        word_counts_top10 = word_counts.most_common(30)  # 获取前10最高频的词
        print(word_counts_top10)  # 输出检查

        # 词频展示
        mask = np.array(Image.open('./wordcloud_bg.jpg'))  # 定义词频背景

        wc = wordcloud.WordCloud(
            font_path="./SourceHanSerifSC-Bold.otf",  # 设置字体格式
            mask=mask,  # 设置背景图
            max_words=30,  # 最多显示词数
            max_font_size=400  # 字体最大值
        )

        wc.generate_from_frequencies(word_counts)  # 从字典生成词云
        image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
        wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案

        plt.imshow(wc)  # 显示词云
        plt.axis('off')  # 关闭坐标轴
        plt.show()  # 显示图像
        plt.imsave("./out.jpg", wc)


    def run(self):

        # 读取文件
        fn = open('job.txt')  # 打开文件
        string_data = fn.read()  # 读出整个文件
        fn.close()  # 关闭文件

        # 文本预处理
        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
        string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除

        # 文本分词
        seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
        object_list = []

        # 去除模式
        remove_words = [u'；', u'：', u'\xa0', u'有', u'数据', u'开发', u'经验', u'大',
                        u'熟悉', u'/', u'。', u' ', u'、', u'技术', u'能力', u'了',u'的',
                        u'和',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0',
                        u'等',u'相关',u'学习',u'或',u'了',u'进行',u'者',u'要求',u'描述',
                        u'任职',u'以上',u'项目',u'应用',u'业务',u'平台',u'沟通',u'对',u'产品',
                        u'设计',u'年',u'优先',u'，',u'’',u'‘',u'及',u'负责',u'工作',u'职位',
                        u'具备',u'具有',u'系统',u'良好',u'团队',u'以上学历',u'使用',u'精通',u'公司',
                        u'通常', u'如果', u'我们', u'需要', u'（', u'）', u',', u'与', u'并', u'中',
                        u'在',u'理解',u'专业']  # 自定义去除词库

        for word in seg_list_exact:  # 循环读出每个分词
            if word not in remove_words:  # 如果不在去除词库中
                object_list.append(word)  # 分词追加到列表

        # filter_words = [u'Hadoop', u'Spark', u'Hive', u'Flink', u'Hbase', u'hdfs', u'Python', u'Shell'
        #     , u'Kafka', u'ElasticSearch', u'Java', u'Scala', u'数据仓库', u'机器学习', u'深度学习', u'TensorFlow'
        #     , u'数据挖掘', u'SQL', u'ETL', u'Storm',u'zookeeper',u'Spring']  # 自定义需要统计的关键词
        # # 保留模式
        # for word in seg_list_exact:  # 循环读出每个分词
        #     if word in filter_words:  # 如果不在去除词库中
        #         object_list.append(word)  # 分词追加到列表

        # 正则过滤英文词汇
        # for word in seg_list_exact:  # 循环读出每个分词
        #     en_word = re.sub(u"([^\u0041-\u005a\u0061-\u007a])", '', word)
        #     if en_word != '':
        #         cap_en_word = en_word.capitalize()
        #         object_list.append(cap_en_word)


        # 词频统计 Counter:
        word_counts_list = collections.Counter(object_list)
        # 词组重复统计剔除 - Spark Straming

        # 写入 CSV
        out = open('./result.csv', 'a', newline='')
        csv_write = csv.writer(out, dialect='excel')
        for wordi in word_counts_list:
            line = [wordi, word_counts_list[wordi]]
            # print(line)
            csv_write.writerow(line)

        word_counts_list["Spark"] -= word_counts_list["Streaming"]
        # 获取前10最高频的词
        word_counts_top30_list = word_counts_list.most_common(30)
        key = []
        values = []
        for i in range(len(word_counts_top30_list)):
            key.append(word_counts_top30_list[i][0])
            values.append(word_counts_top30_list[i][1])
        bar2 = Bar('拉勾网职位信息统计', '频数', page_title='薪资分布', background_color='white')
        # 图表其他主题：vintage,macarons,infographic,shine，roma

        # bar2.use_theme('vintage')
        configure(output_image=True)
        bar2.add('关键词', key, values, is_label_show=True, xaxis_rotate=70)

        bar2.render(path="./lagou.jpeg")
        bar2.render()

        img = mpimg.imread('./lagou.jpeg')
        plt.imshow(img)
        plt.show()

        print(key)
        print(values)


def main():
    # show_cloud()
    static = Statistic()
    static.run()


if __name__ == '__main__':
    main()
