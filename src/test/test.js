var assert = require('assert');
const tokenize = require('../parse_js_esprima');
var crude_tokenization = require('../crude_tokenization')

String.prototype.splitAndKeep = function(separator, method='seperate'){
    var str = this;
    function splitAndKeep(str, separator, method='seperate'){
        if(method == 'seperate'){
            str = str.split(new RegExp(`(${separator})`, 'g'));
        }else if(method == 'infront'){
            str = str.split(new RegExp(`(?=${separator})`, 'g'));
        }else if(method == 'behind'){
            str = str.split(new RegExp(`(.*?${separator})`, 'g'));
            str = str.filter(function(el){return el !== "";});
        }
        return str;
    }
    if(Array.isArray(separator)){
        var parts = splitAndKeep(str, separator[0], method);
        for(var i = 1; i < separator.length; i++){
            var partsTemp = parts;
            parts = [];
            for(var p = 0; p < partsTemp.length; p++){
                parts = parts.concat(splitAndKeep(partsTemp[p], separator[i], method));
            }
        }
        return parts;
    }else{
        return splitAndKeep(str, separator, method);
    }
};

OPERATORS = ['>>>=', '>>=', '<<=',].join("")
var OPERATORS = [
    '>>>=',
    '>>=',
    '<<=',
    '|=',
    '^=',
    '&=',
    '+=',
    '-=',
    '*=',
    '/=',
    '%=',
    ';',
    ',',
    '?',
    ':',
    '||',
    '&&',
    '|',
    '^',
    '&',
    '===',
    '==',
    '=',
    '!==',
    '!=',
    '<<',
    '<=',
    '<',
    '>>>',
    '>>',
    '>=',
    '>',
    '++',
    '--',
    '+',
    '-',
    '*',
    '/',
    '%',
    '!',
    '~',
    '.',
    '[',
    ']',
    '{',
    '}',
    '(',
    ')'
];

describe('tokenization', function () {
    describe("can handle space", function () {

        var string = `cm . replaceSelection (

            , null )`

        console.log(string.replace(/\n/g, " "))

    })

    describe('can parse javascript code', function () {

        it('can parse when first parameter is not present', function () {
            string = "elt(a, b, c)"

            var words = string.split("(,");
            console.log(string.split("(,"))

            words.forEach(token => console.log(token));

            var string = "elt(a, b, c)";
            var parts = string.split(/(?<!\w)\s*(?=\w)|(?<=\w)\s*(?!\w)/);
            console.log(parts);


            string = "elt(a,>>>=, b, c)";
            var parts = string.split(/([-+(),*/:? >>>=,>>=,<<=,|=,^=,&=,+=,-=,*=,/=,%=,;,,,?,:,||,&&,|,^,&,===,==,=,!==,!=,<<,<=,<,>>>,>>,>=,>,++,--,+,-,*,/,%,!,~,.,\[,\],{,},(,)?  ])/g)
            console.log(parts)

        });
    });
});
