"""Lighting, local haze and baked shared camera tracking. Safe to reapply."""
import bpy, math
from mathutils import Vector
scenes=[bpy.data.scenes[n] for n in ('Gaia_Desert','Gaia_Ocean')]
cam=scenes[0].camera
cam.data.animation_data_clear();cam.animation_data_clear()
cam.data.lens=18;cam.data.shift_x=0;cam.data.shift_y=0
cam.data.dof.use_dof=False
# Keep forward/lateral flight on the existing parent. Add a modest floating offset
# and track the visitors with a low-pass filtered aim to avoid jerky corrections.
aim=None
for f in range(1,241):
 t=(f-1)/24
 p1=Vector((math.sin(math.sin(t*.2)+t*.4)*4,14+math.cos(t*.5)*8,2.5+math.sin(math.sin(t*1.3)+t*.2)*2+math.sin(t*1.7)*.12))
 p2=Vector((math.cos(t*.34)*3,18+math.sin(t*.4)*5,2.5+math.sin(t*.8)*1.6+math.sin(t*1.7+1)*.12))
 target=(p1+p2)*.5;target.z-=.55+math.sin(t*.85)*.09+math.sin(t*1.6)*.035
 # Lower the aim to retain the landscape; visitors occupy upper middle frame.
 target.z-=.5
 aim=target if aim is None else aim.lerp(target,.09)
 cam.location=(math.sin(t*.48)*.28,0,math.sin(t*.7)*.055)
 cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
for s in scenes:
 desert=s.name.endswith('Desert');bpy.context.window.scene=s
 s.view_settings.view_transform='AgX';s.view_settings.exposure=-.35 if desert else -.4
 bg=s.world.node_tree.nodes.get('Background')
 if desert:
  sky=next(n for n in s.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_elevation=.065;sky.sun_rotation=-.65;sky.air_density=1.8;bg.inputs['Strength'].default_value=.22
 else:
  # Directional twilight gradient: navy zenith, muted lavender horizon.
  tree=s.world.node_tree
  for link in list(bg.inputs['Color'].links):tree.links.remove(link)
  tex=tree.nodes.new('ShaderNodeTexCoord');sep=tree.nodes.new('ShaderNodeSeparateXYZ');ramp=tree.nodes.new('ShaderNodeValToRGB')
  tree.links.new(tex.outputs['Normal'],sep.inputs[0]);tree.links.new(sep.outputs['Z'],ramp.inputs[0]);tree.links.new(ramp.outputs['Color'],bg.inputs['Color'])
  ramp.color_ramp.elements[0].position=0;ramp.color_ramp.elements[0].color=(.16,.13,.20,1)
  ramp.color_ramp.elements[1].position=.65;ramp.color_ramp.elements[1].color=(.009,.025,.075,1);bg.inputs['Strength'].default_value=.65
 for o in s.objects:
  if o.type=='LIGHT':
   if o.data.type=='SUN':
    o.data.energy=1.5 if desert else .65;o.data.color=(1,.50,.22) if desert else (.36,.55,1);o.data.angle=.12;o.rotation_euler=(1.49,-.25,-.65)
   elif o.data.type=='POINT':o.data.energy=260;o.data.color=(1,.32,.08)
 # Bounded mist avoids infinite world-volume extinction.
 name=s.name+' atmospheric haze';haze=bpy.data.objects.get(name)
 if haze is None:
  bpy.ops.mesh.primitive_cube_add(size=2,location=(-65,170,20));haze=bpy.context.object;haze.name=name;haze.scale=(400,550,110);haze.display_type='WIRE'
  m=bpy.data.materials.new(name);m.use_nodes=True;tree=m.node_tree;tree.nodes.clear();out=tree.nodes.new('ShaderNodeOutputMaterial');vol=tree.nodes.new('ShaderNodeVolumePrincipled');tree.links.new(vol.outputs['Volume'],out.inputs['Volume']);haze.data.materials.append(m)
 haze.scale=(400,550,1000)
 vol=next(n for n in haze.data.materials[0].node_tree.nodes if n.type=='PRINCIPLED_VOLUME');vol.inputs['Density'].default_value=.0018 if desert else .0009;vol.inputs['Color'].default_value=(.75,.47,.24,1) if desert else (.32,.45,.65,1);vol.inputs['Anisotropy'].default_value=.25
 gl=next(n for n in s.compositing_node_group.nodes if n.type=='GLARE');gl.inputs['Threshold'].default_value=1.3;gl.inputs['Strength'].default_value=.25
 s.frame_set(120)
bpy.context.window.scene=scenes[0]
