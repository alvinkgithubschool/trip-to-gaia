"""Run with Blender --background --python build_gaia.py. Add -- --previews to render checks."""
import bpy, math, os, time, json, sys
import numpy as np
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__))
# Never delete existing user scenes. Rebuild in a fresh Blender session for exact names.
if any(n in bpy.data.scenes for n in ('Gaia_Desert','Gaia_Ocean')):
    raise RuntimeError('Gaia scenes already exist; run in a fresh Blender session.')
def obj(scene,name,data):
    o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);return o
def mat(name,color,rough=.5,metal=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m,p
def waves(x,y,t,n=24):
    x=x*.1+t*.1;y=y*.1+t*.1;phase=6.;speed=2.;weight=1.;w=np.zeros_like(x);ws=0
    for i in range(n):
        dx,dy=math.sin(i*12),math.cos(i*12);a=(dx*x+dy*y)*phase+t*speed;v=np.exp(np.sin(a)-1)
        x=x-dx*v*np.cos(a)*weight*.058;y=y-dy*v*np.cos(a)*weight*.058
        w+=v*weight;ws+=weight;weight*=.8;phase*=1.18;speed*=1.07
    return w/ws*2.1-2.1
def desert(x,y):
    lo=np.full_like(x,-100.);hi=np.full_like(x,2.)
    for _ in range(25):
        z=(lo+hi)/2;px=x.copy();py=z.copy();pz=y.copy();f=.02
        for j in range(7):
            d=np.abs((np.sin(px*f)+np.sin(py*f)+np.sin(pz*f))*.12)/f;px+=d;py+=d;pz+=d;f*=2
        above=1+py*.6>0;hi=np.where(above,z,hi);lo=np.where(above,lo,z)
    return (hi+lo)/2
scenes=[]
rig=bpy.data.objects.new('Gaia shared flight rig',None)
camdata=bpy.data.cameras.new('Gaia camera');camdata.type='PERSP';camdata.lens=10.125;camdata.sensor_width=36
cam=bpy.data.objects.new('Gaia camera',camdata);cam.parent=rig
orbs=[]
for i in range(2):
    # Operator creates sphere, then unlink from original scene to preserve its contents.
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=(.1,.14)[i]);o=bpy.context.object;o.name='Visitor '+str(i+1)
    for c in list(o.users_collection):c.objects.unlink(o)
    m,p=mat(o.name+' amber',(1,.4,.2));p.inputs['Emission Color'].default_value=(1,.4,.2,1);p.inputs['Emission Strength'].default_value=8;o.data.materials.append(m)
    for poly in o.data.polygons:poly.use_smooth=True
    l=bpy.data.lights.new(o.name+' glow','POINT');l.energy=180;l.color=(1,.4,.15);l.shadow_soft_size=.18
    lamp=bpy.data.objects.new(l.name,l);lamp.parent=o;orbs.append((o,lamp))
for f in range(1,241):
    t=(f-1)/24;rig.location=(-13*t,12*t,.55+math.sin(t*.85)*.09+math.sin(t*1.6)*.035);rig.keyframe_insert('location',frame=f)
    # Shader off-axis sway, represented exactly with camera lens shifts.
    cam.rotation_euler=(math.pi/2,0,0);camdata.shift_x=math.cos(t*.3)*.4/(2*1280/720);camdata.shift_y=math.cos(t*.3)*.2/(2*1280/720)
    camdata.keyframe_insert('shift_x',frame=f);camdata.keyframe_insert('shift_y',frame=f)
    positions=[(math.sin(math.sin(t*.2)+t*.4)*4,14+t*12+math.cos(t*.5)*8,2.5+math.sin(math.sin(t*1.3)+t*.2)*2+math.sin(t*1.7)*.12),(math.cos(t*.34)*3,18+t*12+math.sin(t*.4)*5,2.5+math.sin(t*.8)*1.6+math.sin(t*1.7+1)*.12)]
    for (o,l),(x,y,z) in zip(orbs,positions):o.location=(x-13*t,y,z);o.keyframe_insert('location',frame=f)
