# PA4: CS480 

# Leah Jones 

# Collaborators 
OpenGL Resources 
Internet Resources
TA/Piazza

# Assignment 
This implements and renders lighting and shading effects in OpenGL using GLSL. This includes generating meshses, visualizing vertex normals, implementing illumination, and setting up light types. 

### Sketch.py
Purpose: rendering the scenes and managing user interactions.
Features:
- Allows switching between scenes using keyboard inputs (1, 2, 3, etc.). (does not work as intended but logic is there)
- Camera movement (zoom, rotation, and translation) 
- Supports toggling of ambient, diffuse, and specular lighting (A, D, S) and switching to normal rendering (N).
- Texture mapping by binding texture images to shaders.

### SceneOne.py, SceneTwo.py, SceneThree.py
Purpose: different scenes with different lighting, objects and materials 

## DisplayableCube.py, DisplayableEllipsoid.py, DisplayableTorus.py, DisplayableCylinder.py, DisplayablePyramid.py
Purpose: Geometry and Properties of objects 

## GLProgram 
Purpose: Manages shaders 

## Summary 
This assignment involved implementing  OpenGL rendering techniques, and enabling normal visualization for debugging. It featured a  lighting model with ambient, diffuse, and specular components, with point lights, infinite lights, and spotlights with attenuation. Two custom scenes were created, showcasing varied objects, materials, and light setups, with dynamic scene and light toggling via keyboard controls. The shaders handled transformations, lighting, and textures, demonstrating proficiency in interactive computer graphics and shader programming.






