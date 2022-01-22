var assert = require('assert');
var tokenization = require('../code-representations/tokenization_utils')

describe('enhanced word tokenization', function () {

    describe("can handle camel case", function () {
        it('should handle camelcase', function() {
            assert.equal(tokenization.camelCaseSplit("camelCase"), "camel <CAMEL> Case");
            assert.equal(tokenization.camelCaseSplit("camelCase"), "camel <CAMEL> Case")
            assert.equal(tokenization.camelCaseSplit("notcamelcase"), "notcamelcase")
            assert.equal(tokenization.camelCaseSplit("CamelCaseXYZ"), "Camel <CAMEL> Case <CAMEL> XYZ")
            assert.equal(tokenization.camelCaseSplit("CamelCaseXYZa"), "Camel <CAMEL> Case <CAMEL> XY <CAMEL> Za")
            assert.equal(tokenization.camelCaseSplit("XYZCamelCase"), "XYZ <CAMEL> Camel <CAMEL> Case")
            assert.equal(tokenization.camelCaseSplit(""), "")
            assert.equal(tokenization.camelCaseSplit(" "), " ")
            assert.equal(tokenization.camelCaseSplit("   "), "   ")
            assert.equal(tokenization.camelCaseSplit("lower"), "lower")
            assert.equal(tokenization.camelCaseSplit("UPPER"), "UPPER")
            assert.equal(tokenization.camelCaseSplit("Initial"), "Initial")
            assert.equal(tokenization.camelCaseSplit("dromedaryCase"), "dromedary <CAMEL> Case")
            assert.equal(tokenization.camelCaseSplit("ABCWordDEF"), "ABC <CAMEL> Word <CAMEL> DEF")
            assert.equal(tokenization.camelCaseSplit("aCamelCaseWordT"), "a <CAMEL> Camel <CAMEL> Case <CAMEL> Word <CAMEL> T")
            assert.equal(tokenization.camelCaseSplit("CamelCaseWordT"), "Camel <CAMEL> Case <CAMEL> Word <CAMEL> T")
            assert.equal(tokenization.camelCaseSplit("CamelCaseWordTa"), "Camel <CAMEL> Case <CAMEL> Word <CAMEL> Ta")
            assert.equal(tokenization.camelCaseSplit("aCamelCaseWordTa"), "a <CAMEL> Camel <CAMEL> Case <CAMEL> Word <CAMEL> Ta")
            assert.equal(tokenization.camelCaseSplit("Ta"), "Ta")
            assert.equal(tokenization.camelCaseSplit("aT"), "a <CAMEL> T")
            assert.equal(tokenization.camelCaseSplit("a"), "a")
            assert.equal(tokenization.camelCaseSplit("T"), "T")
            assert.equal(tokenization.camelCaseSplit("FOOBar"), "FOO <CAMEL> Bar")
        });
    })

    describe("can handle snake case ", function () {
        it('should handle snake case', function() {
            assert.equal(tokenization.snakeCaseSplit("snake_case"), "snake case")
            assert.equal(tokenization.snakeCaseSplit("notsnakecase"), "notsnakecase")
        });
    })

    describe("can handle mixed case", function () {
        it('should handle camel case mixed with snake case', function() {
            assert.equal(tokenization.tokenize("camelCase_snake_case"), "camel <CAMEL> Case snake case")
            assert.equal(tokenization.tokenize("camelCasenotsnakecase"), "camel <CAMEL> Casenotsnakecase")
        });

        it('should handle camel case mixed with snake case', function() {
            assert.equal(tokenization.tokenize("camelCase_snake_case_123"), "camel <CAMEL> Case snake case 123")
            assert.equal(tokenization.tokenize("camelCasenotsnakecase123456789"), "camel <CAMEL> Casenotsnakecase 123456789")
            assert.equal(tokenization.tokenize("nonumber"), "nonumber")
            assert.equal(tokenization.tokenize("single digit number 1"), "single digit number 1")
            assert.equal(tokenization.tokenize("single digit number1"), "single digit number 1")
            assert.equal(tokenization.tokenize("double digit number 12"), "double digit number 12")
            assert.equal(tokenization.tokenize("double digit number12"), "double digit number 12")
            assert.equal(tokenization.tokenize("multi digit number 1285782"), "multi digit number 1285782")
            assert.equal(tokenization.tokenize("multi digit number128578"), "multi digit number 128578")
            assert.equal(tokenization.camelCaseSplit("CamelCaseTest123"), "Camel <CAMEL> Case <CAMEL> Test123")
        });

        it('should handle camel case mixed with snake case and space', function() {
            assert.equal(tokenization.tokenize(" camelCase_snake_case_123"), "camel <CAMEL> Case snake case 123")
            assert.equal(tokenization.tokenize(" camelCasenotsnakecase123456789 "), "camel <CAMEL> Casenotsnakecase 123456789")
            assert.equal(tokenization.tokenize("  nonumber"), "nonumber")
            assert.equal(tokenization.tokenize("single digit number 1   "), "single digit number 1")
            assert.equal(tokenization.tokenize("  single digit number1  "), "single digit number 1")
            assert.equal(tokenization.tokenize("double   digit number 12"), "double digit number 12")
            assert.equal(tokenization.tokenize("double   digit     number12"), "double digit number 12")
            assert.equal(tokenization.tokenize("multi   digit  number      1285782"), "multi digit number 1285782")
            assert.equal(tokenization.tokenize("multi digit               number128578"), "multi digit number 128578")
            assert.equal(tokenization.tokenize("CamelCaseTest123     "), "Camel <CAMEL> Case <CAMEL> Test 123")
        });
    })
})
