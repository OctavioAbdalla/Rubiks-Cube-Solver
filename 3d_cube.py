from ursina import *
from itertools import product
import kociemba

class RubiksCube(Entity):
    def __init__(self):
        super().__init__()
        window.borderless = False
        window.size = (800, 800)
        window.position = (200, 200)
        
        self.duration = 0
        self.action_trigger = True
        self.pre_cube_status = True
        self.result = [[], 0]

        self.filename = 'rubiks_cube.txt'
        self.original_cube = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
        self.modified_cube = self.read_cube_string_from_file(self.filename)

        self.editor_camera = EditorCamera()
        self.center = Entity()
        self.cubes = self.generate_cube()
        
        self.rotation_dict = {
            "U": ['y', 1, 90],    "U'": ['y', 1, -90],   "U2": ['y', 1, 180],
            "D": ['y', -1, -90],  "D'": ['y', -1, 90],   "D2": ['y', -1, 180],
            "L": ['x', -1, -90],  "L'": ['x', -1, 90],   "L2": ['x', -1, 180],
            "R": ['x', 1, 90],    "R'": ['x', 1, -90],   "R2": ['x', 1, 180],
            "F": ['z', -1, 90],   "F'": ['z', -1, -90],  "F2": ['z', -1, 180],
            "B": ['z', 1, -90],   "B'": ['z', 1, 90],    "B2": ['z', 1, 180],
            "right arrow": 0, "left arrow": 0
        }

        self.movement_dict = ["right arrow", "left arrow"]
        
        self.solution_steps()

    def read_cube_string_from_file(self, filename):
        with open(filename, 'r') as file:
            return file.read()

    def generate_cube(self):
        cubes = []
        for pos in product((-1,0,1), repeat=3):    
            cubes.append(Entity(model='assets/model', texture='assets/texture', position=pos, scale=0.5))
        return cubes

    def solution_steps(self):
        for i in kociemba.solve(self.modified_cube).split(' '):
            if i[-1] == '2':
                self.result[0].append(i[0])
                self.result[0].append(i[0])
            else:
                self.result[0].append(i)

    def parent_child_relationship(self, axis, layer):
        #Sets up the parent-child relationship for rotating cube layers.
        for cube in self.cubes:
            cube.position, cube.rotation = round(cube.world_position, 1), cube.world_rotation
            cube.parent = scene
        
        self.center.rotation = 0

        for cube in self.cubes:
            if eval(f'cube.position.{axis}') == layer:
                cube.parent = self.center

    def toggle_animation_trigger(self):
        #Prevents interaction during rotation animation.
        self.action_trigger = not self.action_trigger

    def rotate_layer(self, key):
        #Rotates a specific layer of the cube.
        if not self.pre_cube_status: self.action_trigger = False
        axis, layer, angle = self.rotation_dict[key]
        self.parent_child_relationship(axis, layer)
        eval(f'self.center.animate_rotation_{axis} ({angle}, duration = {self.duration})')
        if not self.pre_cube_status: invoke(self.toggle_animation_trigger, delay=self.duration + 0.1)

    def step_forward(self):
        #Performs the next move in the solution sequence.
        if self.result[1] < len(self.result[0]):
            self.input(self.result[0][self.result[1]])
            self.result[1] += 1

    def step_backward(self):
        #Reverts the previous move in the solution sequence.
        if self.result[1] > 0:
            self.result[1] -= 1
            move = self.result[0][self.result[1]]
            self.input(move[0] if len(move) == 2 else move + "'")

    def input(self, key):
        #Handles key inputs to trigger cube rotations or solve steps.
        if self.action_trigger and key in self.rotation_dict:
            if key == "right arrow": 
                self.step_forward()
            elif key == "left arrow": 
                self.step_backward()
            else:
                self.rotate_layer(key)

    def pre_cube(self):
        #Does all the steps to make the original cube looks like the scanned one
        pre_cube = kociemba.solve(self.original_cube, self.modified_cube)
        for l in pre_cube.split(' '):
            self.input(l)
        self.pre_cube_status = False
        self.duration = 0.5

app = Ursina()
rubiks_cube = RubiksCube()
rubiks_cube.pre_cube()
app.run()