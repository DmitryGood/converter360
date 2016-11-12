from unittest import TestCase
from Utils3D.Screen3D import Screen3D, CylindricCoordinates
from Utils3D.Vector3D import Vector3D

import logging

class TestScreen(TestCase):
    def test_Screen(self):
        s = Screen3D(100, 80, 10, 10)
        self.assertTrue(s is not None)

    def test_initScreen(self):
        s = Screen3D(100, 80, 10, 10)
        s.initScreen(CylindricCoordinates(50, 0, 90))
        v = s.get_screen_vector_by_coord(0, 0)
        self.assertEqual(v, Vector3D(50, 50, 40))
        v1 = s.get_screen_vector_by_coord(10, 10)
        self.assertEqual(v1, Vector3D( 50, -50, -40))

        v2 = s.get_screen_vector_by_coord(5, 5)
        #self.assertEqual(v2, Vector3D( 50, 0, 0))

    def test_get_cylindric_coordinates(self):
        s = Screen3D(100, 80, 10, 10)
        s.initScreen(CylindricCoordinates(50, 0, 90))
        v = s.get_screen_vector_by_coord(0, 0)
        cyl = s.get_cylindric_coordinates(v)
        self.assertAlmostEquals(cyl.getDegrees()[0], 81, delta=.3)