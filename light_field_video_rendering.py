import bpy
import mathutils
import os


# rendering settings
scene = bpy.context.scene
scene.render.resolution_x = 1024
scene.render.resolution_y = 436
scene.render.resolution_percentage = 100
scene.render.antialiasing_samples = '5'
scene.render.color_mode = 'RGB'
scene.render.file_format = 'PNG'
scene.render.fps = 24
#scene.frame_start = 411
#scene.frame_end = 415

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
    ## initial camera move
    init_location = camera.location.copy()
    print(init_location)
    move_along_local_axis(camera, ((num_cams[1] // 2 *(-1)) * baseline, (num_cams[1] // 2) * baseline, 0))
    ## grid camera move
    for iy in range(num_cams[0]):
        for ix in range(num_cams[1]):
            # rendering
            if (not iy*10+ix < resume_point[0]*10+resume_point[1]) \
                and (not iy*10+ix > end_point[0]*10+end_point[1]):
                print('rendering:', iy, ix)
                register_output_dir(output_dir + '/{}x{}_baseline{}/{:02d}_{:02d}/'.format(num_cams[1], num_cams[0], baseline, iy, ix))
                bpy.ops.render.render(animation=True)
            move_along_local_axis(camera, (baseline, 0, 0))
        move_along_local_axis(camera, (-num_cams[0] * baseline, 0, 0))
        move_along_local_axis(camera, (0, -baseline, 0))
    camera.location = init_location

capture_light_field(camera=scene.camera, num_cams=(9, 9), baseline=0.05, resume_point=(0, 0))