#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/29 14:07
# @Author  : Kiriya
# @File    : kry_util.py
# @Description : 图像识别、shell点击工具类
import random
import subprocess
import time

import cv2
import numpy as np


def init_adb():
    subprocess.run(['adb', 'kill-server'])
    subprocess.run(['adb', 'start-server'])
    subprocess.run(['adb', 'devices'])


def click(x, y):
    """
    单击
    :param x: 坐标x
    :param y: 坐标y
    """
    print("点击：", "x:", x, "y:", y)
    subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])


def click_random_range(coordinates):
    """
    随机点击指定范围（多个）
    :param coordinates: [((1, 2), (3, 4)), ((5, 6), (7, 8))]
    """
    # 随机选一个范围
    random_coordinate_pair = random.choice(coordinates)
    # 左上坐标
    x1, y1 = random_coordinate_pair[0]
    # 右下坐标
    x2, y2 = random_coordinate_pair[1]
    x, y = get_random_xy(x1, x2, y1, y2)
    click(x, y)


def get_random_xy(x1, x2, y1, y2):
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    return x, y


def screen_cap(save_path):
    """
    截图
    :param save_path: 截图保存路径
    """
    # 在设备上执行截图命令
    subprocess.run(['adb', 'shell', 'screencap', '/sdcard/screenshot.png'])
    # 将截图从设备复制到电脑
    subprocess.run(['adb', 'pull', '/sdcard/screenshot.png', save_path])


def find_img(source_img_path, find_img_path, similar=0.8):
    """
    找图
    :param source_img_path: 源图片路径
    :param find_img_path: 需要查找的图片路径
    :param similar: 相似度（匹配的阈值）
    :return: x,y坐标
    """
    # 取图片名字：用‘/’分割后取最后一个
    img_name = find_img_path.split("/")[-1]
    print("开始找图：", img_name)
    # 获取最新截图
    screen_cap(source_img_path)

    # 读取待检查的图片和截图
    image = cv2.imread(find_img_path)
    screenshot = cv2.imread(source_img_path)

    # 将图片和截图转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 使用模板匹配来查找图片在截图中的位置
    result = cv2.matchTemplate(gray_screenshot, gray_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 如果找到匹配的位置，则图片在截图中出现过
    if max_val >= similar:
        x, y = max_loc
        print("找到图片：", img_name, "x:", x, "y:", y)
        # 获取最佳匹配位置的坐标
        return x, y
    print("未找到图片：", img_name)
    return -1, -1


def find_img_and_click_ran(source_img_path, find_img_path, similar=0.8):
    """
    找图 如果找到则在该图范围内点击一次
    :param source_img_path: 源图片路径
    :param find_img_path: 需要查找的图片路径
    :param similar: 相似度（匹配的阈值）
    :return: 是否找到
    """
    x, y = find_img(source_img_path, find_img_path, similar)
    if x < 0 and y < 0:
        return False

    # 获取查找图片长宽
    img = cv2.imread(find_img_path)
    width, height = img.shape[0:2]

    # 获取图片范围内随机坐标
    ran_x = random.randint(0, width)
    ran_y = random.randint(0, height)

    # 点击图片内随机坐标
    click(x + ran_x, y + ran_y)
    return True


def ran_delay(min_second, max_second):
    """
    随机延时
    :param min_second: 最小秒数
    :param max_second: 最大秒数
    """
    ran = random.uniform(min_second, max_second)
    print("随机延时", ran, "秒")
    time.sleep(ran)
