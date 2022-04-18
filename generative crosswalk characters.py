import bpy
import random
import time
import mathutils
import math

from math import *
from mathutils import Vector
import os

# clears all objects
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)

for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)

for block in bpy.data.textures:
    if block.users == 0:
        bpy.data.textures.remove(block)

for block in bpy.data.images:
    if block.users == 0:
        bpy.data.images.remove(block)
        
for block in bpy.data.armatures:
    if block.users == 0:
        bpy.data.armatures.remove(block)
        
for block in bpy.data.actions:
    if block.users == 0:
        bpy.data.actions.remove(block)
        
for block in bpy.data.lights:
    if block.users == 0:
        bpy.data.lights.remove(block)

for block in bpy.data.cameras:
    if block.users == 0:
        bpy.data.cameras.remove(block)
        
# clears old collections
old = bpy.data.collections.get("cubes")
bpy.data.collections.remove(collection = old)
old = bpy.data.collections.get("cubes2")
bpy.data.collections.remove(collection = old)

# creates collections
collection = bpy.context.blend_data.collections.new(name='cubes')
bpy.context.collection.children.link(collection)
collection = bpy.context.blend_data.collections.new(name='cubes2')
bpy.context.collection.children.link(collection)

# basic primitive cube grid inputs
dim = 1
spacing = dim * 2.6
rAndC = 5

current_scene = bpy.context.scene

#default_cube = current_scene.objects['default_cube']

count = 0

total_time = 10
fps = 24
keyframe_freq = 20

distanceBetween = rAndC*10

#bpy.ops.mesh.primitive_plane_add(size=1000, enter_editmode=False, align='WORLD', location=(distanceBetween/2, distanceBetween/2, -0.001), scale=(1, 1, 1))

# bring in the street
bpy.ops.wm.append(
            filepath='background.blend',
            directory='D:/Documents/blendr/background.blend/Collection',
            filename='Collection'
            )
            
roadLoc = distanceBetween/2 + ((rAndC - 1) * spacing)/2
roadDim = distanceBetween + (rAndC - 1) * spacing    


bpy.ops.transform.resize(value = (roadDim, roadDim, 1))
bpy.ops.transform.translate(value = (roadLoc, roadLoc, 0))
            
g = bpy.context.selected_objects
bpy.ops.collection.objects_remove_all()
for i in range(len(g)):
    bpy.data.collections['cubes2'].objects.link(g[i])
#            g[i].animation_data_clear() 
old = bpy.data.collections.get("Collection")
bpy.data.collections.remove(collection = old)

# materials
cloudMat = bpy.data.materials.new(name="CloudMat")
cloudMat.use_nodes = True
cloudsNodes = cloudMat.node_tree.nodes
clou = cloudsNodes.new('ShaderNodeTexImage')
clou.image = bpy.data.images.load(filepath = 'C:/Users/Taehwan/Desktop/blender/generative walking cross/gettyimages-1160178301-170667a.jpg')
cloudMat.node_tree.links.new(cloudsNodes['Principled BSDF'].inputs[0], clou.outputs[0])

buildingMat = bpy.data.materials.new(name="BuildingMat")
buildingMat.use_nodes = True
princ = buildingMat.node_tree.nodes.get('Principled BSDF')
princ.inputs[0].default_value = (0.05, 0.05, 0.05, 1)

winMat = bpy.data.materials.new(name="WindowMat")
winMat.use_nodes = True
princ = winMat.node_tree.nodes.get('Principled BSDF')
princ.inputs[0].default_value = (0.733262, 0.8, 0, 1)

# cloud background
camZ = 4.7
zLoc = (math.tan(radians(18.893)) * 42 * roadLoc + camZ) / 2
yScale = math.tan(radians(31.13)) * 42 * roadLoc * 2
bpy.ops.mesh.primitive_plane_add(size = 1, location = (-roadLoc*38, roadLoc, zLoc), rotation = (-3 * pi/2, 0, -pi/2))
bpy.context.object.active_material = cloudMat
bpy.ops.transform.resize(value = (1, yScale, zLoc*2))

