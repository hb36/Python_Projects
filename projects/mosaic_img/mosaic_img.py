# -*-encoding='utf-8'-*-
"""
使用Python创建照片马赛克
输入一张目标照片和多张替换照片，将目标照片按网格划分为许多小方格，然后就小方格替换为颜色值
最接近的那张替换照片，就形成了马赛克效果
"""
from PIL import Image
import numpy as np
import os
import argparse


def get_imgs(img_dir):
    """
    从给定目录中加载所有替换图像
    :param img_dir: 目录路径
    :return: {List[img]}替换图像列表
    """
    files = os.listdir(img_dir)
    imgs = []
    for file in files:
        file_path = os.path.abspath(os.path.join(img_dir, file))
        try:
            fp = open(file_path, 'rb')
            im = Image.open(fp)
            imgs.append(im)
            im.load()
            fp.close()
        except:
            print("Invalid image: %s" % (file_path,))
    return imgs


def get_average_RGB(img):
    """
    计算图像的平均RGB值
    将图像包含的每个像素点的RGB值分别累加，然后除以像素点数，就得到像素的平均RGB
    :param img:Image对象
    :return:{Tuple[int,int,int]}平均RGB值
    """
    # 计算像素点数
    pixels_num = img.size[0] * img.size[1]
    colors = img.getcolors(pixels_num)
    RGB_sum = [(x[0] * x[1][0], x[0] * x[1][1], x[0] * x[1][2]) for x in colors]
    RGB_avg = tuple([int(sum(x) / pixels_num) for x in zip(*RGB_sum)])
    return RGB_avg


def get_average_RGB_np(img):
    """
    使用numpy计算图像的RGB平均值
    :param img: PIL Image对象
    :return: RGB平均值
    """
    im = np.array(img)
    w, h, d = im.shape
    return tuple(np.average(im.reshape(w * h, d), axis=0))


def split_img(img, grid_size):
    """
    将图像按网格划分成多个小图像
    :param img: PIL Image 对象
    :param grid_size: 网格的行数和列数
    :return: 小图像列表
    """
    width = img.size[0]
    height = img.size[1]
    m, n = grid_size
    w = int(width / n)
    h = int(height / m)
    imgs = []

    for j in range(m):
        for i in range(n):
            imgs.append(img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
    return imgs


def get_best_match_index(target_avg, avgs):
    """
    找出颜色值最接近的索引
    :param target_avg: 目标颜色值
    :param avgs: 要搜索的颜色值列表
    :return:命中元素的索引
    """
    index = 0
    min_index = 0
    min_dist = float("inf")
    for val in avgs:
        dist = ((val[0] - target_avg[0]) * (val[0] - target_avg[0]) +
                (val[1] - target_avg[1]) * (val[1] - target_avg[1]) +
                (val[2] - target_avg[2]) * (val[2] - target_avg[2]))
        if dist < min_dist:
            min_dist = dist
            min_index = index
        index += 1
    return min_index


def create_img_grid(output_imgs, grid_size):
    """
    将图像列表里的小图像按先行后列的顺序拼接为一个大图像
    :param imgs: 小图像列表
    :param dims: 大图像的行数和列数
    :return: 拼接得到的大图像
    """
    m, n = grid_size

    # 若不允许重用，确保小图像个数满足要求
    # assert m * n == len(imgs)

    # 计算所有小图像的最大宽度和高度
    width = max([img.size[0] for img in output_imgs])
    height = max([img.size[1] for img in output_imgs])

    # 创建大图像对象
    grid_img = Image.new('RGB', (n * width, m * height))

    # 依次将每个小图像粘贴到大图像里
    for index in range(len(output_imgs)):
        row = int(index / n)
        col = index - n * row
        grid_img.paste(output_imgs[index], (col * width, row * height))

    return grid_img


def create_mosaic_img(target_img, input_imgs, grid_size, reuse_imgs=True):
    """
    马赛克照片的生成
    :param target_img:目标图像
    :param input_imgs: 替换图像列表
    :param grid_size: 网格行数和列数
    :param reuse_imgs: 是否允许重复使用替换图像
    :return: 马赛克图像
    """
    # 将目标图像切成网格小图像
    print('splitting input image...')
    target_imgs = split_img(target_img, grid_size)

    # 为每个网格小图像在替换图像列表里找到颜色最相近的替换图像
    print('finding image matches...')
    output_imgs = []
    # 分10组进行，每组完成后打印进度信息
    count = 0
    batch_size = int(len(target_imgs) / 10)

    # 计算替换图像列表里每个图像的颜色平均值
    avgs = []

    for img in input_imgs:
        avgs.append(get_average_RGB(img))

    for img in target_imgs:
        avg = get_average_RGB(img)
        match_index = get_best_match_index(avg, avgs)
        output_imgs.append(input_imgs[match_index])
        if count > 0 and batch_size > 10 and count % batch_size == 0:
            print('processed %d of %d...' % (count, len(target_imgs)))
        count += 1
        # 如果不允许重用替换图像，则用后从列表中移除
        if not reuse_imgs:
            input_imgs.remove(match_index)

    # 将output_imgs 拼接成一个大图像
    print('creating mosaic...')
    mosaic_img = create_img_grid(output_imgs, grid_size)

    return mosaic_img


def main():
    # 定义程序接收的命令行参数
    # parser = argparse.ArgumentParser(description='Creates a imgmosaic from input images')
    # parser.add_argument('--target_img', dest='target_img', required=True)
    # parser.add_argument('--input_folder', dest='input_folder', required=True)
    # parser.add_argument('--grid_size', nargs=2, dest='grid_size', required=True)
    # parser.add_argument('--output_file', dest='output_file', required=False)
    #
    # args = parser.parse_args('--target_img E:\Python36\projects\mosaic_img\\test-data\\a.jpg '
    #                          '--input_folder E:\Python36\projects\mosaic_img\\test-data\set1 '
    #                          '--grid_size 128 128 '
    #                          '--output_file E:\Python36\projects\mosaic_img\mosaic.png'.split())
    target_img = 'E:\Python36\projects\mosaic_img\\test-data\\a.jpg'
    input_folder = 'E:\Python36\projects\mosaic_img\\test-data\set1'
    grid_size = (128, 128)
    output_file = 'E:\Python36\projects\mosaic_img\mosaic.png'

    # output_filename = 'mosaic.png'
    # if args.output_file:
    #     output_filename = args.output_file

    # 打开目标图像
    print('reading target image...')
    target_img = Image.open(target_img)

    # 从指定文件夹下加载所有替换图像
    print('reading input images...')
    input_imgs = get_imgs(input_folder)

    if input_imgs == []:
        print('No input images found in %s,Exiting.' % (input_folder,))
        exit()

    # 将所有替换图像缩放到指定的网格大小
    print('resizing images...')
    dims = (int(target_img.size[0] / grid_size[1]),
            int(target_img.size[1] / grid_size[0]))
    for img in input_imgs:
        img.thumbnail(dims)

    print('starting imgmosaix creation...')
    mosaic_img = create_mosaic_img(target_img, input_imgs, grid_size)

    mosaic_img.save(output_file, 'PNG')
    print("save output to %s" % (output_file,))

    print('done.')


if __name__ == '__main__':
    main()
