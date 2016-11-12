from unittest import TestCase
import math
from Utils3D.Vector3D import Vector3D


class TestVector3D(TestCase):

    def test_basic(self):
        a = Vector3D( 1, 2, 3)
        self.assertEqual(a.magnitude(), math.sqrt(14), "Magnitude - OK")
        b = Vector3D( 1, 1, 1)
        t = 1 / math.sqrt(3)
        self.assertEqual(b.normal(), Vector3D(t , t, t), "Normalization - OK")
        self.assertEqual( a + b, Vector3D( 2, 3, 4), " Sum - OK")
        self.assertEqual( a * 3, Vector3D( 3, 6, 9), "Mult by scalar - OK")

    def test_vector(self):
        a = Vector3D(2, 0, 0)
        b = Vector3D(1, 1, 0)
        self.assertAlmostEquals(a * b, a.magnitude()*b.magnitude()*math.cos(math.pi/4), delta=0.000000001)
        self.assertAlmostEquals(a & b, a.magnitude() * b.magnitude() * math.cos(math.pi / 4), delta=0.000000001)

        self.assertEqual( a ** b, Vector3D( 0, 0, 2), "Vector multiplication - OK")



