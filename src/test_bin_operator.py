from unittest import TestCase
from binoperator1b import camel_case_split, snake_case_split, stem


class TestBinOps(TestCase):
    def test_camel_case_split(self):
        self.assertEqual(camel_case_split("camelCase"), "camel <CAMEL> Case")
        self.assertEqual(camel_case_split("notcamelcase"), "notcamelcase")
        self.assertEqual(camel_case_split("CamelCaseXYZ"), "Camel <CAMEL> Case <CAMEL> XYZ")
        self.assertEqual(camel_case_split("CamelCaseXYZa"), "Camel <CAMEL> Case <CAMEL> XY <CAMEL> Za")
        self.assertEqual(camel_case_split("XYZCamelCase"), "XYZ <CAMEL> Camel <CAMEL> Case")
        self.assertEqual(camel_case_split(""), "")
        self.assertEqual(camel_case_split(" "), " ")
        self.assertEqual(camel_case_split("   "), "   ")
        self.assertEqual(camel_case_split("lower"), "lower")
        self.assertEqual(camel_case_split("UPPER"), "UPPER")
        self.assertEqual(camel_case_split("Initial"), "Initial")
        self.assertEqual(camel_case_split("dromedaryCase"), "dromedary <CAMEL> Case")
        self.assertEqual(camel_case_split("ABCWordDEF"), "ABC <CAMEL> Word <CAMEL> DEF")
        self.assertEqual(camel_case_split("CamelCaseTest123"), "Camel <CAMEL> Case <CAMEL> Test123")
        self.assertEqual(camel_case_split("aCamelCaseWordT"), "a <CAMEL> Camel <CAMEL> Case <CAMEL> Word <CAMEL> T")
        self.assertEqual(camel_case_split("CamelCaseWordT"), "Camel <CAMEL> Case <CAMEL> Word <CAMEL> T")
        self.assertEqual(camel_case_split("CamelCaseWordTa"), "Camel <CAMEL> Case <CAMEL> Word <CAMEL> Ta")
        self.assertEqual(camel_case_split("aCamelCaseWordTa"), "a <CAMEL> Camel <CAMEL> Case <CAMEL> Word <CAMEL> Ta")
        self.assertEqual(camel_case_split("Ta"), "Ta")
        self.assertEqual(camel_case_split("aT"), "a <CAMEL> T")
        self.assertEqual(camel_case_split("a"), "a")
        self.assertEqual(camel_case_split("T"), "T")
        self.assertEqual(camel_case_split("FOOBar"), "FOO <CAMEL> Bar")

    def test_snake_case(self):
        self.assertEqual(snake_case_split("snake_case"), "snake case")
        self.assertEqual(snake_case_split("notsnakecase"), "notsnakecase")

    def test_camel_case_and_snake_case(self):
        self.assertEqual(stem("camelCase_snake_case"), "camel <CAMEL> Case snake case")
        self.assertEqual(stem("camelCasenotsnakecase"), "camel <CAMEL> Casenotsnakecase")

    def test_camel_case_and_snake_case_and_numbers(self):
        self.assertEqual(stem("camelCase_snake_case_123"), "camel <CAMEL> Case snake case 123")
        self.assertEqual(stem("camelCasenotsnakecase123456789"), "camel <CAMEL> Casenotsnakecase 123456789")
        self.assertEqual(stem("nonumber"), "nonumber")
        self.assertEqual(stem("single digit number 1"), "single digit number 1")
        self.assertEqual(stem("single digit number1"), "single digit number 1")
        self.assertEqual(stem("double digit number 12"), "double digit number 12")
        self.assertEqual(stem("double digit number12"), "double digit number 12")
        self.assertEqual(stem("multi digit number 1285782"), "multi digit number 1285782")
        self.assertEqual(stem("multi digit number128578"), "multi digit number 128578")
