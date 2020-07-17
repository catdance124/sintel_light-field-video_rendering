"""
This is a script that launches a blender in the background and renders a light field animation of a specified blend file.
$ python .\run_blender.py '../clean_files/scenes/07.2_intothecave/07.2b_comp.blend' -resume '1 0' -end '8 8'
"""
import subprocess
import argparse


def render(scene_file_path, resume_point='0 0', end_point='8 8'):
    cmd = r'..\render25_win64\blender.exe' + \
        f' --background {scene_file_path}' + \
        r' --python .\light_field_video_rendering.py' + \
        ' --' + \
        f' --resume_point {resume_point}' + \
        f' --end_point {end_point}'
    print(cmd)
    subprocess.call(cmd, shell=True)


if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('scene_file_path')
    parser.add_argument('-resume', '--resume_point', default='0 0')
    parser.add_argument('-end', '--end_point', default='8 8')
    args = parser.parse_args()

    render(args.scene_file_path, args.resume_point, args.end_point)