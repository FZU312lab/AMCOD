import argparse
import multiprocessing
import shutil
from multiprocessing import Pool
from typing import Optional
import SimpleITK as sitk
from batchgenerators.utilities.file_and_folder_operations import *
from paths import nnUNet_raw
from utilities.dataset_name_id_conversion import find_candidate_datasets
from configuration import default_num_processes
import numpy as np


def split_4d_nifti(filename, output_folder):
    img_itk = sitk.ReadImage(filename)
    dim = img_itk.GetDimension()
    file_base = os.path.basename(filename)
    if dim == 3:
        shutil.move(filename, join(output_folder, file_base[:-7] + "_0000.nii.gz"))
        return
    elif dim != 4:
        raise RuntimeError("Unexpected dimensionality: %d of file %s, cannot split" % (dim, filename))
    else:
        img_npy = sitk.GetArrayFromImage(img_itk)
        spacing = img_itk.GetSpacing()
        origin = img_itk.GetOrigin()
        direction = np.array(img_itk.GetDirection()).reshape(4, 4)
        # now modify these to remove the fourth dimension
        spacing = tuple(list(spacing[:-1]))
        origin = tuple(list(origin[:-1]))
        direction = tuple(direction[:-1, :-1].reshape(-1))
        for i, t in enumerate(range(img_npy.shape[0])):
            img = img_npy[t]
            img_itk_new = sitk.GetImageFromArray(img)
            img_itk_new.SetSpacing(spacing)
            img_itk_new.SetOrigin(origin)
            img_itk_new.SetDirection(direction)
            sitk.WriteImage(img_itk_new, join(output_folder, file_base[:-7] + "_%04.0d.nii.gz" % i))


def convert_msd_dataset(source_folder: str,
                        overwrite_target_id: Optional[int] = None,
                        num_processes: int = default_num_processes) -> None:
    if source_folder.endswith('/') or source_folder.endswith('\\'):
        source_folder = source_folder[:-1]

    labelsTr = join(source_folder, 'labelsTr')
    imagesTr = join(source_folder, 'imagesTr')

    assert isdir(labelsTr), f"labelsTr subfolder missing in source folder"
    assert isdir(imagesTr), f"imagesTr subfolder missing in source folder"

    dataset_json = join(source_folder, 'dataset.json')
    assert isfile(dataset_json), f"dataset.json missing in source_folder"

    # infer source dataset id and name
    task, dataset_name = os.path.basename(source_folder).split('_')
    task_id = int(task[4:])

    # check if target dataset id is taken
    target_id = task_id if overwrite_target_id is None else overwrite_target_id
    existing_datasets = find_candidate_datasets(target_id)
    assert len(existing_datasets) == 0, f"Target dataset id {target_id} is already taken, please consider changing " \
                                        f"it using overwrite_target_id. Conflicting dataset: {existing_datasets} (check nnUNet_results, nnUNet_preprocessed and nnUNet_raw!)"

    target_dataset_name = f"Dataset{target_id:03d}_{dataset_name}"
    target_folder = join(nnUNet_raw, target_dataset_name)
    target_imagesTr = join(target_folder, 'imagesTr')
    target_labelsTr = join(target_folder, 'labelsTr')
    maybe_mkdir_p(target_imagesTr)
    maybe_mkdir_p(target_labelsTr)
    # 将imagesTr和labelsTr移动到目标位置
    source_images = [i for i in subfiles(imagesTr, suffix='.nii.gz', join=False) if
                     not i.startswith('.') and not i.startswith('_') and i.endswith('.nii.gz')]
    source_labels = [i for i in subfiles(labelsTr, suffix='.nii.gz', join=False) if
                     not i.startswith('.') and not i.startswith('_') and i.endswith('.nii.gz')]
    assert len(source_images)==len(source_labels),'imagesTr和labelsTr中的文件数不一致'
    num_training = len(source_images)
    for i in range(len(source_images)):
        base_name = source_images[i][:-7]
        shutil.move(join(imagesTr, source_images[i]), join(target_imagesTr, base_name + "_0000.nii.gz"))
        shutil.move(join(labelsTr, source_labels[i]), join(target_labelsTr, source_images[i]))
    dataset_json = load_json(dataset_json)
    dataset_json['labels'] = {j: int(i) for i, j in dataset_json['labels'].items()}
    dataset_json['file_ending'] = ".nii.gz"
    dataset_json["channel_names"] = dataset_json["modality"]
    if "modality" in dataset_json:
        del dataset_json["modality"]
    if "training" in dataset_json:
        del dataset_json["training"]
    if "test" in dataset_json:
        del dataset_json["test"]
    if "numTraining" not in dataset_json or dataset_json["numTraining"]!=num_training:
        dataset_json["numTraining"] = num_training
    save_json(dataset_json, join(nnUNet_raw, target_dataset_name, 'dataset.json'), sort_keys=False)


def entry_point():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True,
                        help='Downloaded and extracted MSD dataset folder. CANNOT be nnUNetv1 dataset! Example: '
                             '/home/fabian/Downloads/Task05_Prostate')
    parser.add_argument('-overwrite_id', type=int, required=False, default=None,
                        help='Overwrite the dataset id. If not set we use the id of the MSD task (inferred from '
                             'folder name). Only use this if you already have an equivalently numbered dataset!')
    parser.add_argument('-np', type=int, required=False, default=default_num_processes,
                        help=f'Number of processes used. Default: {default_num_processes}')
    args = parser.parse_args()
    convert_msd_dataset(args.i, args.overwrite_id, args.np)


if __name__ == '__main__':
    convert_msd_dataset('D:/DATASET/MSD/Task04_Hippocampus/raw/Task04_Hippocampus', overwrite_target_id=201)
