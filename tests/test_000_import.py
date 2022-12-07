#!/usr/bin/env python

"""Tests for `nodeeditor` package."""


import unittest

from nodeeditor.Escena import Escena


class TestTemplate(unittest.TestCase):
    """Tests for `nodeeditor` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Probando si el metodo elementos_modificados de Escena funciona apropiadamente."""
        assert(hasattr(Escena, 'elementos_modificados'))
