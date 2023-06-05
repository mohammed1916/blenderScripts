import bpy
import random

# Clear existing objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Set up scene
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 250

# Create start_basket
start_basket = bpy.ops.mesh.primitive_cube_add(size=1)
start_basket_obj = bpy.context.active_object
start_basket_obj.location = (0, 0, 0)
start_basket_obj.name = 'Start Basket'

# Create target_buckets
bucket_locations = [(2, 2, 0), (-2, 2, 0), (2, -2, 0)]
target_buckets = []
for i, location in enumerate(bucket_locations):
    bpy.ops.mesh.primitive_cube_add(size=1)
    bucket_obj = bpy.context.active_object
    bucket_obj.location = location
    bucket_obj.name = f'Target Bucket {i+1}'
    target_buckets.append(bucket_obj)

# Create balls
ball_colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]
ball_count = 3

for i in range(ball_count):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = 3 + i * 2
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(x, y, z))
    ball_obj = bpy.context.active_object
    ball_obj.name = f'Ball {i+1}'
    ball_material = bpy.data.materials.new(name=f'Ball {i+1} Material')
    ball_material.diffuse_color = ball_colors[i]
    ball_obj.data.materials.append(ball_material)

# Create animation
for frame in range(scene.frame_start, scene.frame_end + 1):
    scene.frame_set(frame)
    for i, ball_obj in enumerate(target_buckets):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = ball_obj
        ball_obj.select_set(True)
        bpy.ops.object.origin_set(
            type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

        ball = bpy.data.objects[f'Ball {i+1}']
        ball.location.z -= 0.05
        ball.keyframe_insert(data_path='location', frame=frame)

bpy.ops.screen.animation_play()
