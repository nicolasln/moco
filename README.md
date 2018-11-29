# MoCo
MoCo is a Blender addon to import and export motion control data. Currently only Flair, the software that powers the Mark Roberts Motion Control systems, is supported.

# Import
Import a file exported from Flair.

- The data must be MRMC Cartesians
- Coordinates my be MRMC

# Export
Export in the MRMC Carts format:
You need to select 2 objects to export, the camera and the target. The roll is hard-coded to 0 for now.

# To do
- Explain export at boundaries or frames
- Camera and targets are created on current layer
- Simplify F Curves, 
- Extra Mocap Tool
- http://slsi.dfki.de/software-and-resources/keyframe-reduction/
- Motion Path
- Motion Trail