# camera setup
cam = bpy.data.cameras.new("Main Cam")
cam.lens = 31
cam.clip_end = roadLoc*(38+5)
cam_obj = bpy.data.objects.new("Main Cam", cam)
cam_obj.location = (roadLoc*4, roadLoc, camZ + camZ*0.55*(rAndC-2))
cam_obj.rotation_euler = (radians(90),0, pi/2)
current_scene.collection.objects.link(cam_obj)


# create light datablock
light_data = bpy.data.lights.new(name="my-light-data", type='AREA')
light_data.energy = 1000
# create new object, pass the light data 
light_obj = bpy.data.objects.new(name="my-light", object_data=light_data)
# link object to collection in context
bpy.context.collection.objects.link(light_obj)
#  change light position
light_obj.location = (-roadLoc*38 + 10, roadLoc, zLoc)
light_obj.rotation_euler = (0, pi/2, 0)
light_obj.scale = (zLoc*8, yScale*4 ,1)

# this imports the models - currently up to 1000. Can easily add more if you want, just have to change the if statement.
for x in range(rAndC):
    for y in range(rAndC):
        
        xloc = x * spacing
        yloc = y * spacing
        
        location = (xloc, yloc, 0)
        
        bpy.ops.wm.append(
            filepath='character 3.1.blend',
            directory='D:/Documents/blendr/character 3.1.blend/Collection',
            filename='Collection'
            )
        
        bpy.ops.transform.translate(value = location)
        bpy.ops.transform.rotate(value = 45)

        g = bpy.context.selected_objects
        bpy.ops.collection.objects_remove_all()
        for i in range(len(g)):
            bpy.data.collections['cubes'].objects.link(g[i])
#            g[i].animation_data_clear() 
        old = bpy.data.collections.get("Collection")
        bpy.data.collections.remove(collection = old)
        
        
        #animation  
        bpy.context.scene.frame_start = 0
        bpy.context.scene.frame_end = int(total_time * fps) + 1

        nlast = bpy.context.scene.frame_end

        if count == 0:
            arm = bpy.data.objects["Armature"]
        elif 100 > count >= 10:
            arm = bpy.data.objects["Armature.0" + str(count)]
        elif 1000 > count >= 100:
            arm = bpy.data.objects["Armature." + str(count)]
        else:
            arm = bpy.data.objects["Armature.00" + str(count)]
        count += 1
        
        #Making keyframes for the animation
        arm.select_set(True)    
        bpy.context.view_layer.objects.active = arm
        xloc = arm.location.x    
        yloc = arm.location.y    
        zloc = arm.location.z 
        for n in range(nlast):
            
            t = total_time*n/nlast

            if n%keyframe_freq == 0:
                if n == 0:
                    xlocFrame = xloc
                    ylocFrame = yloc
                else:
                    timestamp = n / 24                
                    xlocFrame = xloc + distanceBetween * timestamp / total_time
                    ylocFrame = yloc + distanceBetween * timestamp / total_time

                # Set frame
                bpy.context.scene.frame_set(n)

                # Set location
                arm.location.x = xlocFrame
                arm.location.y = ylocFrame
                # Insert new keyframe for location
                arm.keyframe_insert(data_path="location")
        
#Other array of models
for x in range(rAndC):
    for y in range(rAndC):
        
#        xloc = x * spacing
        xloc = x * spacing - spacing/2
        yloc = y * spacing + distanceBetween
        
        location = (xloc, yloc, 0)

        bpy.ops.wm.append(
            filepath='character 3.1.blend',
            directory='D:/Documents/blendr/character 3.1.blend/Collection',
            filename='Collection'
            )
            
        bpy.ops.transform.translate(value = location)
        bpy.ops.transform.rotate(value = 90)

        g = bpy.context.selected_objects
        bpy.ops.collection.objects_remove_all()
        for i in range(len(g)):
            bpy.data.collections['cubes'].objects.link(g[i])
