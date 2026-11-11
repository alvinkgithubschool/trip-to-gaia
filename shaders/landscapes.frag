#version 120
uniform float iTime;
uniform vec2 iResolution;
uniform int scene;

// Desert adapted from the MIT-licensed shader supplied with the project:
// https://www.shadertoy.com/view/3cXyzB
vec3 desert(vec2 uv){
 float d=0.,s=0.,e=1.,brightness=0.;
 float t=iTime,zt=t*12.,xt=t*13.;
 uv+=cos(t*.3)*vec2(.4,.2);
 for(int i=0;i<128;i++){
  vec3 p=vec3(uv*d,d+zt);
  e=length(p-vec3(sin(sin(t*.2)+t*.4)*4.,sin(sin(t*1.3)+t*.2)*2.,14.+zt+cos(t*.5)*8.))-.1;
  // A second visitor follows a distinct orbit.
  e=min(e,length(p-vec3(cos(t*.34)*3.,sin(t*.8)*1.6,18.+zt+sin(t*.4)*5.))-.14);
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
float waves(vec2 p){
 return sin(p.x*.55+iTime*.7)*.24+sin(p.y*.8-iTime)*.18+sin(p.x*1.8+p.y*1.3+iTime*1.5)*.07;
}
vec3 ocean(vec2 uv){
 vec3 ro=vec3(0.,2.4,iTime*2.);
 vec3 rd=normalize(vec3(uv.x,uv.y-.15,1.5));
 vec3 moon=normalize(vec3(.5,.42,1.));
 float light=max(dot(rd,moon),0.);
 vec3 sky=mix(vec3(.025,.055,.11),vec3(.12,.22,.32),exp(-abs(rd.y)*4.));
 sky+=vec3(.7,.83,1.)*smoothstep(.999,.9997,light);
 sky+=vec3(.12,.18,.26)*pow(light,24.);
 vec3 color=sky;
 if(rd.y<0.){
  float distance=0.;vec3 p=ro;
  for(int i=0;i<100;i++){
   p=ro+rd*distance;float gap=p.y-waves(p.xz);
   if(gap<.015||distance>180.)break;
   distance+=max(.02,gap*.45);
  }
  if(distance<180.){
   float eps=.04;float h=waves(p.xz);
   vec3 n=normalize(vec3(h-waves(p.xz+vec2(eps,0.)),eps,h-waves(p.xz+vec2(0.,eps))));
   vec3 reflected=reflect(rd,n);
   float shine=pow(max(dot(reflected,moon),0.),140.);
   float fresnel=pow(1.-max(dot(-rd,n),0.),5.);
   color=mix(vec3(.008,.08,.11),sky,.3+fresnel*.6)+shine*vec3(.75,.86,1.);
   color=mix(color,sky,1.-exp(-distance*.012));
  }
 }
 for(int j=0;j<2;j++){
  float f=float(j);vec2 center=vec2(sin(iTime*.4+f*2.)*.45,.08+sin(iTime*.65+f*2.)*.13);
  float r=length(uv-center);vec3 tint=mix(vec3(.3,.85,1.),vec3(1.,.6,.25),f);
  color+=tint*(.0015/max(r*r,.001)+.8*smoothstep(.035,.025,r));
 }
 return color;
}
void main(){vec2 uv=(2.*gl_FragCoord.xy-iResolution)/iResolution.y;vec3 color=scene==0?desert(uv):ocean(uv);gl_FragColor=vec4(pow(max(color,vec3(0.)),vec3(.85)),1.);}
