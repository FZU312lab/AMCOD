'''
python ./run/s1_dataset_check_format.py
    -d *必填 数据集的id编号
    -overwrite_id 覆盖已有id
    -np 指定处理的线程数
示例：
python ./run/s1_dataset_check_format.py -d 4
'''
import sys
import os
import shutil

project_root = os.environ.get('PROJECT_ROOT', os.getcwd())
sys.path.append(project_root)
temp_dir = os.path.join(project_root, 'DATA', 'dataset_temp')

from dataset_conversion.convert_MSD_dataset import convert_msd_dataset
import argparse
from configuration import default_num_processes
import json


def check_dir(id: str):
    sub_dirs = os.listdir(temp_dir)
    target_dir = ''
    for s in sub_dirs:
        if id in s:
            target_dir = s
            break
    if target_dir == '':
        print('数据集不存在')
        return False
    else:
        # 检查命名规范
        if not target_dir.startswith('Task'):
            print('文件夹请以"Task+ID号_名称"命名')
            return False
        if not '_' in target_dir:
            print('文件夹请以"Task+ID号_名称"命名')
            return False
        path = os.path.join(temp_dir, target_dir)
        sub_path = os.listdir(path)
        if not 'imagesTr' in sub_path:
            print('imagesTr不存在')
            return False
        if not 'labelsTr' in sub_path:
            print('labelsTr不存在')
            return False
        dataset_json = os.path.join(temp_dir, target_dir, 'dataset.json')
        if not os.path.exists(dataset_json):
            print('dataset.json不存在，到DATASETS/example_dataset.json复制修改')
            return False
        else:
            with open(dataset_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not data['name'] or data['name'] == '':
                print('dataset.json中的name不能为空')
                return False
            if not data['modality'] or len(data['modality']) == 0:
                print('dataset.json中的modality不能为空')
                return False
            if not data['tensorImageSize'] or data['tensorImageSize'] == '':
                print('dataset.json中的tensorImageSize不能为空')
                return False
            if not data['labels'] or len(data['labels']) <= 1:
                print('dataset.json中的labels不能为空')
                return False
    return target_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, required=True,
                        help='input the dataset temp id')
    parser.add_argument('-overwrite_id', type=int, required=False, default=None,
                        help='Overwrite the dataset id. If not set we use the id of the MSD task (inferred from '
                             'folder name). Only use this if you already have an equivalently numbered dataset!')
    parser.add_argument('-np', type=int, required=False, default=default_num_processes,
                        help=f'Number of processes used. Default: {default_num_processes}')
    args = parser.parse_args()
    id = args.d

    target_dir = check_dir(id)
    if not target_dir:
        print("dataset_temp中的文件不规范，原始文件标准见readme.md")
    else:
        print('原始数据集完成检查，可以执行下一步')
        path = os.path.join(temp_dir, target_dir)
        convert_msd_dataset(path, args.overwrite_id, args.np)
        print('文件已完成迁移，可以执行预处理')
        shutil.rmtree(path)
        print(target_dir + '文件夹已从dataset_temp中删除')