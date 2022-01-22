var esprima = require('esprima'); 
var esquery = require('esquery');
var ast = esprima.parse('function hello () {var a = 5; var dooo = 9; var fooo = 89;} function hellor () {var b = 7; var r = 7;}function world () {var b = 3; }');

var func = esquery(ast, ':matches([id.name=hello] > :first-child, :last-child)');

console.log(func);
