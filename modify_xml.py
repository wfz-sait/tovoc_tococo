'''
本文件是重新resize图片之后重新生成对应的xml文件
'''

import os
import cv2
import xml.cur_xml.ElementTree as ET

xml_base_readerpath="E:/VOCdevkit2007/VOC2007/Annotations"
xml_base_writerpath="E:/VOCdevkit2007/VOC2007/Annotations"
img_base_readerrpath="E:/VOCdevkit2007/VOC2007/JPEGImages"
img_base_writerpath="E:/VOCdevkit2007/VOC2007/JPEGImages"
img_check_writerpath="E:/pascal_VOC/trachea foreign/check_320_512"

def modify(img_reader_path,img_write_path,xml_reader_path,xml_writer_path,check_writer_img):
    img=cv2.imread(img_reader_path)
    hight,width,channel=img.shape
    print(img.shape)
    img_resize=cv2.resize(img,(512,320))          #统一size大小
    cv2.imwrite(img_write_path,img_resize)
    cur_xml=ET.parse(xml_reader_path)
    root=cur_xml.getroot()
    obj=root.find('object')
    bbox=obj.find('bndbox')
    xmin=bbox.find('xmin')
    cur_xmin=int(int(bbox.find('xmin').text)*512/width*1.0)
    ymin = bbox.find('ymin')
    cur_ymin = int(int(bbox.find('ymin').text)*320/hight*1.0)
    xmax = bbox.find('xmax')
    cur_xmax= int(int(bbox.find('xmax').text)*512/width*1.0)
    ymax = bbox.find('ymax')
    cur_ymax = int(int(bbox.find('ymax').text)*320/hight*1.0)
    if cur_ymin<1:
        cur_ymin=1
    xmin.text=str(cur_xmin)
    ymin.text = str(cur_ymin)
    xmax.text = str(cur_xmax)
    ymax.text = str(cur_ymax)
    cv2.rectangle(img_resize,(cur_xmin,cur_ymin),(cur_xmax,cur_ymax),(0,250,130),1)
    cv2.imwrite(check_writer_img,img_resize)
    size=root.find('size')
    width=size.find('width')
    height=size.find('height')
    width.text=str(512)
    height.text=str(320)
    cur_xml.write(xml_writer_path)


if __name__=='__main__':
    for i in range(1,19221):
        modify( os.path.join(img_base_readerrpath,"{0:06d}".format(i)+'.jpg'),
                os.path.join(img_base_writerpath, "{0:06d}".format(i) + '.jpg'),
                os.path.join(xml_base_readerpath,"{0:06d}".format(i)+'.xml'),
                os.path.join(xml_base_writerpath, "{0:06d}".format(i) + '.xml'),
                os.path.join(img_check_writerpath, "{0:06d}".format(i) + '.jpg'))