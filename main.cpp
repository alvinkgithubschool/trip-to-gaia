#define GL_SILENCE_DEPRECATION
#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <GLUT/glut.h>
#else
#define GL_GLEXT_PROTOTYPES
#include <GL/glut.h>
#endif
#include <fstream>
#include <sstream>
#include <iostream>
#include <cstdlib>
#include <chrono>
#include <iomanip>
#include <algorithm>

GLuint program; int scene=0, width=1280,height=720; bool paused=false;
float elapsed=0,last=0;
double runSeconds=0;
using Clock=std::chrono::steady_clock;
std::ofstream debugLog("gaia-debug.log",std::ios::app);
bool debugVisible=true; int quality=1,frames=0; double totalMs=0,worstMs=0,fps=0,averageMs=0,peakMs=0;
Clock::time_point sampleStart=Clock::now(),previousFrame=Clock::now();
GLint timeLocation,resolutionLocation,sceneLocation,qualityLocation;
void logEvent(const std::string& message){std::cerr<<message<<"\n";debugLog<<message<<"\n";debugLog.flush();}
void overlay(){
 if(!debugVisible)return;
 glUseProgram(0);glMatrixMode(GL_PROJECTION);glPushMatrix();glLoadIdentity();glOrtho(0,width,height,0,-1,1);
 glMatrixMode(GL_MODELVIEW);glPushMatrix();glLoadIdentity();
 glColor3f(.025f,.035f,.045f);glBegin(GL_QUADS);glVertex2i(12,12);glVertex2i(690,12);glVertex2i(690,112);glVertex2i(12,112);glEnd();
 std::ostringstream stats;stats<<std::fixed<<std::setprecision(1)<<fps<<" FPS | "<<averageMs<<" ms avg | "<<peakMs<<" ms max";
 std::ostringstream info;info<<(scene==0?"Desert":"Ocean")<<" | "<<width<<"x"<<height<<" | "<<(quality?"High":"Low")<<" water quality | "<<(paused?"Paused":"Running");
 std::string lines[]={"GAIA DEBUG  [D] hide | [Q] water quality | [L] log snapshot",stats.str(),info.str(),"1 Desert | 2 Ocean | Space Pause | R Restart | Esc Exit"};
 glColor3f(.85f,.92f,1.f);for(int i=0;i<4;i++){glRasterPos2i(24,34+i*22);for(char c:lines[i])glutBitmapCharacter(GLUT_BITMAP_8_BY_13,c);}
 glPopMatrix();glMatrixMode(GL_PROJECTION);glPopMatrix();glMatrixMode(GL_MODELVIEW);
}

GLuint compile(GLenum type,const std::string& source){
 GLuint shader=glCreateShader(type); const char* text=source.c_str();
 glShaderSource(shader,1,&text,nullptr); glCompileShader(shader);
 GLint ok; glGetShaderiv(shader,GL_COMPILE_STATUS,&ok);
 if(!ok){char log[8192];glGetShaderInfoLog(shader,sizeof(log),nullptr,log);logEvent(log);std::exit(1);}return shader;
}
void display(){
 auto frameStart=Clock::now();
 float now=glutGet(GLUT_ELAPSED_TIME)*.001f;if(!paused)elapsed+=now-last;last=now;
 glUseProgram(program);glUniform1f(timeLocation,elapsed);
 glUniform2f(resolutionLocation,width,height);
 glUniform1i(sceneLocation,scene);
 glUniform1i(qualityLocation,quality);
 glBegin(GL_QUADS);glVertex2f(-1,-1);glVertex2f(1,-1);glVertex2f(1,1);glVertex2f(-1,1);glEnd();
 overlay();glutSwapBuffers();
 auto end=Clock::now();double ms=std::chrono::duration<double,std::milli>(end-previousFrame).count();previousFrame=end;
 totalMs+=ms;worstMs=std::max(worstMs,ms);frames++;
 double seconds=std::chrono::duration<double>(end-sampleStart).count();
 if(seconds>=2.){fps=frames/seconds;averageMs=totalMs/frames;peakMs=worstMs;
  std::ostringstream report;report<<"PERF scene="<<scene<<" resolution="<<width<<"x"<<height<<" quality="<<quality<<" fps="<<fps<<" frame_avg_ms="<<averageMs<<" frame_max_ms="<<peakMs<<" submit_ms="<<std::chrono::duration<double,std::milli>(end-frameStart).count();logEvent(report.str());
  frames=0;totalMs=0;worstMs=0;sampleStart=end;
 }
 if(runSeconds>0 && now>=runSeconds){logEvent("Timed profiling run complete");std::exit(0);}
 GLenum error=glGetError();if(error!=GL_NO_ERROR)logEvent("OpenGL error="+std::to_string(error));
}
void reshape(int w,int h){width=w;height=h>0?h:1;glViewport(0,0,width,height);}
void keyboard(unsigned char key,int,int){if(key==27){logEvent("Exit");std::exit(0);}if(key=='d'||key=='D')debugVisible=!debugVisible;if(key=='q'||key=='Q'){quality=1-quality;logEvent("Quality="+std::to_string(quality));}if(key=='l'||key=='L')logEvent("Snapshot time="+std::to_string(elapsed)+" scene="+std::to_string(scene)+" fps="+std::to_string(fps));if(key=='1'){scene=0;logEvent("Scene=desert");}if(key=='2'){scene=1;logEvent("Scene=ocean");}if(key==' ')paused=!paused;if(key=='r')elapsed=0;}
int main(int argc,char** argv){
 for(int i=1;i<argc;i++){std::string arg=argv[i];if(arg=="--ocean")scene=1;else if(arg=="--low")quality=0;else if(arg=="--seconds" && i+1<argc)runSeconds=std::atof(argv[++i]);}
 std::ifstream file("shaders/landscapes.frag");if(!file){std::cerr<<"Run from the project directory: missing shaders/landscapes.frag\n";return 1;}
 std::stringstream source;source<<file.rdbuf();
 glutInit(&argc,argv);glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA);glutInitWindowSize(width,height);
 glutCreateWindow("Trip to Gaia | 1 Desert | 2 Ocean | Space Pause | R Restart | Esc Exit");
 program=glCreateProgram();GLuint vertex=compile(GL_VERTEX_SHADER,"#version 120\nvoid main(){gl_Position=gl_Vertex;}");
 GLuint fragment=compile(GL_FRAGMENT_SHADER,source.str());glAttachShader(program,vertex);glAttachShader(program,fragment);glLinkProgram(program);
 GLint ok;glGetProgramiv(program,GL_LINK_STATUS,&ok);if(!ok){char log[8192];glGetProgramInfoLog(program,sizeof(log),nullptr,log);std::cerr<<log;return 1;}
 timeLocation=glGetUniformLocation(program,"iTime");resolutionLocation=glGetUniformLocation(program,"iResolution");sceneLocation=glGetUniformLocation(program,"scene");qualityLocation=glGetUniformLocation(program,"quality");
 logEvent(std::string("GPU: ")+reinterpret_cast<const char*>(glGetString(GL_RENDERER))+" | GL: "+reinterpret_cast<const char*>(glGetString(GL_VERSION)));
 logEvent("Shader linked successfully; frame timings include presentation/vsync, not isolated GPU timings.");
 previousFrame=sampleStart=Clock::now();
 glDeleteShader(vertex);glDeleteShader(fragment);glutDisplayFunc(display);glutIdleFunc(glutPostRedisplay);glutReshapeFunc(reshape);glutKeyboardFunc(keyboard);glutMainLoop();
}
