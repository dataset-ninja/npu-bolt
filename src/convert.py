import os
import shutil
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)

import src.settings as s
from dataset_tools.convert import unpack_if_archive

# https://www.kaggle.com/datasets/yartinz/npu-bolt


# if sly.is_development():
# load_dotenv("local.env")
# load_dotenv(os.path.expanduser("~/supervisely.env"))

# api = sly.Api.from_env()
# team_id = sly.env.team_id()
# workspace_id = sly.env.workspace_id()


# project_name = "NPU-BOLT"
dataset_path = "APP_DATA/VOCFormat"
batch_size = 30
ds_name = "ds"
images_folder_name = "JPEGImages"
bboxes_folder_name = "Annotations"
bboxes_ext = ".xml"


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    def create_ann(image_path):
        labels = []

        bbox_path = os.path.join(bboxes_path, get_file_name(image_path) + bboxes_ext)

        if file_exists(bbox_path):
            tree = ET.parse(bbox_path)
            root = tree.getroot()

            img_height = int(root.find(".//height").text)
            img_wight = int(root.find(".//width").text)

            coords_xml = root.findall(".//object")
            for curr_object in coords_xml:
                class_name = curr_object.find(".//name").text
                obj_class_name = name_to_real_name[class_name]
                obj_class = meta.get_obj_class(obj_class_name)

                curr_coord = curr_object.find(".//bndbox")

                left = int(curr_coord[0].text)
                top = int(curr_coord[1].text)
                right = int(curr_coord[2].text)
                bottom = int(curr_coord[3].text)

                rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
                label = sly.Label(rect, obj_class)
                labels.append(label)

            tag_name = abbr2source[os.path.basename(bbox_path).split("-")[0]]
            tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == tag_name]

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    name_to_real_name = {
        "bolt_a": "bolt head",
        "bolt_b": "bolt nut",
        "bolt_c": "bolt side",
        "vague": "blur bolt",
    }

    obj_class_a = sly.ObjClass("bolt head", sly.Rectangle)
    obj_class_b = sly.ObjClass("bolt nut", sly.Rectangle)
    obj_class_c = sly.ObjClass("bolt side", sly.Rectangle)
    obj_class_vague = sly.ObjClass("blur bolt", sly.Rectangle)

    tag_names = [
        "captured by authors",
        "from internet",
        "3D CAD simulation",
    ]
    abbr2source = {k: v for k, v in zip(["AUT", "WEB", "CAD"], tag_names)}
    tag_metas = [sly.TagMeta(name, sly.TagValueType.NONE) for name in tag_names]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class_a, obj_class_b, obj_class_c, obj_class_vague], tag_metas=tag_metas
    )
    api.project.update_meta(project.id, meta.to_json())

    images_path = os.path.join(dataset_path, images_folder_name)
    bboxes_path = os.path.join(dataset_path, bboxes_folder_name)

    images_names = os.listdir(images_path)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for images_names_batch in sly.batched(images_names, batch_size=batch_size):
        img_pathes_batch = [
            os.path.join(images_path, image_name) for image_name in images_names_batch
        ]

        img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(images_names_batch))
