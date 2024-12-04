"""
Define Torus here.
First version in 11/01/2021

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


class DisplayableTorus(Displayable):
    def __init__(self, shaderProg, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTGREEN):
        super(DisplayableTorus, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # VBO can only be initiated with a shader program activated
        self.ebo = EBO()

        self.generate(innerRadius, outerRadius, nsides, rings, color)

    def generate(self, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTGREEN):
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.nsides = nsides
        self.rings = rings
        self.color = color

        # Number of vertices and indices
        num_vertices = (rings + 1) * (nsides + 1)
        num_indices = rings * nsides * 6

        # Initialize vertices and indices
        self.vertices = np.zeros((num_vertices, 11), dtype=np.float32)  # pos(3), normal(3), color(3), texCoord(2)
        self.indices = np.zeros(num_indices, dtype=np.uint32)

        # Generate vertices
        for i in range(rings + 1):
            theta = 2.0 * math.pi * i / rings
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            for j in range(nsides + 1):
                phi = 2.0 * math.pi * j / nsides
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)

                # Position
                x = (outerRadius + innerRadius * cos_phi) * cos_theta
                y = (outerRadius + innerRadius * cos_phi) * sin_theta
                z = innerRadius * sin_phi

                # Normal
                nx = cos_phi * cos_theta
                ny = cos_phi * sin_theta
                nz = sin_phi

                # Index for vertex array
                idx = i * (nsides + 1) + j

                # Store vertex attributes
                self.vertices[idx, 0:3] = [x, y, z]
                self.vertices[idx, 3:6] = [nx, ny, nz]  # Normal
                self.vertices[idx, 6:9] = [color.r, color.g, color.b]  # Color
                self.vertices[idx, 9:11] = [i / rings, j / nsides]  # Texture coordinates

        # Generate indices
        idx = 0
        for i in range(rings):
            for j in range(nsides):
                p0 = i * (nsides + 1) + j
                p1 = p0 + 1
                p2 = p0 + (nsides + 1)
                p3 = p2 + 1

                # Two triangles per quad
                self.indices[idx:idx + 6] = [p0, p1, p2, p1, p3, p2]
                idx += 6

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Bind VAO, VBO, and EBO for rendering
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)  # 11 attributes per vertex
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"), stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"), stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"), stride=11, offset=6, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"), stride=11, offset=9, attribSize=2)

        self.vao.unbind()
