# Trip to Gaia

A C++ / OpenGL landscape prototype: a warm procedural desert and a moonlit ocean, each with two animated orb visitors.

## Build and run

On macOS, install Xcode Command Line Tools. On Linux, install a C++ compiler and freeglut development headers. From this folder:

```sh
make
./gaia
```

Press **1** for desert, **2** for ocean, **Space** to pause, **R** to restart time, and **Esc** to exit. Resize the window to change resolution. The shader is loaded from `shaders/landscapes.frag`; launch from this directory.

The desert adapts the user-supplied MIT-licensed code from https://www.shadertoy.com/view/3cXyzB with initialized accumulators, guarded divisions and a second orb. The ocean adapts the public domain afl_ext 2024 wave model supplied from https://www.shadertoy.com/view/M3fGDl, with a simplified sky, bounded marching, shared desert orb trajectories, water reflections and local orb lighting. The second reference, https://www.shadertoy.com/view/w3KyW1, could not be retrieved, so its source has not been incorporated.

This is an environment prototype. The remaining three environments, soundtrack, transitions and course algorithm demonstrations described in the proposal are future work. Requires desktop OpenGL 2.1 / GLSL 1.20 compatibility support; macOS uses the deprecated system GLUT framework.

## Debugging and optimisation

The debug panel starts visible. Press **D** to toggle it, **Q** to switch water wave quality (12/18 versus 24/37 wave iterations for marching/normals), and **L** to log a snapshot. `gaia-debug.log` records GPU/driver details, shader failures, scene/quality changes, OpenGL errors and two-second FPS/average/max frame time samples. Timings include swap/vsync and overlay cost; they are not isolated GPU timings. Compare the same scene and resolution with the overlay hidden when profiling. Logs append across launches and are excluded from Git.

Both scenes share a raised, gently bobbing camera and raised orb paths. Desert sand grain/ripples modulate color without changing dunes. Ocean whitecaps follow wave height and slope without changing wave geometry. Ocean marching skips air above the maximum water height, and distant normals use fewer wave octaves.

For repeatable performance samples: `./gaia --ocean --seconds 10` or `./gaia --ocean --low --seconds 10`. Close other Gaia windows first to avoid competing GPU workloads. Compare logs at the same window size; frame times include vsync.