for kind in ('Desert','Ocean'):
    s=bpy.data.scenes.new('Gaia_'+kind);scenes.append(s);s.collection.objects.link(rig);s.collection.objects.link(cam)
    for o,l in orbs:s.collection.objects.link(o);s.collection.objects.link(l)
    s.camera=cam;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=240
    s.eevee.taa_render_samples=48;s.eevee.use_raytracing=True
    s.world=bpy.data.worlds.new(kind+' sky');s.world.use_nodes=True
    ns=s.world.node_tree.nodes;ls=s.world.node_tree.links;bg=ns.get('Background');bg.inputs['Strength'].default_value=.35
    sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=.12;sky.sun_rotation=-.65;sky.altitude=.1;sky.air_density=1.4;ls.new(sky.outputs[0],bg.inputs[0])
    sun=bpy.data.lights.new(kind+' sun','SUN');sun.energy=2 if kind=='Desert' else .7;sun.angle=.08;sun.color=(1,.65,.35);o=obj(s,sun.name,sun);o.rotation_euler=(1.43,-.3,-.65)
    # Single connected grid: no tile boundaries. Concentrate sampling along the flight corridor.
    xs=np.linspace(-330,200,531);ys=np.concatenate([np.linspace(-45,240,571),np.linspace(242,850,100)])
    X,Y=np.meshgrid(xs,ys);x=X.ravel();y=Y.ravel();z=desert(x,y) if kind=='Desert' else waves(x,y,0)
    verts=np.stack([x,y,z],axis=1);nx=len(xs);ny=len(ys);idx=np.arange((ny-1)*nx).reshape(ny-1,nx)[:,:-1].ravel();faces=np.stack([idx,idx+1,idx+1+nx,idx+nx],axis=1)
    mesh=bpy.data.meshes.new(kind+' procedural surface');mesh.from_pydata(verts.tolist(),[],faces.tolist());mesh.update();surface=obj(s,kind+' surface',mesh)
    for p in mesh.polygons:p.use_smooth=True
    if kind=='Desert':
        m,p=mat('Warm sand',(.55,.25,.08),.85)
        n=m.node_tree.nodes;l=m.node_tree.links;noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=180
        bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.015;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
        wave=n.new('ShaderNodeTexWave');wave.inputs['Scale'].default_value=21;wave.inputs['Distortion'].default_value=3
        b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.15;b.inputs['Distance'].default_value=.025;l.new(wave.outputs[0],b.inputs['Height']);l.new(bump.outputs[0],b.inputs['Normal']);l.new(b.outputs[0],p.inputs['Normal'])
    else:
        m,p=mat('Reflective teal water',(.01,.10,.14),.12,.25)
        n=m.node_tree.nodes;l=m.node_tree.links;geom=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geom.outputs['Position'],sep.inputs[0]);r=n.new('ShaderNodeMapRange');r.inputs['From Min'].default_value=-1.05;r.inputs['From Max'].default_value=-.55;l.new(sep.outputs['Z'],r.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=8
        mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(r.outputs[0],mul.inputs[0]);l.new(noise.outputs['Fac'],mul.inputs[1]);mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.01,.10,.14,1);mix.inputs[2].default_value=(.88,.94,.96,1);l.new(mul.outputs[0],mix.inputs[0]);l.new(mix.outputs[0],p.inputs['Base Color'])
        surface.shape_key_add(name='Basis')
        # Baked 6 Hz samples, interpolated by shape keys; fully portable without handlers.
        for f in list(range(1,241,4))+[240]:
            t=(f-1)/24;h=waves(x,y,t,18);v=np.stack([x,y,h],axis=1).astype(np.float32)
            key=surface.shape_key_add(name='wave_%03d'%f);key.data.foreach_set('co',v.ravel());key.value=0;key.keyframe_insert('value',frame=max(-3,f-4));key.value=1;key.keyframe_insert('value',frame=f);key.value=0;key.keyframe_insert('value',frame=f+4 if f!=237 else 240)
    surface.data.materials.append(m)
    tree=bpy.data.node_groups.new(kind+' compositor','CompositorNodeTree');s.compositing_node_group=tree;rl=tree.nodes.new('CompositorNodeRLayers');rl.scene=s;gl=tree.nodes.new('CompositorNodeGlare');gl.inputs['Type'].default_value='Fog Glow';gl.inputs['Threshold'].default_value=2;gl.inputs['Strength'].default_value=.15;tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');out=tree.nodes.new('NodeGroupOutput');tree.links.new(rl.outputs['Image'],gl.inputs['Image']);tree.links.new(gl.outputs['Image'],out.inputs[0]);s.frame_set(120)
exec(compile(open(os.path.join(OUT,'refine_gaia.py')).read(),'refine_gaia.py','exec'))
exec(compile(open(os.path.join(OUT,'cinematic_gaia.py')).read(),'cinematic_gaia.py','exec'), {})
bpy.context.window.scene=scenes[0]
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Trip_to_Gaia.blend'),compress=True)
if '--previews' in sys.argv:
    report=[]
    os.makedirs(os.path.join(OUT,'previews'),exist_ok=True)
    for s in scenes:
        for f in (1,120,240):
            s.frame_set(f);s.render.filepath=os.path.join(OUT,'previews',s.name+'_%03d.png'%f);start=time.perf_counter();bpy.ops.render.render(write_still=True,scene=s.name);report.append({'scene':s.name,'frame':f,'seconds':time.perf_counter()-start})
    with open(os.path.join(OUT,'render_report.json'),'w') as h:json.dump(report,h,indent=2)
