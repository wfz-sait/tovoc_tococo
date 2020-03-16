'''
本文件是定义xml的tree结构等函数
'''


from lxml import etree
import os
import xml.etree.ElementTree as ET
class GEN_Annotations:
    def __init__(self, filename):
        self.root = etree.Element("annotation")

        child1 = etree.SubElement(self.root, "folder")
        child1.text = "VOC2007"

        child2 = etree.SubElement(self.root, "filename")
        child2.text = str(filename)

        child3 = etree.SubElement(self.root, "source")
        child4 = etree.SubElement(child3, "database")
        child4.text = "The VOC2007 Database"
        child5 = etree.SubElement(child3, "annotation")
        child5.text = "PASCAL VOC2007"
        child6 = etree.SubElement(child3, "image")
        child6.text = "flickr"

    def set_size(self,w,h,channel):
        size = etree.SubElement(self.root, "size")
        width = etree.SubElement(size, "width")
        width.text = str(w)
        height = etree.SubElement(size, "height")
        height.text = str(h)
        depth = etree.SubElement(size, "depth")
        depth.text = str(channel)
    # 把这个xml树写在指定位置
    # def set_back_fore_label(self,back_fore_label):
    #     label=etree.SubElement(self.root,"label")
    #     label.text=back_fore_label
    def savefile(self,filename):
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')

    def set_segmented(self,value):
        segmented=etree.SubElement(self.root,"segmented")
        segmented.text=str(value)

    # 标记grouder truth 记录矩形区域的对角坐标
    def add_pic_attr(self,label,minx,miny,maxx,maxy):
        object = etree.SubElement(self.root, "object")
        name = etree.SubElement(object, "name")
        name.text = label
        pose=etree.SubElement(object,"pose")
        pose.text="Unspecified"
        truncated=etree.SubElement(object,"truncated")
        truncated.text="0"
        difficult=etree.SubElement(object,"difficult")
        difficult.text="0"
        bndbox = etree.SubElement(object, "bndbox")
        xmin = etree.SubElement(bndbox, "xmin")
        xmin.text = str(minx)
        ymin = etree.SubElement(bndbox, "ymin")
        ymin.text = str(miny)
        xmax = etree.SubElement(bndbox, "xmax")
        xmax.text = str(maxx)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(maxy)

