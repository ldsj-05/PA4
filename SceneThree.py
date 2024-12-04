"""
Define a scene with a cylinder, torus, and ellipsoid
First version in 12/03/2024

:author: micou(Zezhou Sun)
:version: 2024.12.03
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

from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableTorus import DisplayableTorus
from DisplayableCube import DisplayableCube
from DisplayableCylinder import DisplayableCylinder


class SceneThree(Component, Animation):
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

        # Cylinder (Teal)
        cylinder = Component(Point((-3, 0, 0)), DisplayableCylinder(shaderProg, 1.0, 1.5, 36))
        m_cylinder = Material(
            np.array((0.1, 0.1, 0.1, 1.0)),
            np.array((0.0, 0.7, 0.7, 1.0)),  # Teal
            np.array((0.4, 0.7, 0.7, 1.0)),
            64,
        )
        cylinder.setMaterial(m_cylinder)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        # Torus (Pink, Moving)
        self.torus = Component(Point((0, 0, 0)), DisplayableTorus(shaderProg, 0.5, 1, 36, 36))
        m_torus = Material(
            np.array((0.1, 0.1, 0.1, 1.0)),
            np.array((1.0, 0.0, 0.5, 1.0)),  # Pink
            np.array((0.8, 0.5, 0.6, 1.0)),
            64,
        )
        self.torus.setMaterial(m_torus)
        self.torus.renderingRouting = "lighting"
        self.addChild(self.torus)

        # Ellipsoid (Yellow)
        ellipsoid = Component(Point((3, 0, 0)), DisplayableEllipsoid(shaderProg, 0.4, 0.6, 0.4, 36, 36))
        m_ellipsoid = Material(
            np.array((0.1, 0.1, 0.1, 1.0)),
            np.array((1.0, 1.0, 0.0, 1.0)),  # Yellow
            np.array((0.9, 0.8, 0.4, 1.0)),
            32,
        )
        ellipsoid.setMaterial(m_ellipsoid)
        ellipsoid.renderingRouting = "lighting"
        self.addChild(ellipsoid)

        # Lights
        l0 = Light(
            self.lightPos(self.lRadius, self.lAngles[0], self.lTransformations[0]),
            np.array((0.0, 1.0, 1.0, 1.0)),  # Cyan
        )
        lightCube0 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.CYAN))
        lightCube0.renderingRouting = "vertex"

        l1 = Light(
            self.lightPos(self.lRadius, self.lAngles[0], self.lTransformations[0]),
            np.array((0.5, 0.0, 0.5, 1.0)),  # Purple
        )
        lightCube1 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.PURPLE))
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
        # Move torus up and down using a sine wave
        time = (self.lAngles[0] / 360) * 2 * math.pi
        self.torus.setCurrentPosition(Point((0, math.sin(time), 0)))

        # Update light positions
        self.lAngles[0] = (self.lAngles[0] + 0.5) % 360
        for i, v in enumerate(self.lights):
            lPos = self.lightPos(self.lRadius, self.lAngles[0], self.lTransformations[0])
            self.lightCubes[i].setCurrentPosition(Point(lPos))
            self.lights[i].setPosition(lPos)
            self.shaderProg.setLight(i, v)

        # Update animations for children
        for c in self.children:
            if isinstance(c, Animation):
                c.animationUpdate()

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
