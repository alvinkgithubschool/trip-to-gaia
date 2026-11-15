# Trip to Gaia — Blender rebuild

Open `Trip_to_Gaia.blend` in Blender 5.3. Choose Gaia_Desert or Gaia_Ocean and play frames 1–240 (24 FPS, ten seconds). The original Scene is retained, and the original project file is untouched. Render with F12. No external assets or Python handlers are needed for playback.

Rebuild in a fresh Blender session: open the Scripting workspace, load `build_gaia.py`, and Run Script. Keep `refine_gaia.py` beside it. This writes Trip_to_Gaia.blend beside the script. Existing Gaia scenes cause a safe refusal; existing unrelated scenes are retained. Alternatively run `blender --background --python build_gaia.py`. For six checks run `render_checks.py` after opening the output file. Background Eevee could not obtain Metal in this environment, so previews were rendered through the connected official Blender MCP window.

Settings: Eevee, ray tracing enabled, 48 samples, 1280×720, one render subdivision level. Six PNG checks are in previews/ (frames 1, 120, 240); per-frame timings are in render_report.json, approximately 2–4 seconds on the connected session after shader warmup. First unrefined cold render took 7.46 seconds. Generated previews, backups and caches are Git-ignored.

The shared rig maps shader (x,y,z) into Blender (x,z,y). A -13t horizontal translation turns the shader's laterally scrolling surface into stationary geometry; visitors receive the same translation. Camera and visitor motion is sampled every frame, with t=(frame-1)/24. Camera lens shift recreates the shader's off-axis sway. Radii and raised visitor paths come directly from landscapes.frag.

Desert geometry solves the seven-step implicit ground equation by bisection, with material-only grain and ripples. The shader's accumulated raymarch brightness and upper distance-field surface are not physically reproducible with this height field: the result has deeper valleys, more physical shadows and a daylight sky rather than the original abstract amber glow. Subdivision reduces sampled faceting; a distant flat horizon closes the finite mesh boundary.

Ocean geometry uses the supplied exponential wave and domain-warp equations (18 iterations), baked into shape keys every four frames. This reduces fine wave detail and temporal accuracy relative to the 37-iteration shader. Whitecaps use height and procedural breakup; reflections use Eevee screen tracing, so tiny orb reflections are much less conspicuous than the shader's analytical halos. The physical sky also differs from skyColor(). Attached point lights and restrained compositor glow are included. Meshes, materials, lights, keyframes and shape keys remain editable. The large baked wave data makes the compressed file about 147 MB.

Checks found both visitors in frame at beginning/middle/end. Their minimum height stays above water's maximum zero height; the desert lies below the camera. Initial horizon gaps and pronounced faceting were corrected and previews regenerated. This is a geometry adaptation, not a pixel-identical shader recreation.

References: ../shaders/landscapes.frag and ../Trip_to_Gaia_Project_Proposal.md. Desert source attribution: https://www.shadertoy.com/view/3cXyzB (MIT, as noted in supplied shader). Ocean model: afl_ext 2024, https://www.shadertoy.com/view/M3fGDl (public domain, as noted in supplied shader).

## Cinematic lighting and tracking update

The build now also runs `cinematic_gaia.py` (keep it beside the other scripts). This replaces the original off-axis camera sway with a shared 18 mm camera, a filtered visitor tracking aim, 5.5 cm slow vertical bob and 28 cm lateral drift layered over the original flight rig. The 240-frame animation remains baked and editable. Desert lighting is now low amber dawn with bounded volumetric haze; ocean lighting is muted blue twilight with a lavender horizon, cool directional light, and warm visitor lights. AgX exposure and restrained glare retain surrounding surface detail. These choices intentionally depart from the exact shader camera and sky.

All 240 frames were checked for visitor-center framing: screen X 0.397–0.568, Y 0.410–0.902, positive camera depth throughout. Six updated renders are in previews/, with timings in render_report.json. The file opens at frame 1 in desert camera view. Press Space in the viewport to play; select Rendered shading to see the atmosphere. `cinematic_gaia.py` can be reapplied to the generated project, and `render_checks.py` refreshes the six previews.
