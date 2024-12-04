"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType

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


class DisplayableCube(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    length = None
    width = None
    height = None
    color = None

    def __init__(self, shaderProg, length=1, width=1, height=1, color=ColorType.BLUE):
        super(DisplayableCube, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(length, width, height, color)

    def generate(self, length=1, width=1, height=1, color=None):
        self.length = length
        self.width = width
        self.height = height
        self.color = color
        frontcolor = ColorType.GREENYELLOW

        self.vertices = np.zeros([36, 11])
        vl = np.array([
            # back face
            -length/2, -width/2, -height/2, 0, 0, -1, *color,
            -length/2, width/2, -height/2, 0, 0, -1, *color,
            length/2, width/2, -height/2, 0, 0, -1, *color,

            
            -length / 2, -width / 2, -height / 2, 0, 0, -1, *color,
            length / 2, width / 2, -height / 2, 0, 0, -1, *color,
            length/2, -width/2, -height/2, 0, 0, -1, *color,
            # front face
            -length/2, -width/2, height/2, 0, 0, 1, *frontcolor,
            length/2, -width/2, height/2, 0, 0, 1, *frontcolor,
            length/2, width/2, height/2, 0, 0, 1, *frontcolor,
            -length / 2, -width / 2, height / 2, 0, 0, 1, *frontcolor,
            length / 2, width / 2, height / 2, 0, 0, 1, *frontcolor,
            -length/2, width/2, height/2, 0, 0, 1, *color,
            # left face
            -length/2, -width/2, -height/2, -1, 0, 0, *color,
            -length/2, -width/2, height/2, -1, 0, 0, *color,
            -length/2, width/2, height/2, -1, 0, 0, *color,
            -length / 2, -width / 2, -height / 2, -1, 0, 0, *color,
            -length / 2, width / 2, height / 2, -1, 0, 0, *color,
            -length/2, width/2, -height/2, -1, 0, 0, *color,
            # right face
            length/2, -width/2, height/2, 1, 0, 0, *color,
            length/2, -width/2, -height/2, 1, 0, 0, *color,
            length/2, width/2, -height/2, 1, 0, 0, *color,
            length / 2, -width / 2, height / 2, 1, 0, 0, *color,
            length / 2, width / 2, -height / 2, 1, 0, 0, *color,
            length/2, width/2, height/2, 1, 0, 0, *color,
            # top face
            -length/2, width/2, height/2, 0, 1, 0, *color,
            length/2, width/2, height/2, 0, 1, 0, *color,
            length/2, width/2, -height/2, 0, 1, 0, *color,
            -length / 2, width / 2, height / 2, 0, 1, 0, *color,
            length / 2, width / 2, -height / 2, 0, 1, 0, *color,
            -length/2, width/2, -height/2, 0, 1, 0, *color,
            # bottom face
            -length/2, -width/2, -height/2, 0, -1, 0, *color,
            length/2, -width/2, -height/2, 0, -1, 0, *color,
            length/2, -width/2, height/2, 0, -1, 0, *color,
            -length / 2, -width / 2, -height / 2, 0, -1, 0, *color,
            length / 2, -width / 2, height / 2, 0, -1, 0, *color,
            -length/2, -width/2, height/2, 0, -1, 0, *color,
        ]).reshape((36, 9))
        self.vertices[0:36, 0:9] = vl

        self.indices = np.array([x for x in range(36)])


    def draw(self):
        if self.texture_id:  # Bind the texture if available
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
        self.vao.bind()
        # TODO 1.1 is at here, switch from vbo to ebo
        self.ebo.draw()
        self.vao.unbind()
        if self.texture_id:  # Unbind the texture
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def load_texture(self, file_path):
        """
        Load a texture from the given file path and bind it to OpenGL.
        """
        from PIL import Image

        try:
            # Open and flip the image vertically
            img = Image.open(file_path)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = img.convert("RGBA").tobytes()

            # Generate texture
            texture_id = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

            # Pass the image data to OpenGL
            gl.glTexImage2D(
                gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, img.width, img.height, 0,
                gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data
            )

            # Set texture parameters
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

            # Unbind the texture
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

            return texture_id

        except Exception as e:
            print(f"Error loading texture {file_path}: {e}")
            return None

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
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
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        texture_path = "C:/Users/Owner/Downloads/PA4_Fall2024/PA4_Fall2024/assets/earth.jpg"
        self.texture_id = self.load_texture(texture_path)
        self.vao.unbind()



