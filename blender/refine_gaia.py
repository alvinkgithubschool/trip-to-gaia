import bpy
for name in ('Gaia_Desert','Gaia_Ocean'):
 s=bpy.data.scenes[name];s.camera.data.clip_end=20000
 surf=next(o for o in s.objects if 'surface' in o.name)
 mod=surf.modifiers.new('Smooth sampled surface','SUBSURF');mod.levels=1;mod.render_levels=1
 m=surf.data.materials[0]
 if name.endswith('Desert'):
  for n in m.node_tree.nodes:
   if n.type=='BUMP':n.inputs['Strength'].default_value=.045;n.inputs['Distance'].default_value=.003
 mesh=bpy.data.meshes.new(name+' distant horizon');z=-65 if name.endswith('Desert') else -2.1
 mesh.from_pydata([(-15000,-15000,z),(15000,-15000,z),(15000,15000,z),(-15000,15000,z)],[],[(0,1,2,3)]);o=bpy.data.objects.new(mesh.name,mesh);s.collection.objects.link(o);mesh.materials.append(m)
 for o in s.objects:
  if o.type=='MESH' and o.name.startswith('Visitor'):
   o.data.materials[0].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=30
 s.frame_set(120)
