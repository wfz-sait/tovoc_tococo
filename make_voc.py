'''
本文件是得到images和xml之后制作VOC2007数据集
分两步走：01、创建voc2007的文件夹，然后把所有xml文件放进VOC2007/Annotations中，所有image放进VOC2007/ImageSets
         02、按照比例划分训练集、测试集，并生成相应的txt文件
'''

import os
import random

##############第一步#####################
# make voc_dir
def make_voc_dir():
    os.makedirs('VOC2007/Annotations')
    os.makedirs('VOC2007/ImageSets')
    os.makedirs('VOC2007/ImageSets/Main')
    os.makedirs('VOC2007/ImageSets/Layout')
    os.makedirs('VOC2007/ImageSets/Segmentation')
    os.makedirs('VOC2007/JPEGImages')
    os.makedirs('VOC2007/SegmentationClass')
    os.makedirs('VOC2007/SegmentationObject')
##############第一步#####################

##############复制xml和image到相应文件夹#####################


##############第二步#####################
# make Main_txt
def make_voc_txt():
    trainval_percent = 0.7
    train_percent = 0.8
    xmlfilepath = 'VOC2007/Annotations'
    txtsavepath = 'VOC2007/ImageSets/Main'
    total_xml = os.listdir(xmlfilepath)                       #计算总的xml的个数
    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)                      #训练+验证集数量
    tr = int(tv * train_percent)                          #训练集数量

    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftrainval = open(txtsavepath + '/trainval.txt', 'w')
    ftest = open(txtsavepath + '/test.txt', 'w')
    ftrain = open(txtsavepath + '/train.txt', 'w')
    fval = open(txtsavepath + '/val.txt', 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()
##############第二步#####################


if __name__ == '__main__':
    make_voc_dir()
    make_voc_txt()