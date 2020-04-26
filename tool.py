import os
import cv2
from PIL import Image

def list_files(root_dir, ext_name=".jpg", prefix_name=None):
    """
    #TODO:Add comments
    """
    #
    path_list = list()
    #
    sub_paths = os.walk(root_dir)
    for root, dirs, files in sub_paths:
        #
        for cur_file in files:
            if prefix_name is not None:
                if not cur_file.startswith(prefix_name):
                    continue
            if ext_name is None or cur_file.endswith(ext_name):
                cur_path = os.path.join(root, cur_file)
                path_list.append(cur_path)
    #
    return path_list

def extract_frames(video_path):
    head_img = None
    tail_img = None
    video_capture = cv2.VideoCapture(video_path)
    is_first = True
    prev_img = None
    while(video_capture.isOpened()):
        ret, frame_img = video_capture.read()
        if not ret:
            break
        if is_first:
            head_img = frame_img
            is_first = False
        prev_img = frame_img
    video_capture.release()
    #
    tail_img = prev_img
    return head_img, tail_img

def extract_videos(src_dir, dest_dir):
    #
    this_dir = os.path.dirname(__file__)
    src_dir = os.path.join(this_dir, src_dir)
    dest_dir = os.path.join(this_dir, dest_dir)
    #
    video_paths = list_files(src_dir, ext_name=".mp4")
    for video_idx, video_path in enumerate(video_paths):
        print("[%d/%d] Processing %s"%(video_idx + 1, len(video_paths), video_path))
        head_img, tail_img = extract_frames(video_path)
        head_path = os.path.join(dest_dir, "frame_%d_1.png"%video_idx)
        tail_path = os.path.join(dest_dir, "frame_%d_2.png"%video_idx)
        if (head_img is None) or (tail_img is None):
            print("Failed to extract frame...");
            continue
        cv2.imwrite(head_path, head_img)
        cv2.imwrite(tail_path, tail_img)
    #
#
#extract_videos("./dataset/douyin_photo_painting-20191107", "./dataset/train/20191107")

def rename_images(src_dir, dest_dir):
    #
    this_dir = os.path.dirname(__file__)
    src_dir = os.path.join(this_dir, src_dir)
    dest_dir = os.path.join(this_dir, dest_dir)
    #
    img_paths = list_files(src_dir, ext_name=None)
    for img_idx, img_path in enumerate(img_paths):
        print("[%d/%d] Processing %s"%(img_idx, len(img_paths), img_path))
        img = Image.open(img_path)
        dest_path = os.path.join(dest_dir, "img_%04d.png"%(img_idx + 1))
        img.save(dest_path)
#
rename_images("./dataset/taobao_photo_painting-20191106", "./dataset/train/20191106")

