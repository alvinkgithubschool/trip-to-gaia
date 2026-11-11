#version 120
uniform float iTime;
uniform vec2 iResolution;
uniform int scene;

uniform int quality;
vec3 orbCenter(int id){
 float t=iTime;
 if(id==0)return vec3(sin(sin(t*.2)+t*.4)*4.,sin(sin(t*1.3)+t*.2)*2.,14.+t*12.+cos(t*.5)*8.);
 return vec3(cos(t*.34)*3.,sin(t*.8)*1.6,18.+t*12.+sin(t*.4)*5.);
}
float orbRadius(int id){return id==0?.1:.14;}
vec3 orbColor(){return vec3(5.,2.,1.);}
// Desert adapted from the MIT-licensed shader supplied with the project:
// https://www.shadertoy.com/view/3cXyzB
vec3 desert(vec2 uv){
 float d=0.,s=0.,e=1.,brightness=0.;
 float t=iTime,zt=t*12.,xt=t*13.;
 uv+=cos(t*.3)*vec2(.4,.2);
 for(int i=0;i<128;i++){
  vec3 p=vec3(uv*d,d+zt);
  e=min(length(p-orbCenter(0))-orbRadius(0),length(p-orbCenter(1))-orbRadius(1));
  p.x-=xt;
  float frequency=.02;
  for(int j=0;j<7;j++){
   p+=abs(dot(sin(p*frequency),vec3(.12)))/frequency;
   frequency*=2.;
  }
  s=max(.005,min(e,min(1.+p.y*.6,5.-p.y*.05)));
  d+=s;brightness+=s+3./max(abs(e),.025);
 }
 uv+=uv.yx*.7+.2-vec2(-1.,.1);
 vec3 x=vec3(5.,2.,1.)*brightness*brightness/max(d, .01)/1000./max(length(uv),.08);
 return 1.-2./(exp(2.*min(x,vec3(20.)))+1.);
}
// Wave model adapted from afl_ext 2024, public domain, supplied by user.
// https://www.shadertoy.com/view/M3fGDl
float waves(vec2 position,int iterations){
 position=position*.1+iTime*.1;
 float phase=6.,speed=2.,weight=1.,w=0.,ws=0.;
 for(int i=0;i<37;i++){
  if(i>=iterations)break;
  float angle=float(i)*12.;vec2 direction=vec2(sin(angle),cos(angle));
  float x=dot(direction,position)*phase+iTime*speed;
  float wave=exp(sin(x)-1.);
  position-=direction*wave*cos(x)*weight*.058;
  w+=wave*weight;ws+=weight;weight*=.8;phase*=1.18;speed*=1.07;
 }
 return w/ws*2.1-2.1;
}
vec3 skyColor(vec3 ray){
 vec3 sunDir=normalize(vec3(.8,.12,1.));
 float sun=max(dot(ray,sunDir),0.);
 return mix(vec3(.06,.15,.28),vec3(.55,.36,.22),exp(-abs(ray.y)*5.))
       +vec3(1.,.65,.3)*pow(sun,64.)*.5+vec3(8.,5.,2.)*pow(sun,1228.);
}
// Physical spheres and inverse-square halos use the same world positions as desert.
vec3 orbEmission(vec3 origin,vec3 ray,float limit){
 vec3 result=vec3(0.);
 for(int j=0;j<2;j++){
  vec3 delta=orbCenter(j)-origin;float along=dot(delta,ray);
  if(along>0. && along<limit){
   float closest2=max(dot(delta,delta)-along*along,0.);
   float radius=orbRadius(j);
   result+=orbColor()*(.018/(closest2+.025)+2.*(1.-smoothstep(radius*radius,radius*radius*1.3,closest2)));
  }
 }
 return result;
}
vec3 ocean(vec2 uv){
 // Match desert's forward/lateral flight and camera sway exactly.
 uv+=cos(iTime*.3)*vec2(.4,.2);
 vec3 ro=vec3(-iTime*13.,0.,iTime*12.);
 vec3 rd=normalize(vec3(uv,1.));
 // Shift the wave field laterally, while visitors retain camera-relative X motion.
 vec3 waterOrigin=vec3(0.,0.,iTime*12.);
 vec3 color=skyColor(rd);float hit=1000.;
 int marchOctaves=quality==0?12:24;int normalOctaves=quality==0?18:37;
 if(rd.y<-.001){
  float distance=0.;bool found=false;vec3 p=waterOrigin;
  for(int i=0;i<160;i++){
   p=waterOrigin+rd*distance;
   float gap=p.y-waves(p.xz+vec2(ro.x,0.),marchOctaves);
   if(gap<.003){found=true;break;}
   distance+=max(.003,gap*.7);
   if(distance>350.)break;
  }
  if(found){
   hit=distance;float e=.01;vec2 wp=p.xz+vec2(ro.x,0.);
   float h=waves(wp,normalOctaves);
   vec3 n=normalize(vec3(h-waves(wp+vec2(e,0.),normalOctaves),e,h-waves(wp+vec2(0.,e),normalOctaves)));
   n=normalize(mix(n,vec3(0.,1.,0.),.8*min(1.,sqrt(distance*.01)*1.1)));
   vec3 reflected=normalize(reflect(rd,n));reflected.y=abs(reflected.y);
   float fresnel=.04+.96*pow(1.-max(dot(-rd,n),0.),5.);
   color=vec3(.01,.10,.14)*(1.-fresnel)+skyColor(reflected)*fresnel;
   color+=orbEmission(p+n*.02,reflected,1000.)*fresnel;
   for(int j=0;j<2;j++){
    vec3 delta=orbCenter(j)-p;
    color+=orbColor()*.6*max(dot(n,normalize(delta)),0.)/(1.+dot(delta,delta)*.35);
   }
   color=mix(color,skyColor(rd),1.-exp(-distance*.006));
  }
 }
 color+=orbEmission(waterOrigin,rd,hit);
 return color/(1.+color);
}
void main(){vec2 uv=(2.*gl_FragCoord.xy-iResolution)/iResolution.y;vec3 color=scene==0?desert(uv):ocean(uv);gl_FragColor=vec4(pow(max(color,vec3(0.)),vec3(.85)),1.);}
