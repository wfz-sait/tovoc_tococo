# tovoc_tococo
本文件主要基于bbox的数值数据生成xml文件，获取到图片和对应的xml文件就可以制作自己的voc格式的数据集。当然，我们也有些时候需要将voc数据集转换成coco数据集格式，用于代码的训练。

1. make_xml_file.py 是读取csv格式的bbox标注数据，生成VOC格式的xml文件；
2. make_voc.py是得到images和xml之后制作VOC2007格式的数据集
	- 创建voc2007的文件夹，然后把所有xml文件放进VOC2007/Annotations中，所有image放进					            VOC2007/ImageSets
	- 按照比例划分训练集、测试集，并生成相应的txt文件
3. voctococo.py是将voc格式的数据集转换成coco数据集的格式，首先需要将所有图片和xml文件放在同一个文件Annotations下，用于目标检测

4. 以下是几个备用程序：
	- CREATE_XML.py是定义xml的tree结构等函数;
	- modify_xml.py是重新resize图片之后重新生成对应的xml文件，平时用处不大；
	- xml_helper.py包括两个操作，可以学习一下：
		- 从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]；
		- 将bounding box信息写入xml文件中, bouding box格式为[[x_min, y_min, x_max, y_max, name]]；
