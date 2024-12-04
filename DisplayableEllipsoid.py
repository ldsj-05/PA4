"""
Define ellipsoid here.
First version in 12/03/2024

:author: micou(Zezhou Sun)
:version: 2024.12.03
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
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


class DisplayableEllipsoid(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # Stores current ellipsoid's information, read-only
    stacks = 0
    slices = 0
    radiusX = 0
    radiusY = 0
    radiusZ = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, radiusX=0.6, radiusY=0.3, radiusZ=0.9, stacks=18, slices=36, color=ColorType.SOFTBLUE):
        super(DisplayableEllipsoid, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # VBO requires active GLProgram
        self.ebo = EBO()

        self.generate(radiusX, radiusY, radiusZ, stacks, slices, color)

    def generate(self, radiusX=0.6, radiusY=0.3, radiusZ=0.9, stacks=18, slices=36, color=ColorType.SOFTBLUE):
        self.radiusX = radiusX
        self.radiusY = radiusY
        self.radiusZ = radiusZ
        self.stacks = stacks
        self.slices = slices
        self.color = color

        vertex_count = (stacks + 1) * (slices + 1)
        self.vertices = np.zeros((vertex_count, 11))
        indices = []

        for i in range(stacks + 1):
            phi = math.pi * i / stacks  # Latitude angle
            for j in range(slices + 1):
                theta = 2 * math.pi * j / slices  # Longitude angle

                x = radiusX * math.sin(phi) * math.cos(theta)
                y = radiusY * math.cos(phi)
                z = radiusZ * math.sin(phi) * math.sin(theta)

                nx = x / radiusX
                ny = y / radiusY
                nz = z / radiusZ
                length = math.sqrt(nx**2 + ny**2 + nz**2)
                nx, ny, nz = nx / length, ny / length, nz / length

                u = j / slices
                v = i / stacks

                vertex_index = i * (slices + 1) + j
                self.vertices[vertex_index][:9] = [x, y, z, nx, ny, nz, *color]
                self.vertices[vertex_index][9:] = [u, v]

                if i < stacks and j < slices:
                    p0 = i * (slices + 1) + j
                    p1 = p0 + 1
                    p2 = p0 + (slices + 1)
                    p3 = p2 + 1
                    indices.append([p0, p2, p1])
                    indices.append([p1, p2, p3])

        self.indices = np.array(indices).flatten()

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bound, the program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation.
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
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=11, offset=9, attribSize=2)
        self.vao.unbind()
