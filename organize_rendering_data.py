import glob, os
import csv
import shutil
import numpy as np
from readEXR import readEXR


l = glob.glob('../rendering/clean/**/9x9_baseline0.01', recursive=True)

with open('./focal_length.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    lt = [row for row in reader]

def depth2disp(Z, baseline, focal_length):
    return baseline * focal_length / Z

for scene in l:
    print(scene)
    for iy in range(9):
        for ix in range(9):
            for exr_path in glob.glob(f'{scene}/{iy:02}_{ix:02}/*.exr'):
                # path settings
                old_dir = os.path.dirname(exr_path).replace('\\', '/')
                new_dir = old_dir.replace('../rendering/clean', '../data').replace('/9x9_baseline0.01', '')
                frame = os.path.splitext(os.path.basename(exr_path))[0][1:]    # '**/**/Z0104.exr' -> '0104'
                os.makedirs(new_dir, exist_ok=True)

                # EXR(depth) -> npy(disparity)
                img, Z = readEXR(exr_path)
                for scene_id, num in lt:
                    if scene_id in old_dir:
                        focal_length = float(num)
                disp = depth2disp(Z, baseline=0.01, focal_length=focal_length)
                np.save(f'{new_dir}/{frame}', disp)

                # copy .png
                shutil.copy(f'{old_dir}/{frame}.png', new_dir)