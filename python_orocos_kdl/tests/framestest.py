# Copyright  (C)  2007  Ruben Smits <ruben dot smits at mech dot kuleuven dot be>

# Version: 1.0
# Author: Ruben Smits <ruben dot smits at mech dot kuleuven dot be>
# Maintainer: Ruben Smits <ruben dot smits at mech dot kuleuven dot be>
# URL: http://www.orocos.org/kdl

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import unittest
from PyKDL import Wrench, Twist, Vector, Rotation, Frame, dot
from math import radians, sqrt


def wrench_test(test, w):
    test.assertEqual(2 * w - w, w)
    test.assertEqual(w * 2 - w, w)
    test.assertEqual(w + w + w - 2 * w, w)
    w2 = Wrench(w)
    test.assertEqual(w, w2)
    w2 += w
    test.assertEqual(2 * w, w2)
    w2 -= w
    test.assertEqual(w, w2)
    w.ReverseSign()
    test.assertEqual(w, -w2)


def twist_test(test, t):
    test.assertEqual(2 * t - t, t)
    test.assertEqual(t * 2 - t, t)
    test.assertEqual(t + t + t - 2 * t, t)
    t2 = Twist(t)
    test.assertEqual(t, t2)
    t2 += t
    test.assertEqual(2 * t, t2)
    t2 -= t
    test.assertEqual(t, t2)
    t.ReverseSign()
    test.assertEqual(t, -t2)


def vector_test(test, v):
    test.assertEqual(2 * v - v, v)
    test.assertEqual(v * 2 - v, v)
    test.assertEqual(v + v + v - 2 * v, v)
    v2 = Vector(v)
    test.assertEqual(v, v2)
    v2 += v
    test.assertEqual(2 * v, v2)
    v2 -= v
    test.assertEqual(v, v2)
    v2.ReverseSign()
    test.assertEqual(v, -v2)


class FramesTestFunctions(unittest.TestCase):
    def testVector(self):
        v = Vector(3, 4, 5)
        vector_test(self, v)
        v = Vector.Zero()
        vector_test(self, v)

    def testTwist(self):
        t = Twist(Vector(6, 3, 5), Vector(4, -2, 7))
        twist_test(self, t)
        t = Twist.Zero()
        twist_test(self, t)
        t = Twist(Vector(0, -9, -3), Vector(1, -2, -4))
        twist_test(self, t)

    def testWrench(self):
        w = Wrench(Vector(7, -1, 3), Vector(2, -3, 3))
        wrench_test(self, w)
        w = Wrench.Zero()
        wrench_test(self, w)
        w = Wrench(Vector(2, 1, 4), Vector(5, 3, 1))
        wrench_test(self, w)

    def testRotation(self):
        v = Vector(3, 4, 5)
        a = radians(10)
        b = radians(20)
        c = radians(30)
        w = Wrench(Vector(7, -1, 3), Vector(2, -3, 3))
        t = Twist(Vector(6, 3, 5), Vector(4, -2, 7))
        R = Rotation.RPY(a, b, c)

        self.assertAlmostEqual(dot(R.UnitX(), R.UnitX()), 1.0, 15)
        self.assertEqual(dot(R.UnitY(), R.UnitY()), 1.0)
        self.assertEqual(dot(R.UnitZ(), R.UnitZ()), 1.0)
        self.assertAlmostEqual(dot(R.UnitX(), R.UnitY()), 0.0, 15)
        self.assertAlmostEqual(dot(R.UnitX(), R.UnitZ()), 0.0, 15)
        self.assertEqual(dot(R.UnitY(), R.UnitZ()), 0.0)
        R2 = Rotation(R)
        self.assertEqual(R, R2)
        self.assertAlmostEqual((R * v).Norm(), v.Norm(), 14)
        self.assertEqual(R.Inverse(R * v), v)
        self.assertEqual(R.Inverse(R * t), t)
        self.assertEqual(R.Inverse(R * w), w)
        self.assertEqual(R * R.Inverse(v), v)
        self.assertEqual(R * Rotation.Identity(), R)
        self.assertEqual(Rotation.Identity() * R, R)
        self.assertEqual(R * (R * (R * v)), (R * R * R) * v)
        self.assertEqual(R * (R * (R * t)), (R * R * R) * t)
        self.assertEqual(R * (R * (R * w)), (R * R * R) * w)
        self.assertEqual(R * R.Inverse(), Rotation.Identity())
        self.assertEqual(R.Inverse() * R, Rotation.Identity())
        self.assertEqual(R.Inverse() * v, R.Inverse(v))
        (ra, rb, rc) = R.GetRPY()
        self.assertEqual(ra, a)
        self.assertEqual(rb, b)
        self.assertEqual(rc, c)
        R = Rotation.EulerZYX(a, b, c)
        (ra, rb, rc) = R.GetEulerZYX()
        self.assertEqual(ra, a)
        self.assertEqual(rb, b)
        self.assertEqual(rc, c)
        R = Rotation.EulerZYZ(a, b, c)
        (ra, rb, rc) = R.GetEulerZYZ()
        self.assertEqual(ra, a)
        self.assertEqual(rb, b)
        self.assertAlmostEqual(rc, c, 15)
        (angle, v2) = R.GetRotAngle()
        R2 = Rotation.Rot(v2, angle)
        self.assertEqual(R2, R)
        R2 = Rotation.Rot(v2 * 1e20, angle)
        self.assertEqual(R, R2)
        v2 = Vector(6, 2, 4)
        self.assertAlmostEqual(v2.Norm(), sqrt(dot(v2, v2)), 14)

    def testFrame(self):
        v = Vector(3, 4, 5)
        w = Wrench(Vector(7, -1, 3), Vector(2, -3, 3))
        t = Twist(Vector(6, 3, 5), Vector(4, -2, 7))
        F = Frame(
            Rotation.EulerZYX(radians(10), radians(20), radians(-10)), Vector(4, -2, 1)
        )
        F2 = Frame(F)
        self.assertEqual(F, F2)
        self.assertEqual(F.Inverse(F * v), v)
        self.assertEqual(F.Inverse(F * t), t)
        self.assertEqual(F.Inverse(F * w), w)
        self.assertEqual(F * F.Inverse(v), v)
        self.assertEqual(F * F.Inverse(t), t)
        self.assertEqual(F * F.Inverse(w), w)
        self.assertEqual(F * Frame.Identity(), F)
        self.assertEqual(Frame.Identity() * F, F)
        self.assertEqual(F * (F * (F * v)), (F * F * F) * v)
        self.assertEqual(F * (F * (F * t)), (F * F * F) * t)
        self.assertEqual(F * (F * (F * w)), (F * F * F) * w)
        self.assertEqual(F * F.Inverse(), Frame.Identity())
        self.assertEqual(F.Inverse() * F, Frame.Identity())
        self.assertEqual(F.Inverse() * v, F.Inverse(v))

    def testPickle(self):
        import pickle

        data = {}
        data["v"] = Vector(1, 2, 3)
        data["rot"] = Rotation.RotX(1.3)
        data["fr"] = Frame(data["rot"], data["v"])
        data["tw"] = Twist(data["v"], Vector(4, 5, 6))
        data["wr"] = Wrench(Vector(0.1, 0.2, 0.3), data["v"])

        f = open("/tmp/pickle_test", "wb")
        pickle.dump(data, f)
        f.close()

        f = open("/tmp/pickle_test", "rb")
        data1 = pickle.load(f)
        f.close()

        self.assertEqual(data, data1)
