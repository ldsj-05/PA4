"""
Define a scene with an ellipsoid, cylinder, and cube
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math
import numpy as np

import ColorType
from Animation import Animation
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableCylinder import DisplayableCylinder


class SceneTwo(Component, Animation):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None

    lRadius = None
    lAngles = None
    lTransformations = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        # Light configuration
        self.lRadius = 3
        self.lAngles = [0, 0]
        self.lTransformations = [self.glutility.translate(0, 2, 0, False)]

        # Cube
        cube = Component(Point((-2, 0, 0)), DisplayableCube(shaderProg, 1.0))
        m_cube = Material(
            np.array((0.1, 0.1, 0.1, 1.0)),
            np.array((0.8, 0.2, 0.2, 1.0)),
            np.array((0.5, 0.5, 0.5, 1.0)),
            64,
        )
        cube.setMaterial(m_cube)
        cube.renderingRouting = "lighting"
        self.addChild(cube)

        # Cylinder
        cylinder = Component(Point((0, 0, 0)), DisplayableCylinder(shaderProg, 0.5, 1, 36))
        m_cylinder = Material(
            np.array((0.1, 0.1, 0.1, 1.0)),
            np.array((0.2, 0.8, 0.2, 1.0)),
            np.array((0.7, 0.7, 0.7, 1.0)),
            64,
        )
        cylinder.setMaterial(m_cylinder)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        # Ellipsoid
        ellipsoid = Component(Point((2, 0, 0)), DisplayableEllipsoid(shaderProg, 0.4, 0.4, 0.4, 36, 36))
        m_ellipsoid = Material(
            np.array((0.1, 0.1, 0.1, 1.0)),
            np.array((0.2, 0.2, 0.8, 1.0)),
            np.array((0.6, 0.6, 0.6, 1.0)),
            32,
        )
        ellipsoid.setMaterial(m_ellipsoid)
        ellipsoid.renderingRouting = "lighting"
        self.addChild(ellipsoid)

        # Lights
        l0 = Light(
            self.lightPos(self.lRadius, self.lAngles[0], self.lTransformations[0]),
            np.array((*ColorType.SOFTRED, 1.0)),
        )
        lightCube0 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTRED))
        lightCube0.renderingRouting = "vertex"

        l1 = Light(
            self.lightPos(self.lRadius, self.lAngles[0], self.lTransformations[0]),
            np.array((*ColorType.SOFTBLUE, 1.0)),
        )
        lightCube1 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTBLUE))
        lightCube1.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.addChild(lightCube1)
        self.lights = [l0, l1]
        self.lightCubes = [lightCube0, lightCube1]

    def lightPos(self, radius, thetaAng, transformationMatrix):
        r = np.zeros(4)
        r[0] = radius * math.cos(thetaAng / 180 * math.pi)
        r[2] = radius * math.sin(thetaAng / 180 * math.pi)
        r[3] = 1
        r = transformationMatrix @ r
        return r[0:3]

    def animationUpdate(self):
        self.lAngles[0] = (self.lAngles[0] + 0.5) % 360
        for i, v in enumerate(self.lights):
            lPos = self.lightPos(self.lRadius, self.lAngles[0], self.lTransformations[0])
            self.lightCubes[i].setCurrentPosition(Point(lPos))
            self.lights[i].setPosition(lPos)
            self.shaderProg.setLight(i, v)

        for c in self.children:
            if isinstance(c, Animation):
                c.animationUpdate()

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
