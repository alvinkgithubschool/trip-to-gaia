import bpy,os,time,json
out=os.path.dirname(bpy.data.filepath);os.makedirs(out+'/previews',exist_ok=True);report=[]
for name in ('Gaia_Desert','Gaia_Ocean'):
 s=bpy.data.scenes[name];bpy.context.window.scene=s
 for f in (1,120,240):
  s.frame_set(f);s.render.filepath=f'{out}/previews/{name}_{f:03}.png';start=time.perf_counter();bpy.ops.render.render(write_still=True,scene=name);report.append(dict(scene=name,frame=f,seconds=time.perf_counter()-start))
  open(out+'/render_report.json','w').write(json.dumps(report,indent=2))
