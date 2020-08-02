import bpy
print(bpy.context.scene.camera.name)
for i,camera in enumerate(bpy.data.cameras):
    print(i, camera.name ,camera.lens, camera.lens_unit)
    