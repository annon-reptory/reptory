const fs = require("fs");

const ast2seq = require('./ast2seq');
const parser = require('./js-parsers/utils');
const esprima = require('esprima');

const PINO = require('pino');
const LOGGER = PINO({
    prettyPrint: {colorize: true}
})

const TrainSourceCorrectDir = "./TrainSourceCorrect/";
const TrainSourceBuggyDir = "./TrainSourceBuggy/";

const DevSourceCorrectDir = "./DevSourceCorrect/";
const DevSourceBuggyDir = "./DevSourceBuggy/";

const TestSourceCorrectDir = "./TestSourceCorrect/";
const TestSourceBuggyDir = "./TestSourceBuggy/";

const dirs = [TrainSourceCorrectDir, TrainSourceBuggyDir, TestSourceCorrectDir, TestSourceBuggyDir, DevSourceCorrectDir, DevSourceBuggyDir];
const dirsTrain = [TrainSourceCorrectDir, TrainSourceBuggyDir, DevSourceCorrectDir, DevSourceBuggyDir];
const dirsTest = [TestSourceCorrectDir, TestSourceBuggyDir];

for (let i in dirs) {
    const dir = dirs[i]
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir)
    }
}

const buggyTrain = [];
const correctTrain = [];

var buggyDev = [];
var correctDev = [];

var buggyTest = [];
var correctTest = [];

const examplesTrain = [correctTrain, buggyTrain, correctDev, buggyDev];
const examplesTest = [correctTest, buggyTest];

fileStream = fs.createReadStream("dataset/data-test-all-calls.json", {encoding: 'utf8'});
var JSONStream = require('JSONStream');
var es = require('event-stream');

function getIdOrLit(input) {
    return input.split(":")[0];
}

function getBase(call) {
    const baseName = call.base
    const baseType = call.original.base;

    return getIdOrLit(baseType) === "LIT" ?
        "Literal " + baseName + " "
        : "Identifier " + baseName + " ";
}

function getCallee(call){
    const calleeName = call.callee;
    const calleeType = call.original.callee;

    return getIdOrLit(calleeType) === "LIT" ?
        "Literal " + calleeName + " "
        : "Identifier " + calleeName + " ";
}

function getArg1(call) {
    const arg1 = call.original.arguments[0];
    return getIdOrLit(arg1) === "LIT" ? "Literal " + call.arg1 + " "
        : "Identifier " + call.arg1 + " ";
}

function getArg2(call) {
    const arg2 = call.original.arguments[1];
    return getIdOrLit(arg2) === "LIT" ? "Literal " + call.arg2 + " "
        : "Identifier " + call.arg2 + " ";
}

fs.createReadStream('./dataset/data-test-all-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (call) {

        const currentCall = call.original;
        var baseAndCallee = call.base ? getBase(call) + " " + getCallee(call) : getCallee(call);

        ast2seq.walk(call.correct_call);
        const ast_tree = tokenize_esprima("sum(aa, bb)");
        const ast_seq = walk(ast_tree)

        const correctCall = `Program ExpressionStatement CallExpression MemberExpression 
                    ${baseAndCallee} 
                    ${getArg1(call)} 
                    ${getArg2(call)}`;

        const buggyCall = `Program ExpressionStatement CallExpression MemberExpression 
                    ${baseAndCallee} 
                    ${getArg2(call)} 
                    ${getArg1(call)}`;

        correctTest.push(parser.stem(correctCall))
        buggyTest.push(parser.stem(buggyCall))

        return currentCall;
    })).on('end', function () {
    console.log("finished running....");
    LOGGER.info({
        'Test Stats:': {
            "buggy instances": buggyTest.length,
            "correct instances": correctTest.length
        }
    });

    // write dataset
    for (var i = 0; i < examplesTest.length; i++) {
        const exampleSet = examplesTest[i];
        var dir = dirsTest[i];
        for (var j = 0; j < exampleSet.length; j++) {
            fs.writeFileSync(dir + j + '.js', exampleSet[j], function (err) {
                if (err) throw err;
                console.log('Processed ' + j + '.js' + ' in ' + dir);
            })
        }
    }

});

//end: handle the test calls

//handle the train calls
var index = 0;
fs.createReadStream('./dataset/data-training-all-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (call) {

        const currentCall = call.original;
        var baseAndCallee = call.base ? getBase(call) + " " + getCallee(call) : getCallee(call);

        const correctCall = `Program ExpressionStatement CallExpression MemberExpression 
                    ${baseAndCallee} 
                    ${getArg1(call)} 
                    ${getArg2(call)}`;

        const buggyCall = `Program ExpressionStatement CallExpression MemberExpression 
                    ${baseAndCallee} 
                    ${getArg2(call)} 
                    ${getArg1(call)}`;

        const isDevSet = index % 10 == 0;
        index = index + 1;
        if (isDevSet) {
            correctDev.push(parser.stem(correctCall))
            buggyDev.push(parser.stem(buggyCall))
        } else {
            correctTrain.push(parser.stem(correctCall))
            buggyTrain.push(parser.stem(buggyCall))
        }

        return currentCall;
    })).on('end', function () {
    console.log("finished running....");

    LOGGER.info({
        'Train Stats': {
            'buggy instances': buggyTrain.length,
            'correct instances': correctTrain.length
        }
    });

    LOGGER.info({
            'Dev Stats:': {
                "buggy instances": buggyDev.length,
                "correct instances": correctDev.length
            }
        }
    );

    // write dataset
    for (var i = 0; i < examplesTrain.length; i++) {
        const exampleSet = examplesTrain[i];
        var dir = dirsTrain[i]
        for (var j = 0; j < exampleSet.length; j++) {
            fs.writeFileSync(dir + j + '.js', exampleSet[j], function (err) {
                if (err) throw err
                console.log('Processed ' + j + '.js' + ' in ' + dir)
            })
        }
    }
});
