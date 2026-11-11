# Trip to Gaia

A C++ / OpenGL landscape prototype: a warm procedural desert and a moonlit ocean, each with two animated orb visitors.

## Build and run

On macOS, install Xcode Command Line Tools. On Linux, install a C++ compiler and freeglut development headers. From this folder:

```sh
make
./gaia
```

Press **1** for desert, **2** for ocean, **Space** to pause, **R** to restart time, and **Esc** to exit. Resize the window to change resolution. The shader is loaded from `shaders/landscapes.frag`; launch from this directory.

The desert adapts the user-supplied MIT-licensed code from https://www.shadertoy.com/view/3cXyzB with initialized accumulators, guarded divisions and a second orb. The ocean is an original procedural heightfield implementation. The second reference, https://www.shadertoy.com/view/w3KyW1, could not be retrieved, so its source has not been incorporated.

This is an environment prototype. The remaining three environments, soundtrack, transitions and course algorithm demonstrations described in the proposal are future work. Requires desktop OpenGL 2.1 / GLSL 1.20 compatibility support; macOS uses the deprecated system GLUT framework.
