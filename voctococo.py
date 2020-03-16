"""
本文件是将voc格式的数据集转换成coco数据集的格式，首先需要将所有图片和xml文件放在同一个文件Annotations下，用于目标检测
"""

#coding:utf-8
# pip install lxml
 
import os
import glob
import json
import shutil
import numpy as np
import xml.etree.ElementTree as ET

path = "to_coco/"
START_BOUNDING_BOX_ID = 1


def img_rename():                #根据自身需要，可以将图片和xml统一换成000001开始的文件名，例如000001.jpg,000002.jpg,
    dir1 = "to_coco/Annotations"
    dir2 = "to_coco/Annotations1/"
    xml_list = glob.glob(dir1 + "/*.xml")
    i = 1
    for xml in xml_list:
        print(i)

        img = xml[:-4] + ".jpg"
        shutil.copyfile(xml, dir2 + "{0:06d}".format(int(i)) + '.xml')
        shutil.copyfile(img, dir2 + "{0:06d}".format(int(i)) + '.jpg')
        i += 1

def get(root, name):
    return root.findall(name)


def get_and_check(root, name, length):                   #读取数据并检查xml是否为坏数据
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def convert(xml_list, json_file):                    #转换函数
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    categories = pre_define_categories.copy()
    bnd_id = START_BOUNDING_BOX_ID
    all_categories = {}
    for index, line in enumerate(xml_list):
        # print("Processing %s"%(line))
        xml_f = line
        tree = ET.parse(xml_f)
        root = tree.getroot()

        filename = os.path.basename(xml_f)[:-4] + ".jpg"
        #print(filename)
        image_id = 1 + index
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width, 'id':image_id}
        json_dict['images'].append(image)
        ## Cruuently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category in all_categories:
                all_categories[category] += 1
            else:
                all_categories[category] = 1
            if category not in categories:
                if only_care_pre_define_categories:
                    continue
                new_id = len(categories) + 1
                print("[warning] category '{}' not in 'pre_define_categories'({}), create new id: {} automatically".format(category, pre_define_categories, new_id))
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin1=float(get_and_check(bndbox, 'xmin', 1).text)
            xmin = round(xmin1,2)                                 #round返回两位小数，也可以用int全部返回整数型
            ymin1=float(get_and_check(bndbox, 'ymin', 1).text)
            ymin = round(ymin1,2)
            xmax1=float(get_and_check(bndbox, 'xmax', 1).text)
            xmax = round(xmax1,2)
            ymax1=float(get_and_check(bndbox, 'ymax', 1).text)
            ymax = round(ymax1,2)
            assert(xmax > xmin), "xmax <= xmin, {}".format(line)
            assert(ymax > ymin), "ymax <= ymin, {}".format(line)
            o_width1 = abs(xmax - xmin)
            o_width=round(o_width1,2)
            o_height1 = abs(ymax - ymin)
            o_height = round(o_height1,2)
            area = round(o_width*o_height,2)
            ann = {'area': area, 'iscrowd': 0, 'image_id':
                   image_id, 'bbox':[xmin, ymin, o_width, o_height],
                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                   'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
    print("------------create {} done--------------".format(json_file))
    print("find {} categories: {} -->>> your pre_define_categories {}: {}".format(len(all_categories), all_categories.keys(), len(pre_define_categories), pre_define_categories.keys()))
    print("category: id --> {}".format(categories))
    print(categories.keys())
    print(categories.values())


if __name__ == '__main__':
    classes = ['Gun','knife','Wrench','Pliers','Scissors']                 #修改类别
    pre_define_categories = {'Gun':1,'knife':2,'Wrench':3,'Pliers':4,'Scissors':5}      #对应的键值，也可不需要设置
    for i, cls in enumerate(classes):
        pre_define_categories[cls] = i + 1
    only_care_pre_define_categories = True
    # only_care_pre_define_categories = False

    if os.path.exists(path + "/annotations"):
        shutil.rmtree(path + "/annotations")
    os.makedirs(path + "/annotations")
    if os.path.exists(path + "/images/trainval2014"):
        shutil.rmtree(path + "/images/trainval2014")
    os.makedirs(path + "/images/trainval2014")
    if os.path.exists(path + "/images/testdev2017"):
        shutil.rmtree(path + "/images/testdev2017")
    os.makedirs(path + "/images/testdev2017")
    if os.path.exists(path + "/images/minival2014"):
        shutil.rmtree(path +"/images/minival2014")
    os.makedirs(path + "/images/minival2014")

    train_ratio = 0.8    #训练集占总体的比例
    trainval_ratio=0.9      #训练集+测试集的比例
    save_file = 'to_coco/'
    save_json_train = save_file+'annotations/instances_train2014.json'
    save_json_val = save_file+'annotations/instances_minival2014.json'
    save_json_test = save_file+'annotations/instances_testdev2017.json'
    xml_dir = "to_coco/Annotations"
    #img_dir = "C:/Users/jiang/Desktop/to_coco/images"

    xml_list = glob.glob(xml_dir + "/*.xml")
    xml_list = np.sort(xml_list)
    np.random.seed(100)
    np.random.shuffle(xml_list)

    len1=len(xml_list)
    train_num = int(len1 * train_ratio)
    trainval_num = int(len1*trainval_ratio)
    # xml_list_train = xml_list[:train_num]
    xml_list_trainval = xml_list[:trainval_num]
    xml_list_val = xml_list[train_num:trainval_num]
    xml_list_test = xml_list[trainval_num:]

    convert(xml_list_trainval, save_json_train)
    convert(xml_list_test, save_json_test)
    convert(xml_list_val, save_json_val)



    f1 = open("trainval.txt", "w")
    for xml in xml_list_trainval:
        img = xml[:-4] + ".jpg"
        f1.write(os.path.basename(xml)[:-4] + "\n")
        shutil.copyfile(img, path + "/images/trainval2014/" + os.path.basename(img))

    f2 = open("test.txt", "w")
    for xml in xml_list_test:
        img = xml[:-4] + ".jpg"
        f2.write(os.path.basename(xml)[:-4] + "\n")
        shutil.copyfile(img, path + "/images/testdev2017/" + os.path.basename(img))

    f3 = open("val.txt", "w")
    for xml in xml_list_val:
        img = xml[:-4] + ".jpg"
        f2.write(os.path.basename(xml)[:-4] + "\n")
        shutil.copyfile(img, path + "/images/minival2014/" + os.path.basename(img))

    f1.close()
    f2.close()
    f3.close()

    print("-------------------------------")
    print("trainval number:", len(xml_list_trainval))
    print("test number:", len(xml_list_test))
    print("val number:", len(xml_list_val))