#            g[i].animation_data_clear() 
        old = bpy.data.collections.get("Collection")
        bpy.data.collections.remove(collection = old)
        
        #animation
#        item.animation_data_clear()        
        bpy.context.scene.frame_start = 0
        bpy.context.scene.frame_end = int(total_time * fps) + 1

        nlast = bpy.context.scene.frame_end
        
        if count == 0:
            arm = bpy.data.objects["Armature"]
        elif 100 > count >= 10:
            arm = bpy.data.objects["Armature.0" + str(count)]
        elif 1000 > count >= 100:
            arm = bpy.data.objects["Armature." + str(count)]
        else:
            arm = bpy.data.objects["Armature.00" + str(count)]
        count += 1
            
        arm.select_set(True)    
        bpy.context.view_layer.objects.active = arm
        xloc = arm.location.x    
        yloc = arm.location.y    
        zloc = arm.location.z 
        for n in range(nlast):
            
            t = total_time*n/nlast

            if n%keyframe_freq == 0:
                if n == 0:
                    xlocFrame = xloc
                    ylocFrame = yloc
                else:
                    timestamp = n / 24                
                    xlocFrame = xloc + distanceBetween * timestamp / total_time
                    ylocFrame = yloc - distanceBetween * timestamp / total_time

                # Set frame
                bpy.context.scene.frame_set(n)

                # Set location
                arm.location.x = xlocFrame
                arm.location.y = ylocFrame
                # Insert new keyframe for location
                arm.keyframe_insert(data_path="location")
                
#basic primitive cube grid
spacing = 2.2
sizeCube = rAndC * 5
cubeCount = 2
#alley should be about 37 to reach the clouds
alley = 40



for x in range(alley):
    for y in range(cubeCount):
        if random.random() < 0.02:
            zScale = random.randint(10, 15)
        else:
            zScale = random.randint(1, 4)
