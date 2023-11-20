import os
from PIL import Image
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.io import imread

root_dir = 'D:\\VCIP2023\\dataset\\Image\\'

for item in os.listdir(root_dir):   # 遍历root_dir
        name = root_dir + '\\' + item   # 获取图片路径
        save_dir = 'D:\\VCIP2023\\dataset\\encode_bpg\\'   # 存储编码结果
        save_dir1 = 'D:\\VCIP2023\\dataset\\decode_bpg\\'  # 存储解码结果
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        if not os.path.exists(save_dir1):
            os.makedirs(save_dir1)

        os.system('bpgenc -q 28 ' + name + ' -o ' + save_dir + item.split('.')[0] + '.bpg')
        os.system('bpgdec -o ' + save_dir1 + item.split('.')[0] + '.png' + ' ' + save_dir + item.split('.')[0] + '.bpg')
        print("done")

# 定义两个文件夹的路径
folder_path1 = 'D:\\VCIP2023\\dataset\\encode_bpg\\'
folder_path2 = 'D:\\VCIP2023\\dataset\\Image\\'
folder_path3 = 'D:\\VCIP2023\\dataset\\decode_bpg\\'

# 初始化一个空的dataframe来存储结果
df = pd.DataFrame(columns=['图像名称', '图像文件大小(总bits数)', '图像长', '图像宽', '像素总值', 'BPP', 'PSNR'])

# 遍历第一个文件夹中的每个文件以获取文件大小
for filename in os.listdir(folder_path1):
    # 获取文件的完整路径
    file_path1 = os.path.join(folder_path1, filename)
    
    # 获取文件大小
    file_size = os.path.getsize(file_path1) * 8  # 转换为bits
    
    # 在第二个文件夹中找到对应的.png文件并获取其尺寸和像素总值
    base_filename, file_extension = os.path.splitext(filename)
    if file_extension != ".png":
        new_filename = base_filename + ".png"
    else:
        new_filename = filename

    file_path2 = os.path.join(folder_path2, new_filename)
    file_path3 = os.path.join(folder_path3, new_filename)
    if os.path.exists(file_path2) and os.path.exists(file_path3):
        with Image.open(file_path2) as img:
            width, height = img.size
            pixel_count = width * height
            
        # 计算BPP
        bpp = file_size / pixel_count

        # 计算PSNR
        original = imread(file_path2)
        compressed = imread(file_path3)
        psnr = compare_psnr(original, compressed)
            
        # 将结果添加到dataframe中
        df = df.append({'图像名称': new_filename, '图像文件大小(总bits数)': file_size, '图像长': width, '图像宽': height, '像素总值': pixel_count, 'BPP': bpp, 'PSNR': psnr}, ignore_index=True)

# 将结果输出到excel文件中
df.to_excel('output_test.xlsx', index=False)
