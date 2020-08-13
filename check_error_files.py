import glob, os
import numpy as np


l = glob.glob('../rendering/clean/**/9x9_baseline0.01', recursive=True)

# get all file paths
scenes = []
for i, scene in enumerate(l):
    frames = []
    for frame in glob.glob(f'{scene}/00_00/*.png'):
        basename = os.path.basename(frame)
        arr = np.zeros((9,9))
        for y in range(9):
            for x in range(9):
                arr[y, x] = os.path.getsize(f'{scene}/{y:02}_{x:02}/{basename}')
        frames.append(arr)
    scenes.append(frames)

# check error files
errors = []
for i, scene in enumerate(l):
    for j, frame in enumerate(glob.glob(f'{scene}/00_00/*.png')):
        if np.any(scenes[i][j] - scenes[i][j].mean() < -50000):
            if not '06.k_comp' in frame:
                for iy, ix in list(zip(*np.where(scenes[i][j] - scenes[i][j].mean() < -50000))):
                    errors.append(frame.replace('00_00', f'{iy:02}_{ix:02}').replace('\\','/'))
print('error num: ', len(errors))
print('all error files:')
for e in errors:
    print(e)

print('central vertical/horizontal error files:')
for i in sorted(errors):
    if (i[-13] == '4' or i[-10] == '4'):
        print(i)