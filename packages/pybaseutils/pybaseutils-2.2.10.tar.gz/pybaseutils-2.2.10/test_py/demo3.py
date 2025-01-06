# -*-coding: utf-8 -*-
"""
    @Author : panjq
    @E-mail : pan_jinquan@163.com
    @Date   : 2022-08-30 09:45:44
    @Brief  :
"""

import os
import numpy as np
import cv2
from tqdm import tqdm
from pybaseutils import image_utils, file_utils
from pybaseutils.converter import build_voc


def save_voc_dataset(bboxes, labels, image_file, image_shape, out_xml_dir):
    """
    保存VOC数据集
    :param bboxes:
    :param labels:
    :param image_file:
    :param image_shape:
    :param out_xml_dir:
    :return:
    """
    basename = os.path.basename(image_file)
    image_id = basename.split(".")[0]
    objects = []
    for box, name in zip(bboxes, labels):
        objects.append({"name": name, "bndbox": box})
    xml_path = file_utils.create_dir(out_xml_dir, None, "{}.xml".format(image_id))
    build_voc.write_voc_xml_objects(basename, image_shape, objects, xml_path)


def save_crop_dataset(image, bboxes, labels, image_file, crop_root):
    """
    裁剪检测区域
    :param image:
    :param bboxes:
    :param labels:
    :param image_file:
    :param crop_root:
    :return:
    """
    basename = os.path.basename(image_file)
    image_id = basename.split(".")[0]
    crops = image_utils.get_bboxes_image(image, bboxes, size=None)
    for i, (img, label) in enumerate(zip(crops, labels)):
        file = file_utils.create_dir(crop_root, label, "{}_{:0=3d}.jpg".format(image_id, i))
        cv2.imwrite(file, img)


def convert_HaGRID_dataset(data_root, vis=True):
    """
    将HaGRID转换为VOC和分类数据集
    :param data_root: HaGRID数据集个根目录
    :param vis: 是否可视化效果
    :return:
    """
    sub_list = file_utils.get_sub_paths(data_root)
    class_names = []
    for sub in sub_list:
        anno_file = os.path.join(data_root, sub, "{}.json".format(sub))
        annotation = file_utils.read_json_data(anno_file)
        image_list = file_utils.get_images_list(os.path.join(data_root, sub, "JPEGImages"))
        print("process:{},nums:{}".format(anno_file, len(image_list)))
        # 保存VOC格式的xml文件
        out_xml_dir = os.path.join(data_root, sub, "Annotations")
        # 裁剪并保存标注框区域的图片
        out_crop_dir = os.path.join(data_root, sub, "Classification")
        for image_file in tqdm(image_list):
            basename = os.path.basename(image_file)
            image_id = basename.split(".")[0]
            image = cv2.imread(image_file)
            anno = annotation[image_id]
            h, w = image.shape[:2]
            # [top left X pos, top left Y pos, width, height]
            bboxes = image_utils.rects2bboxes(anno['bboxes'])
            bboxes = np.asarray(bboxes) * [w, h, w, h]
            labels = anno['labels']
            class_names += labels
            image_shape = image.shape
            assert len(bboxes) == len(labels)
            if out_xml_dir:
                save_voc_dataset(bboxes, labels, image_file, image_shape, out_xml_dir)
            if out_crop_dir:
                save_crop_dataset(image, bboxes, labels, image_file, out_crop_dir)
            if vis:
                image = image_utils.draw_image_bboxes_text(image, bboxes, labels, color=(255, 0, 0))
                image_utils.cv_show_image("image", image, use_rgb=False)
    class_names = set(class_names)
    print(class_names)


if __name__ == "__main__":
    data_root = "path/to/gesture/HaGRID/trainval"
    convert_HaGRID_dataset(data_root, vis=True)