
from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
from Point import Point
import numpy as np
import ColorType
import math
try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    nsides = 0
    radius = 0
    height = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, radius=0.5, height=1, nsides=36, stacks=1, color=ColorType.SOFTBLUE):
        super(DisplayableCylinder, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, height, nsides, color)

    def generate(self, radius=0.5, height=1, nsides=36, color=ColorType.SOFTBLUE):
        self.radius = radius
        self.height = height
        self.nsides = nsides
        self.color = color

        # Prepare vertices and indices
        self.vertices = np.zeros([(nsides + 1) * 2 + 2, 11])  # Sides + 1 extra for closing + top/bottom centers
        self.indices = []

        # Generate side vertices (top and bottom)
        for i in range(nsides + 1):
            angle = 2 * math.pi * i / nsides
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            # Bottom vertex (-z)
            self.vertices[i][:9] = [x, y, -height / 2, x, y, 0, *color]

            # Top vertex (+z)
            self.vertices[i + nsides + 1][:9] = [x, y, height / 2, x, y, 0, *color]

        # Generate indices for the sides
        for i in range(nsides):
            self.indices.extend([
                [i, (i + 1) % nsides, i + nsides + 1],
                [(i + 1) % nsides, (i + 1) % nsides + nsides + 1, i + nsides + 1]
            ])

        # Bottom center vertex (-z)
        botCenterIdx = len(self.vertices) - 2
        self.vertices[botCenterIdx][:9] = [0, 0, -height / 2, 0, 0, -1, *color]

        # Generate indices for the bottom cap
        for i in range(nsides):
            self.indices.append([botCenterIdx, i, (i + 1) % nsides])

        # Top center vertex (+z)
        topCenterIdx = len(self.vertices) - 1
        self.vertices[topCenterIdx][:9] = [0, 0, height / 2, 0, 0, 1, *color]

        # Generate indices for the top cap
        for i in range(nsides):
            self.indices.append([topCenterIdx, (i + 1) % nsides + nsides + 1, i + nsides + 1])

        # Convert indices to NumPy array
        self.indices = np.array(self.indices)



    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems which don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=11, offset=6, attribSize=3)

        self.vao.unbind()