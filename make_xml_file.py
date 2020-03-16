'''
本文件是读取csv格式的标注数据，生成VOC格式的xml
'''

# -*- coding: utf-8 -*-
import os
import csv
import numpy as np
import cv2
from CREATE_XML import GEN_Annotations
import xml.etree.ElementTree as ET
if __name__=='__main__':
    csv_filename = open('E:/data.csv', 'rt')          #csv文件的存储位置
    reader = csv.reader(csv_filename)                                   #csv.reader()返回一个reader对象，利用该对象遍历csv文件中的行
    headers = next(reader)                                              #标题行
    row = next(reader)                                                  #数据首行
    i=1
    img_name='1.jpg'
    while(i<=5000):                                     #循环的次数，要超过bbox的个数
        ##处理该行的数据##
        images__file_name=row[0]
        images__height, images__width, annotations__category_id = \
            (int(row[1]), int(row[2]), row[3])
        centre_x, centre_y, width, hight = (int(row[4]), int(row[5]), int(row[6]), int(row[7]))
        # point_xmin,point_ymin,point_xmax,point_ymax=(int(np.round(centre_x-width/2)),int(np.round(centre_y-hight/2)),
        #                                              int(np.round(centre_x+width/2)),int(np.round(centre_y+hight/2)))
        point_xmin, point_ymin, point_xmax, point_ymax = (
            int(np.round(centre_x)), int(np.round(centre_y)),
            int(np.round(centre_x + width)), int(np.round(centre_y + hight)))   #xml的bbox需要xmin、ymin、xmax、ymax
        ####因为一张image有多个bbox,靠images_id联系，因此image数量少于bbox数量，所以需要判断是否是下一张image
        if img_name!=images__file_name:                       #下一张图片，生成新的xml
            img_name=images__file_name
            image = cv2.imread(os.path.join("E:/images",       #对应图片存放的位置
                                            img_name))
            anno = GEN_Annotations(images__file_name)                           #生成xml tree
            anno.set_size(w=images__width, h=images__height, channel=3)
            anno.set_segmented(value=1)
            # anno.set_back_fore_label(back_fore_label='foreground')
            anno.add_pic_attr(label=annotations__category_id, minx=point_xmin, miny=point_ymin,
                              maxx=point_xmax, maxy=point_ymax)
            filename_xml = os.path.join("E:/XML", os.path.splitext(images__file_name)[0] + '.xml')     #生成xml存放的位置
            anno.savefile(filename_xml)

        else:              #同一张image的bbox,在原来xml的基础上继续
            cur_xml = ET.parse( os.path.join("E:/XML", os.path.splitext(images__file_name)[0] + '.xml'))       #读取xml
            root = cur_xml.getroot()
            object = ET.SubElement(root, "object")
            name = ET.SubElement(object,'name')
            name.text = annotations__category_id
            pose = ET.SubElement(object,"pose")
            pose.text = "Unspecified"
            truncated = ET.SubElement( object,"truncated")
            truncated.text = "0"
            difficult = ET.SubElement(object, "difficult")
            difficult.text = "0"
            bndbox = ET.SubElement(object, "bndbox")
            xmin = ET.SubElement(bndbox, "xmin")
            xmin.text = str(point_xmin)
            ymin = ET.SubElement(bndbox, "ymin")
            ymin.text = str(point_ymin)
            xmax = ET.SubElement(bndbox, "xmax")
            xmax.text = str(point_xmax)
            ymaxn = ET.SubElement(bndbox, "ymax")
            ymaxn.text = str(point_ymax)
            cur_xml.write( os.path.join("E:/XML", os.path.splitext(images__file_name)[0] + '.xml'))

        # print(images__file_name)
        # print("xmi:%d ymi: %d xma: %d ymax: %d  "%( point_xmin, point_ymin, point_xmax, point_ymax))
        #
        # #####将bbox的gt画出来，看看gt效果
        # cv2.rectangle(image,(point_xmin,point_ymin),(point_xmax,point_ymax),(0,0,255),1)
        # cv2.putText(image,annotations__category_id,(point_xmin,point_ymin-6),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8,(0,0,0))
        # cv2.imwrite(os.path.join("J:/Xray/pascal_voc/check_image",images__file_name),image)
        #
        # cv2.imshow('1',image)
        # cv2.waitKey(0)

        row=next(reader)
        i=i+1
        print(i)
