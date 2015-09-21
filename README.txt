-----------------------------------------------------------
CURRENT
-----------------------------------------------------------

--- Installation ---
sudo apt-get install python-pygame
sudo apt-get install imagemagick


--- Running the program ---
"python main.py -t" - Runs the test cases, in long form
"python main.py -ts" - Runs the test cases, in short form
"python main.py -td" - Runs the test of showing a simple pyramid object
"python main.py -rs" - Runs the simulator, takes days to complete and eventually gives the parameters for the optimum walk
"python main.py -rp" - Runs the mech in walking mode with a given set of parameters


--- MindFuckStructure ---
The mfStructure class is a generic, clean structure simulator. A user adds joints to it to describe the structure. A structure can do several things: compute the locations/dimensions of it's own structure, detect parts of the structure that collide with others, display itself.

joint.py - A complex joint class, able to do difficult calculations with the help of it's libraries. Many of these make up a structure.
* joint_generalHelperFunctions.py - A lot of basic trig
* joint_collisionHelperFunctions.py - Functions to compute collisions
* joint_locationHelperFunctions.py - Functions for computing the locations of each joint relative to the others

* structureDisplay.py - A class for bringing up a display of the structure
* displayView.py - An individual window within the display, able to do the transformations of perspective it needs to show the object at that angle.

* span.py - A simple span class, used for holding simple information about it's own length, mass, and how to display it
* displayProperties.py - Information about how to display a given joint 
* location.py - A location in 3D, able to perform a number of basic trigonometric functions


--- Mech ---
The mech has a hard-coded description of it's structure. It also has a simulator that computes the parameters needed for walking. In this computation it assumes a certain series of actuator movements and empyrically finds exactly what actuator lengths to use in those movements. During this, it checks to see if it will take strides that are too big, too small, too low, stepping on it's own feet, or failing to make contact with the ground. In the end it will print some statistics of the walk and display an animation of it walking.


-----------------------------------------------------------
FUTURE / MESSY NOTES
-----------------------------------------------------------
Simulation of walking
* Collision detection - DONE
* Design upgrades
** Cockpit in the design - foldable - Better be one in back of the other
** Engine
** Exacting joint dimensions
* Center of mass - Partially handled by the stride length - Take into account??
** Stats on how close to the edge it is
* Other movements like crouching and turning

Serious, it's time we handle center of mass correctly. This requires we actually know the mass of the various components. Can't we make some assumptions and begin to at least put those in. Like 'angle iron, thickness'

For now, let's do center of mass but no gravity. - center of mass should be drawable
* every limb has mass
* center of mass can be drawn with cross hairs

We need to be able to seee what joints are which
* Take labels as the first parameter of the joint
* Take labels as all the parameters of the joint...  

Simulation approach:
* Run the simulation to find the set of all effective combinations. (100^5? -- very many. We should run the simulation to raise the foot as separate.
** Optimize the step - make an ordered list of best steps.
** Check each one for collision detection, including the calf movement.

* VARIABLES: Foot length,thigh length, calf length 
* CRITERIA: 
** Feet must not collide
** Foot must not scrape the ground
** center of mass must always be over the right foot by so
* 
* Simulation of turning
* collision detection - DONE
* Fall-over warning
** Center of mass calculation
** 
* Center of mass calculation and summation
** How will we determine if center of mass has been violated? I do want to bring it down and rotate it until it's on the ground.
** What's wrong with bringing it down and rotating it? That depends on the other locations that were built. Will these also be moved and rotated? I don't see why not. They're saved next to everything else. We do a transformation of all of it.
** Do we really need this to do our job correctly? I understand the collision detection system but this seems over-blown. WHy not just put points on the feet, call those zero and let it go? 
What does the simulation look like? More than one step? Not really, just putting one foot in front and transferring the weight.

Simulation of turning
