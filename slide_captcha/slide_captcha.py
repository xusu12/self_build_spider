# -*- coding: utf-8 -*-
import random
import requests
import time, re
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# 访问虎嗅页面  点击注册按钮
def visit_index(driver):
    driver.get("https://www.huxiu.com/")

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="js-register"]')))
    # 定位注册按钮
    reg_element = driver.find_element_by_xpath('//*[@class="js-register"]')
    # 点击注册按钮
    reg_element.click()


# 鼠标移动到拖动按钮，显示出拖动图片
def move_to_element(driver):
    # 找到滑块的按钮
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_slider_knob gt_show"]')))
    element = driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
    # 鼠标移动到滑块的位置
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(1)


# 获取图片和位置列表
def get_image_url(driver, xpath):
    link = re.compile('background-image: url\("(.*?)"\); background-position: (.*?)px (.*?)px;')
    elements = driver.find_elements_by_xpath(xpath)
    image_url = None
    location = list()
    for element in elements:
        style = element.get_attribute("style")
        groups = link.search(style)
        url = groups[1]
        x_pos = groups[2]
        y_pos = groups[3]
        location.append((int(x_pos), int(y_pos)))
        image_url = url
    return image_url, location

    # 拼接图片
    def mosaic_image(self, image_url, location):
        print(image_url)
        resq = requests.get(image_url)
        file = BytesIO(resq.content)
        img = Image.open(file)
        image_upper_lst = []
        image_down_lst = []
        for pos in location:
            if pos[1] == 0:
                # y值==0的图片属于上半部分，高度58
                image_upper_lst.append(img.crop((abs(pos[0]), 0, abs(pos[0]) + 10, 58)))
            else:
                # y值==58的图片属于下半部分
                image_down_lst.append(img.crop((abs(pos[0]), 58, abs(pos[0]) + 10, img.height)))

        x_offset = 0
        # 创建一张画布，x_offset主要为新画布使用
        new_img = Image.new("RGB", (260, img.height))
        for img in image_upper_lst:
            new_img.paste(img, (x_offset, 58))
            x_offset += img.width

        x_offset = 0
        for img in image_down_lst:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.width

        return new_img


# 拼接图片
def mosaic_image(image_url, location):
    print(image_url)
    resq = requests.get(image_url)
    file = BytesIO(resq.content)
    img = Image.open(file)
    image_upper_lst = []
    image_down_lst = []
    for pos in location:
        if pos[1] == 0:
            # y值==0的图片属于上半部分，高度58
            image_upper_lst.append(img.crop((abs(pos[0]), 0, abs(pos[0]) + 10, 58)))
        else:
            # y值==58的图片属于下半部分
            image_down_lst.append(img.crop((abs(pos[0]), 58, abs(pos[0]) + 10, img.height)))

    x_offset = 0
    # 创建一张画布，x_offset主要为新画布使用
    new_img = Image.new("RGB", (260, img.height))
    for img in image_upper_lst:
        new_img.paste(img, (x_offset, 58))
        x_offset += img.width

    x_offset = 0
    for img in image_down_lst:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.width

    return new_img


# 判断颜色是否相近
def is_similar_color(x_pixel, y_pixel):
    for i, pixel in enumerate(x_pixel):
        if abs(y_pixel[i] - pixel) > 50:
            return False
    return True


# 计算距离
def get_offset_distance(cut_image, full_image):
    for x in range(cut_image.width):
        for y in range(cut_image.height):
            cpx = cut_image.getpixel((x, y))
            fpx = full_image.getpixel((x, y))
            if not is_similar_color(cpx, fpx):
                img = cut_image.crop((x, y, x + 50, y + 40))
                # 保存一下计算出来位置图片，看看是不是缺口部分
                # img.save("1.jpg")
                return x


# 开始移动
def start_move(driver, distance):
    element = driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')

    # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
    distance -= element.size.get('width') / 2
    distance += 15

    # 按下鼠标左键
    ActionChains(driver).click_and_hold(element).perform()
    time.sleep(0.2)
    while distance > 0:
        if distance > 10:
            # 如果距离大于10，就让他移动快一点
            span = random.randint(15, 18)
        else:
            # 快到缺口了，就移动慢一点
            span = random.randint(1, 2)
            span = 1
        ActionChains(driver).move_by_offset(span, 0).perform()
        distance -= span
        time.sleep(random.randint(10, 50) / 100)

    ActionChains(driver).move_by_offset(distance, 1).perform()
    ActionChains(driver).release(on_element=element).perform()


# 滑动验证成功后  输入手机号注册
def register(driver):
    element = driver.find_element_by_xpath('//input[@id="sms_username"]')
    element.clear()
    element.send_keys("13900112233")

    ele_captcha = driver.find_element_by_xpath('//span[@class="js-btn-captcha btn-captcha"]')
    ele_captcha.click()


# 滑动验证成功后  输入手机号注册
def register(driver):
    element = driver.find_element_by_xpath('//input[@id="sms_username"]')
    element.clear()
    # 输入手机号
    element.send_keys("13900112233")
    # 点击发送短信按钮
    ele_captcha = driver.find_element_by_xpath('//span[@class="js-btn-captcha btn-captcha"]')
    ele_captcha.click()


def run(driver):
    # 1. 访问虎嗅页面  点击注册按钮
    visit_index(driver)

    # 2. 鼠标移动到滑块的位置
    move_to_element(driver)

    # 3. # 获取有缺口的图片
    cut_image_url, cut_location = get_image_url(driver, '//div[@class="gt_cut_bg_slice"]')
    # 获取没有缺口的完整的图片
    full_image_url, full_location = get_image_url(driver, '//div[@class="gt_cut_fullbg_slice"]')

    # 4. 根据坐标拼接完整的图片
    cut_image = mosaic_image(cut_image_url, cut_location)
    full_image = mosaic_image(full_image_url, full_location)

    # 5. 根据两个图片计算距离
    distance = get_offset_distance(cut_image, full_image)

    # 6. 开始移动
    start_move(driver, distance)

    # 7. 成功后输入手机号，发送验证码
    register(driver)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.set_window_size(1300, 800)
    run(driver)
