#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/29 14:07
# @Author  : Kiriya
# @File    : main.py
# @Description : 阴阳师脚本 auto_yys
import random
import time

import utils.kry_util as kry

# 截图存放处
save_path = "screenshot/temp.png"
# 找图相似度
similar = 0.8


def xuan_shang(accept):
    """
    检测悬赏
    :param accept: 是否接受 True/False
    """
    x, y = kry.find_img(save_path, "img/xuan_shang.png")
    if x < 0 and y < 0:
        print("未发现悬赏")
    else:
        print("发现悬赏")
        if accept:
            print("接受悬赏")
            kry.click_random_range([((1258, 592), (1474, 662))])
        else:
            print("拒绝悬赏")
            kry.click_random_range([((1258, 749), (1474, 814))])


def start_common(times, mode):
    """
    通用副本函数：1、御魂 2、御灵
    :param times: 次数
    :param mode: 模式
    """
    if mode == "yu_hun":
        mode_name = "御魂"
        start_img_path = "img/yu_hun_start.png"
        end_img_path = "img/yu_hun_end.png"
    elif mode == "yu_ling":
        mode_name = "御灵"
        start_img_path = "img/yu_ling_start.png"
        end_img_path = "img/yu_ling_end.png"
    else:
        print("模式匹配错误！")
        exit()

    print("进入" + mode_name + "模式：")
    # 当前次数
    current_times = 0
    # 点击开始按钮超时次数
    timeout_times = 10
    # 循环超时次数
    loop_timeout_times = 60
    while times > 0:
        if loop_timeout_times < 1:
            print("循环次数超时！")
            exit()
        loop_timeout_times = loop_timeout_times - 1

        # 点击开始按钮
        flag = kry.find_img_and_click_ran(save_path, start_img_path, similar)
        if flag:
            times = times - 1
            current_times = current_times + 1
            print("当前第", current_times, "次，", "剩余", times, "次")
            # 超时次数-1
            timeout_times = timeout_times - 1
            if timeout_times < 1:
                print("点击开始按钮次数超时，请检查是否有足够的体力/入场券！")
                exit()
            kry.ran_delay(1, 1.5)

        # 结算
        end_x, end_y = kry.find_img(save_path, end_img_path, similar)
        if end_x >= 0 and end_y >= 0:
            # 结算时点击范围
            coordinates = [((774, 841), (1816, 950)),
                           ((1613, 150), (1872, 935))]
            kry.click_random_range(coordinates)
            # 正常结算 初始化超时次数
            timeout_times = 10
            loop_timeout_times = 60

        # 检测悬赏
        xuan_shang(True)

        # 单次循环结束
        kry.ran_delay(1, 1.5)

        ran_wait()
    print(mode_name + "模式执行结束，共执行" + current_times + "次")


def tan_suo(times):
    print("进入探索模式：")
    # 开始
    start_img_path = ""
    # boss
    boss_img_path = ""
    # 小怪
    mob_img_path = ""
    # 探索副本内
    tan_suo_scene = ""
    # 奖励箱子
    bonus_img_path = ""
    # 结束
    end_img_path = ""
    while times > 0:
        # 点击开始按钮
        flag = kry.find_img_and_click_ran(save_path, start_img_path, similar)


def ran_wait():
    """
    防封随机等待
    """
    # 十分之一的概率随机延迟5到10秒
    if random.randint(1, 10) == 1:
        kry.ran_delay(5, 10)
    # 百分之一的概率随机延迟30到60秒
    if random.randint(1, 100) == 1:
        kry.ran_delay(30, 60)


if __name__ == '__main__':
    print("程序开始运行：")
    kry.init_adb()
    start_common(4000, "yu_ling")
    # start_common(500, "yu_hun")

    # x, y = kry.find_img(save_path, "img/yu_ling_start.png")
    # print(x, y)
