"""
This script renders the light field animation.
This script runs in python v3.1.2 bundled in blender(render25).
"""
import bpy
import mathutils
import os
import glob
import sys


# rendering settings
scene = bpy.context.scene
scene.render.resolution_x = 1024
scene.render.resolution_y = 436
scene.render.resolution_percentage = 100
scene.render.antialiasing_samples = '5'
scene.render.color_mode = 'RGB'
scene.render.file_format = 'PNG'
scene.render.fps = 24

# Turns off transparency for all objects.
for mat in bpy.data.materials:
    if mat.alpha < 1:
        print(mat.name)
        mat.transparency = False
        mat.alpha = 1.0
        for ts in mat.texture_slots:
            if ts is not None:
                ts.map_alpha = False

# output dir settings
blend_filepath = bpy.data.filepath
middle_class_name = os.path.basename(os.path.dirname(blend_filepath))
small_class_name = os.path.splitext(os.path.basename(blend_filepath))[0]
output_dir = '../rendering/clean/{}/{}'.format(middle_class_name, small_class_name)
def register_output_dir(output_dir):
    def my_makedirs(path):
        if not os.path.isdir(path):
            os.makedirs(path)
    my_makedirs(output_dir)
    scene.render.output_path = output_dir
register_output_dir(output_dir)

# capture light field
def move_along_local_axis(obj, delta_vec=(0.0, 0.0, 0.0)):
    delta_vec = mathutils.Vector(delta_vec)
    inv = obj.rotation_euler.to_matrix()
    inv.invert()
    # vec aligned to local axis
    obj.location += delta_vec * inv

def capture_light_field(camera, num_cams=(5, 5), baseline=0.1, resume_point=(0, 0), end_point=None):
    if end_point is None:
        end_point = (num_cams[0]-1, num_cams[1]-1)
    print('=============================\n=============================')
    print('rendering' + str(resume_point) + 'to' + str(end_point))
    print('=============================\n=============================')
    ## initial camera move
    init_location = camera.location.copy()
    print(init_location)
    move_along_local_axis(camera, ((num_cams[1] // 2 *(-1)) * baseline, (num_cams[1] // 2) * baseline, 0))
    ## grid camera move
    for iy in range(num_cams[0]):
        for ix in range(num_cams[1]):
            # rendering
            if (not iy*10+ix < resume_point[0]*10+resume_point[1]) and (not iy*10+ix > end_point[0]*10+end_point[1]):
                current_output_dir = output_dir + '/{}x{}_baseline{}/{:02d}_{:02d}/'.format(num_cams[1], num_cams[0], baseline, iy, ix)
                for node in scene.nodetree.nodes:
                    if 'File Output' in node.name:
                        node.image_type = 'OPENEXR'
                        node.filepath = current_output_dir + 'Z'
                register_output_dir(current_output_dir)
                # Get the completed frame
                png_list = glob.glob(current_output_dir + '*.png')
                exr_list = glob.glob(current_output_dir + '*.exr')
                if len(png_list) != 0 and len(exr_list) != 0:
                    completed_frame = min(int(png_list[-1][-8:-4]), int(exr_list[-1][-8:-4]))
                    scene.frame_start, temp = completed_frame+1, scene.frame_start
                print('START:'+str(scene.frame_start)+', END:'+str(scene.frame_end))
                if scene.frame_start < scene.frame_end:
                    print('rendering:', iy, ix)
                    bpy.ops.render.render(animation=True)
                if len(png_list) != 0 and len(exr_list) != 0:
                    scene.frame_start = temp
            move_along_local_axis(camera, (baseline, 0, 0))
        move_along_local_axis(camera, (-num_cams[0] * baseline, 0, 0))
        move_along_local_axis(camera, (0, -baseline, 0))
    camera.location = init_location


if '__main__' == __name__:
    # get args given to python
    # $.\blender.exe --background --python hoge.py -- --resume_point 0 0 --end_point 3 2
    #     --> ['--resume_point', '0', '0', '--end_point', '3', '2']
    argv = sys.argv
    argv = argv[argv.index('--') + 1:]    # get all args after '--'
    
    if '--resume_point' in argv:
        idx = argv.index('--resume_point')
        resume_point = (int(argv[idx + 1]), int(argv[idx + 2]))
    else:
        resume_point = (0, 0)
    if '--end_point' in argv:
        idx = argv.index('--end_point')
        end_point = (int(argv[idx + 1]), int(argv[idx + 2]))
    else:
        end_point = None
    
    if '--frame_start' in argv:
        idx = argv.index('--frame_start')
        scene.frame_start = int(argv[idx + 1])
    if '--frame_end' in argv:
        idx = argv.index('--frame_end')
        scene.frame_end = int(argv[idx + 1])
    print(scene.frame_start, scene.frame_end)
    
    capture_light_field(camera=scene.camera, num_cams=(9, 9), baseline=0.01, resume_point=resume_point, end_point=end_point)