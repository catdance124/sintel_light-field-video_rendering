"""
work notes
1. Turns off transparency for all objects.
2. Collapses the scene into a single render layer (turns off halo).

After running this script, manually 
    edit the node network (press A -> X (delete all nodes), shift+A(add node))
"""

import bpy 


scene = bpy.context.scene
scene.render.resolution_x = 1024
scene.render.resolution_y = 436
scene.render.resolution_percentage = 100
scene.render.antialiasing_samples = '5'
scene.render.color_mode = 'RGB'

# 1. Turns off transparency for all objects.
for mat in bpy.data.materials:
    if mat.alpha < 1:
        print(mat.name)
        if not 'eye' in mat.name:
            mat.alpha = 1.0
        for ts in mat.texture_slots:
            if ts is not None:
                ts.map_alpha = False

# 2. Collapses the scene into a single render layer (turns off halo).
for render_layer in scene.render.layers:
    render_layer.enabled = False
bpy.ops.scene.render_layer_add()
scene.render.layers[-1].visible_layers = scene.layers
scene.render.layers[-1].name = 'collapse_layer'
scene.render.layers[-1].halo = False

# edit the node network (press A -> X (delete all nodes), shift+A(add node))