#        zScale = 4
        location = (-(x * spacing * (sizeCube / 2) + sizeCube / 2 + 0.33 * roadDim), -(y * spacing * (sizeCube / 2) + sizeCube / 2 + 0.33 * roadDim), (zScale *sizeCube) / 2)            
        bpy.ops.mesh.primitive_cube_add(size=sizeCube, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, zScale))
        
        item = bpy.context.object
        bpy.context.object.active_material = buildingMat

        for j in range(0, 4, 1):
            w = 0.2
            h = 0.1
            t = 0.01
            if j == 0:
                windowLoc = (location[0] - sizeCube / 2 + w * sizeCube, location[1] - sizeCube / 2, sizeCube / 5 * 2.5)
                Scale = (w, t, h)
            elif j == 1:
                windowLoc = (location[0] - sizeCube / 2 + w * sizeCube, location[1] + sizeCube / 2, sizeCube / 5 * 2.5)
                Scale = (w, t, h)
            elif j == 2:
                windowLoc = (location[0] - sizeCube / 2, location[1] - sizeCube / 2 + w * sizeCube, sizeCube / 5 * 2.5)
                Scale = (t, w, h)
            elif j == 3:
                windowLoc = (location[0] + sizeCube / 2, location[1] - sizeCube / 2 + w * sizeCube, sizeCube / 5 * 2.5)
                Scale = (t, w, h)
            
            column = 3
            columnSpacing = 1.5

            rowSpacing = 4
            row = round(zScale / rowSpacing / h) - 1

            bpy.ops.mesh.primitive_cube_add(size=sizeCube, enter_editmode=False, align='WORLD', location=windowLoc, scale=Scale)
            bpy.context.object.modifiers.new(name = 'row', type = 'ARRAY')
            bpy.context.object.active_material = winMat
            #bpy.context.object.modifiers["row"].use_constant_offset = True
            bpy.context.object.modifiers["row"].use_relative_offset = True
            bpy.context.object.modifiers["row"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["row"].relative_offset_displace[2] = rowSpacing
            bpy.context.object.modifiers["row"].count = row

            bpy.context.object.modifiers.new(name = 'column', type = 'ARRAY')
            #bpy.context.object.modifiers["column"].use_constant_offset = True
            bpy.context.object.modifiers["column"].use_relative_offset = True
            if j <= 1:
                bpy.context.object.modifiers["column"].relative_offset_displace[0] = columnSpacing
            else:
                bpy.context.object.modifiers["column"].relative_offset_displace[0] = 0
                bpy.context.object.modifiers["column"].relative_offset_displace[1] = columnSpacing
            bpy.context.object.modifiers["column"].count = column

            #g = bpy.context.selected_objects
            #bpy.ops.collection.objects_remove_all()
            #bpy.data.collections['windows'].objects.link(g)

            bpy.ops.object.modifier_apply(modifier="row")
            bpy.ops.object.modifier_apply(modifier="column")
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

            g = bpy.context.selected_objects
            for i in range(len(g)):
                imDumb = random.random()
                if imDumb < 0.2:
                    bpy.data.objects.remove(g[i])
                    continue
                elif imDumb < 0.8:
                    g[i].scale.z = random.uniform(1.5, 4)
                elif imDumb > 0.98:
                    g[i].scale.z = 0.3
                if g[i].location[2] + g[i].scale.z / 2 > (zScale * sizeCube):
                    bpy.data.objects.remove(g[i])
                    continue
               
                imDumber = random.random()   
                if j <= 1:
                        if imDumber < 0.4:
                            ry = 0
                            continue
                        elif imDumber < 0.7:
                            ry = random.uniform(0, 1) * pi / 12
                        elif imDumber < 1:
                            ry = - random.uniform(0, 1) * pi / 12
                        g[i].rotation_euler = (0, ry, 0)
                else:    
                        if imDumber < 0.4:
                            rx = 0
                            continue
                        elif imDumber < 0.7:
                            rx = random.uniform(0, 1) * pi / 12
                        elif imDumber < 1:
                            rx = - random.uniform(0, 1) * pi / 12
                        g[i].rotation_euler = (rx, 0, 0)       
    


cubeCount = 2
        
for x in range(cubeCount):
    for y in range(cubeCount):
        if random.random() < 0.02:
            zScale = random.randint(10, 15)
        else:
            zScale = random.randint(1, 4)
        location = ((x * spacing * (sizeCube / 2) + sizeCube / 2 + 0.33 * roadDim) + roadDim, -(y * spacing * (sizeCube / 2) + sizeCube / 2 + 0.33 * roadDim), (zScale *sizeCube) / 2)            
        bpy.ops.mesh.primitive_cube_add(size=sizeCube, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, zScale))
        
        item = bpy.context.object
        bpy.context.object.active_material = buildingMat
        
        for j in range(0, 4, 1):
            w = 0.2
            h = 0.1
            t = 0.01
            if j == 0:
                windowLoc = (location[0] - sizeCube / 2 + w * sizeCube, location[1] - sizeCube / 2, sizeCube / 5 * 2.5)
                Scale = (w, t, h)
            elif j == 1:
                windowLoc = (location[0] - sizeCube / 2 + w * sizeCube, location[1] + sizeCube / 2, sizeCube / 5 * 2.5)
                Scale = (w, t, h)
            elif j == 2:
                windowLoc = (location[0] - sizeCube / 2, location[1] - sizeCube / 2 + w * sizeCube, sizeCube / 5 * 2.5)
                Scale = (t, w, h)
            elif j == 3:
                windowLoc = (location[0] + sizeCube / 2, location[1] - sizeCube / 2 + w * sizeCube, sizeCube / 5 * 2.5)
                Scale = (t, w, h)
            
            column = 3
            columnSpacing = 1.5

            rowSpacing = 4
            row = round(zScale / rowSpacing / h) - 1

            bpy.ops.mesh.primitive_cube_add(size=sizeCube, enter_editmode=False, align='WORLD', location=windowLoc, scale=Scale)
            bpy.context.object.modifiers.new(name = 'row', type = 'ARRAY')
            bpy.context.object.active_material = winMat
            #bpy.context.object.modifiers["row"].use_constant_offset = True
            bpy.context.object.modifiers["row"].use_relative_offset = True
            bpy.context.object.modifiers["row"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["row"].relative_offset_displace[2] = rowSpacing
            bpy.context.object.modifiers["row"].count = row

            bpy.context.object.modifiers.new(name = 'column', type = 'ARRAY')
            #bpy.context.object.modifiers["column"].use_constant_offset = True
            bpy.context.object.modifiers["column"].use_relative_offset = True
            if j <= 1:
                bpy.context.object.modifiers["column"].relative_offset_displace[0] = columnSpacing
            else:
                bpy.context.object.modifiers["column"].relative_offset_displace[0] = 0
                bpy.context.object.modifiers["column"].relative_offset_displace[1] = columnSpacing
            bpy.context.object.modifiers["column"].count = column

            #g = bpy.context.selected_objects
            #bpy.ops.collection.objects_remove_all()
            #bpy.data.collections['windows'].objects.link(g)

            bpy.ops.object.modifier_apply(modifier="row")
            bpy.ops.object.modifier_apply(modifier="column")
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

            g = bpy.context.selected_objects
            for i in range(len(g)):
                imDumb = random.random()
                if imDumb < 0.2:
                    bpy.data.objects.remove(g[i])
                    continue
                elif imDumb < 0.8:
                    g[i].scale.z = random.uniform(1.5, 4)
                elif imDumb > 0.98:
                    g[i].scale.z = 0.3
                if g[i].location[2] + g[i].scale.z / 2 > (zScale * sizeCube):
                    bpy.data.objects.remove(g[i])
                    continue
                 
                imDumber = random.random()   
                if j <= 1:
                        if imDumber < 0.4:
                            ry = 0
                            continue
                        elif imDumber < 0.7:
                            ry = random.uniform(0, 1) * pi / 12
                        elif imDumber < 1:
                            ry = - random.uniform(0, 1) * pi / 12
                        g[i].rotation_euler = (0, ry, 0)
                else:    
                        if imDumber < 0.4:
                            rx = 0
                            continue
                        elif imDumber < 0.7:
                            rx = random.uniform(0, 1) * pi / 12
                        elif imDumber < 1:
                            rx = - random.uniform(0, 1) * pi / 12
                        g[i].rotation_euler = (rx, 0, 0)       
        
        
        
cubeCount = 2       
        
for x in range(alley):
    for y in range(cubeCount):
        if random.random() < 0.02:
            zScale = random.randint(10, 15)
        else:
            zScale = random.randint(1, 4)
        location = (-(x * spacing * (sizeCube / 2) + sizeCube / 2 + 0.33 * roadDim), (y * spacing * (sizeCube / 2) + sizeCube / 2 + 0.33 * roadDim) + roadDim, (zScale *sizeCube) / 2)            
        bpy.ops.mesh.primitive_cube_add(size=sizeCube, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, zScale))
        
        item = bpy.context.object
        bpy.context.object.active_material = buildingMat
        
        for j in range(0, 4, 1):
            w = 0.2
            h = 0.1
            t = 0.01
            if j == 0:
                windowLoc = (location[0] - sizeCube / 2 + w * sizeCube, location[1] - sizeCube / 2, sizeCube / 5 * 2.5)
                Scale = (w, t, h)
            elif j == 1:
                windowLoc = (location[0] - sizeCube / 2 + w * sizeCube, location[1] + sizeCube / 2, sizeCube / 5 * 2.5)
                Scale = (w, t, h)
            elif j == 2:
                windowLoc = (location[0] - sizeCube / 2, location[1] - sizeCube / 2 + w * sizeCube, sizeCube / 5 * 2.5)
                Scale = (t, w, h)
            elif j == 3:
                windowLoc = (location[0] + sizeCube / 2, location[1] - sizeCube / 2 + w * sizeCube, sizeCube / 5 * 2.5)
                Scale = (t, w, h)
            
            column = 3
            columnSpacing = 1.5

            rowSpacing = 4
            row = round(zScale / rowSpacing / h) - 1

            bpy.ops.mesh.primitive_cube_add(size=sizeCube, enter_editmode=False, align='WORLD', location=windowLoc, scale=Scale)
            bpy.context.object.modifiers.new(name = 'row', type = 'ARRAY')
            bpy.context.object.active_material = winMat
            #bpy.context.object.modifiers["row"].use_constant_offset = True
            bpy.context.object.modifiers["row"].use_relative_offset = True
            bpy.context.object.modifiers["row"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["row"].relative_offset_displace[2] = rowSpacing
            bpy.context.object.modifiers["row"].count = row

            bpy.context.object.modifiers.new(name = 'column', type = 'ARRAY')
            #bpy.context.object.modifiers["column"].use_constant_offset = True
            bpy.context.object.modifiers["column"].use_relative_offset = True
            if j <= 1:
                bpy.context.object.modifiers["column"].relative_offset_displace[0] = columnSpacing
            else:
                bpy.context.object.modifiers["column"].relative_offset_displace[0] = 0
                bpy.context.object.modifiers["column"].relative_offset_displace[1] = columnSpacing
            bpy.context.object.modifiers["column"].count = column

            #g = bpy.context.selected_objects
            #bpy.ops.collection.objects_remove_all()
            #bpy.data.collections['windows'].objects.link(g)

            bpy.ops.object.modifier_apply(modifier="row")
            bpy.ops.object.modifier_apply(modifier="column")
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

            g = bpy.context.selected_objects
            for i in range(len(g)):
                imDumb = random.random()
                if imDumb < 0.2:
                    bpy.data.objects.remove(g[i])
                    continue
                elif imDumb < 0.8:
                    g[i].scale.z = random.uniform(1.5, 4)
                elif imDumb > 0.98:
                    g[i].scale.z = 0.3
                if g[i].location[2] + g[i].scale.z / 2 > (zScale * sizeCube):
                    bpy.data.objects.remove(g[i])
                    continue
                 
                imDumber = random.random()   
                if j <= 1:
                        if imDumber < 0.4:
                            ry = 0
                            continue
                        elif imDumber < 0.7:
                            ry = random.uniform(0, 1) * pi / 12
                        elif imDumber < 1:
                            ry = - random.uniform(0, 1) * pi / 12
                        g[i].rotation_euler = (0, ry, 0)
                else:    
                        if imDumber < 0.4:
                            rx = 0
                            continue
                        elif imDumber < 0.7:
                            rx = random.uniform(0, 1) * pi / 12
                        elif imDumber < 1:
                            rx = - random.uniform(0, 1) * pi / 12
                        g[i].rotation_euler = (rx, 0, 0)       

cubeCount = 2       
        
for x in range(cubeCount):
    for y in range(cubeCount):
        if random.random() < 0.02:
            zScale = random.randint(10, 15)
        else:
            zScale = random.randint(1, 4)
        location = ((x * spacing * (sizeCube / 2) + sizeCube / 2 + 0.33 * roadDim) + roadDim, (y * spacing * (sizeCube / 2) + sizeCube / 2 + 0.33 * roadDim) + roadDim, (zScale *sizeCube) / 2)            
        bpy.ops.mesh.primitive_cube_add(size=sizeCube, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, zScale))
        
        item = bpy.context.object
        bpy.context.object.active_material = buildingMat
        
        for j in range(0, 4, 1):
            w = 0.2
            h = 0.1
            t = 0.01
            if j == 0:
                windowLoc = (location[0] - sizeCube / 2 + w * sizeCube, location[1] - sizeCube / 2, sizeCube / 5 * 2.5)
                Scale = (w, t, h)
            elif j == 1:
                windowLoc = (location[0] - sizeCube / 2 + w * sizeCube, location[1] + sizeCube / 2, sizeCube / 5 * 2.5)
                Scale = (w, t, h)
            elif j == 2:
                windowLoc = (location[0] - sizeCube / 2, location[1] - sizeCube / 2 + w * sizeCube, sizeCube / 5 * 2.5)
                Scale = (t, w, h)
            elif j == 3:
                windowLoc = (location[0] + sizeCube / 2, location[1] - sizeCube / 2 + w * sizeCube, sizeCube / 5 * 2.5)
                Scale = (t, w, h)
            
            column = 3
            columnSpacing = 1.5

            rowSpacing = 4
            row = round(zScale / rowSpacing / h) - 1

            bpy.ops.mesh.primitive_cube_add(size=sizeCube, enter_editmode=False, align='WORLD', location=windowLoc, scale=Scale)
            bpy.context.object.modifiers.new(name = 'row', type = 'ARRAY')
            bpy.context.object.active_material = winMat
            #bpy.context.object.modifiers["row"].use_constant_offset = True
            bpy.context.object.modifiers["row"].use_relative_offset = True
            bpy.context.object.modifiers["row"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["row"].relative_offset_displace[2] = rowSpacing
            bpy.context.object.modifiers["row"].count = row

            bpy.context.object.modifiers.new(name = 'column', type = 'ARRAY')
            #bpy.context.object.modifiers["column"].use_constant_offset = True
            bpy.context.object.modifiers["column"].use_relative_offset = True
            if j <= 1:
                bpy.context.object.modifiers["column"].relative_offset_displace[0] = columnSpacing
            else:
                bpy.context.object.modifiers["column"].relative_offset_displace[0] = 0
                bpy.context.object.modifiers["column"].relative_offset_displace[1] = columnSpacing
            bpy.context.object.modifiers["column"].count = column

            #g = bpy.context.selected_objects
            #bpy.ops.collection.objects_remove_all()
            #bpy.data.collections['windows'].objects.link(g)

            bpy.ops.object.modifier_apply(modifier="row")
            bpy.ops.object.modifier_apply(modifier="column")
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

            g = bpy.context.selected_objects
            for i in range(len(g)):
                imDumb = random.random()
                if imDumb < 0.2:
                    bpy.data.objects.remove(g[i])
                    continue
                elif imDumb < 0.8:
                    g[i].scale.z = random.uniform(1.5, 4)
                elif imDumb > 0.98:
                    g[i].scale.z = 0.3
                if g[i].location[2] + g[i].scale.z / 2 > (zScale * sizeCube):
                    bpy.data.objects.remove(g[i])
                    continue
                 
                imDumber = random.random()   
                if j <= 1:
                        if imDumber < 0.4:
                            ry = 0
                            continue
                        elif imDumber < 0.7:
                            ry = random.uniform(0, 1) * pi / 12
                        elif imDumber < 1:
                            ry = - random.uniform(0, 1) * pi / 12
                        g[i].rotation_euler = (0, ry, 0)
                else:    
                        if imDumber < 0.4:
                            rx = 0
                            continue
                        elif imDumber < 0.7:
                            rx = random.uniform(0, 1) * pi / 12
                        elif imDumber < 1:
                            rx = - random.uniform(0, 1) * pi / 12
                        g[i].rotation_euler = (rx, 0, 0)      

