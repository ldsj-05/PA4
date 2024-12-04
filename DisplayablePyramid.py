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


class DisplayablePyramid(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, baseSize=1.0, height=1.5, color=ColorType.SOFTBLUE):
        super(DisplayablePyramid, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # VBO requires active GLProgram
        self.ebo = EBO()

        self.generate(baseSize, height, color)

    def generate(self, baseSize=1.0, height=1.5, color=ColorType.SOFTBLUE):
        if not isinstance(color, (list, tuple, np.ndarray)):
            raise ValueError("Color must be an iterable (list, tuple, or numpy array).")
        
        if len(color) != 3 and len(color) != 4:
            raise ValueError("Color must have 3 (RGB) or 4 (RGBA) components.")

        halfBase = baseSize / 2

        # Define vertices (position, normal, color)
        # Base vertices
        v0 = [-halfBase, 0, -halfBase]
        v1 = [halfBase, 0, -halfBase]
        v2 = [halfBase, 0, halfBase]
        v3 = [-halfBase, 0, halfBase]
        # Apex
        v4 = [0, height, 0]

        # Define normals for the faces
        n_base = [0, -1, 0]
        n_front = [0, height / 2, -baseSize / 2]
        n_right = [baseSize / 2, height / 2, 0]
        n_back = [0, height / 2, baseSize / 2]
        n_left = [-baseSize / 2, height / 2, 0]

        # Normalize normals
        def normalize(vec):
            length = np.linalg.norm(vec)
            return vec / length

        n_front = normalize(n_front)
        n_right = normalize(n_right)
        n_back = normalize(n_back)
        n_left = normalize(n_left)

        # Add vertices with positions, normals, and color
        self.vertices = np.array([
            *v0, *n_base, *color,
            *v1, *n_base, *color,
            *v2, *n_base, *color,
            *v3, *n_base, *color,
            *v4, *n_front, *color,
            *v4, *n_right, *color,
            *v4, *n_back, *color,
            *v4, *n_left, *color,
        ], dtype=np.float32).reshape((-1, 9))

        # Define indices for triangles
        self.indices = np.array([
            # Base face
            0, 1, 2,
            0, 2, 3,
            # Front face
            0, 1, 4,
            # Right face
            1, 2, 5,
            # Back face
            2, 3, 6,
            # Left face
            3, 0, 7
        ], dtype=np.uint32)


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
        self.vbo.setBuffer(self.vertices, 9)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=9, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=9, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=9, offset=6, attribSize=3)
        self.vao.unbind()
