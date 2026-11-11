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

GLuint program; int scene=0, width=1280,height=720; bool paused=false;
float elapsed=0,last=0;
GLuint compile(GLenum type,const std::string& source){
 GLuint shader=glCreateShader(type); const char* text=source.c_str();
 glShaderSource(shader,1,&text,nullptr); glCompileShader(shader);
 GLint ok; glGetShaderiv(shader,GL_COMPILE_STATUS,&ok);
 if(!ok){char log[8192];glGetShaderInfoLog(shader,sizeof(log),nullptr,log);std::cerr<<log;std::exit(1);}return shader;
}
void display(){
 float now=glutGet(GLUT_ELAPSED_TIME)*.001f;if(!paused)elapsed+=now-last;last=now;
 glUseProgram(program);glUniform1f(glGetUniformLocation(program,"iTime"),elapsed);
 glUniform2f(glGetUniformLocation(program,"iResolution"),width,height);
 glUniform1i(glGetUniformLocation(program,"scene"),scene);
 glBegin(GL_QUADS);glVertex2f(-1,-1);glVertex2f(1,-1);glVertex2f(1,1);glVertex2f(-1,1);glEnd();
 glutSwapBuffers();
}
void reshape(int w,int h){width=w;height=h>0?h:1;glViewport(0,0,width,height);}
void keyboard(unsigned char key,int,int){if(key==27)std::exit(0);if(key=='1')scene=0;if(key=='2')scene=1;if(key==' ')paused=!paused;if(key=='r')elapsed=0;}
int main(int argc,char** argv){
 std::ifstream file("shaders/landscapes.frag");if(!file){std::cerr<<"Run from the project directory: missing shaders/landscapes.frag\n";return 1;}
 std::stringstream source;source<<file.rdbuf();
 glutInit(&argc,argv);glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA);glutInitWindowSize(width,height);
 glutCreateWindow("Trip to Gaia | 1 Desert | 2 Ocean | Space Pause | R Restart | Esc Exit");
 program=glCreateProgram();GLuint vertex=compile(GL_VERTEX_SHADER,"#version 120\nvoid main(){gl_Position=gl_Vertex;}");
 GLuint fragment=compile(GL_FRAGMENT_SHADER,source.str());glAttachShader(program,vertex);glAttachShader(program,fragment);glLinkProgram(program);
 GLint ok;glGetProgramiv(program,GL_LINK_STATUS,&ok);if(!ok){char log[8192];glGetProgramInfoLog(program,sizeof(log),nullptr,log);std::cerr<<log;return 1;}
 glDeleteShader(vertex);glDeleteShader(fragment);glutDisplayFunc(display);glutIdleFunc(glutPostRedisplay);glutReshapeFunc(reshape);glutKeyboardFunc(keyboard);glutMainLoop();
}
