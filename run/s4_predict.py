'''
python ./run/s4_predict.py
    -i input folder *必须
    -o Output folder *必须
    -d datasetid,相当于选择相同任务 *必须
    -c configuration !required [2d, 3d_fullres, 3d_lowres]
    -f folder 如果没有合折训练就必须指定第几折
    -chk 默认是checkpoint_best.pth，可以改成checkpoint_final.pth
    -p plans
    -tr trainer
    -step_size 滑窗步长，默认0.5
    --disable_tta
    --verbose
    --save_probabilities
    --continue_prediction
    -npp 预处理线程数
    -nps 分割线程数
    -prev_stage_predictions
    -num_parts
    -part_id
    -device
    --disable_progress_bar
示例：
    python ./run/s4_predict.py
        -i F:\nnUNet-master\nnunetv2\DATASETS\nnUNet_raw\Dataset004_Hippocampus\imagesTs
        -o F:\nnUNet-master\nnunetv2\DATASETS\nnUNet_results\Dataset004_Hippocampus\test
        -d 004
'''

import sys
import os
project_root = os.environ.get('PROJECT_ROOT', os.getcwd())
sys.path.append(project_root)

from inference.predict_from_raw_data import predict_entry_point

if __name__ == '__main__':
    predict_entry_point()