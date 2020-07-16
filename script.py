import subprocess


def render(scene_file_path):
    cmd = r'..\render25_win64\blender.exe' + \
        f' --background {scene_file_path}' + \
        r' --python .\light_field_video_rendering.py'
    print(cmd)
    subprocess.call(cmd, shell=True)

render('../clean_files/scenes/07.2_intothecave/07.2b_comp.blend')
render('../clean_files/scenes/04.1_ziggurat/04.1a_comp.blend')