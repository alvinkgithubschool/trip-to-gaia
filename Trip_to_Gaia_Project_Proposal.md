# Trip to Gaia

*A procedural, atmospheric exploration of a world beyond humanity*

**ICS 3204 · Computer Graphics · Project Definition · November 2026**

## 01 / Concept & Experience

Two mysterious, orb-shaped alien visitors arrive on Earth long after humanity has vanished. Defying conventional physics, they drift, orbit and dance through seemingly endless landscapes, driven by curiosity and intrigue. Each environment tells part of the story through terrain, colour, lighting, movement and a distinct backing track. The journey ends with a vibrant archipelago, suggesting renewal and the resilience of life.

**Core experience:** A continuously scrolling exploration with two animated protagonists, five themed environments, smooth scene transitions, ambient soundtracks and light interaction (e.g., camera or movement controls).

## 02 / The Five Environments

| Environment | Time | Visual elements |
|---|---|---|
| **01 · Desert** | Early morning | Rolling dunes, long shadows, sparse ruins, warm dawn palette |
| **02 · Forest & Greenland** | Midday | Trees, rolling hills, dense vegetation, vivid greens and daylight |
| **03 · Urban Wasteland** | Sunset | Collapsed buildings, overgrowth, silhouettes, amber skies |
| **04 · Ocean** | Night | Moonlit waves, reflections, wreckage and animated marine life |
| **05 · Archipelago** | Morning | Lush islands, abundant life, soft sunrise and hopeful atmosphere |

## 03 / Graphics Concepts & Implementation

**Course foundations (pure C++ first):** DDA/Bresenham lines; midpoint circles and ellipses for orb shapes; triangles, polygons and filling for terrain/buildings; Bézier curves and splines for organic motion and contours; RGB/HSV colour models; translation, rotation, scaling and homogeneous transformation matrices; raster operations and frame-based animation.

**OpenGL stage:** Rendering pipeline, camera and scene setup, geometry integration, lighting, shading, textures and real-time animation. GLFW/GLUT may provide the application window and input handling.

**Optional advanced extensions:** Signed distance functions (SDFs), raymarching for terrain and objects, procedural generation and infinite scrolling, shader-based colour mixing, atmospheric effects, water reflections and stylized lighting. These supplement—not substitute for—the demonstrable course algorithms.

## 04 / Development Phases & Checkpoint Evidence

### Week of 02 Nov · Phase 1 — Design & Foundations / CP1

Define narrative, scenes, interaction and art direction. Implement initial pure C++ graphics algorithms and simplified components.

**Checkpoint:** Concept summary; planned graphics concepts; completed algorithms/components; next steps.

### Week of 09 Nov · Phase 2 — Build Graphics / CP2

Create terrain/tree/building/wave primitives with polygons, filling and curves. Extend components with pure C++ transformations and early animation.

**Checkpoint:** Algorithms implemented; screenshot of current scene; GitHub repository link; remaining work.

### Week of 16 Nov · Phase 3 — Transform, Animate & OpenGL / CP3

Integrate geometry into OpenGL; implement rendering loop, camera movement, orb animation, input and initial effects.

**Checkpoint:** Current OpenGL implementation; animation/interaction evidence; GitHub link; remaining work.

### Week of 23 Nov · Phase 4 — Render, Integrate & Demonstrate / Prototype

Assemble five environments into a navigable prototype; refine scene transitions, lighting, music and performance.

**Checkpoint:** Final demo; working features; known limitations; final changes/recommendations.

## 05 / Scope & Success Criteria

**Minimum viable prototype:** Two clearly animated orb visitors, one working seamless-scrolling environment, demonstrable pure C++ algorithms, OpenGL rendering, and basic navigation/interaction. Expand to all five distinctive environments with synchronized soundtrack, transitions, lighting and atmospheric effects for the final project.

Success will be evidenced through algorithm demonstrations, source-code history on GitHub, checkpoint screenshots/videos, a running OpenGL prototype and a final demonstration clearly distinguishing completed features from experimental techniques.

**Course alignment:** *ICS 3204 Computer Graphics Course Outline*, pp. 1–6, 8 (geometric primitives, polygon filling, curves, transformations, raster operations, OpenGL, lighting/shading and animation).
