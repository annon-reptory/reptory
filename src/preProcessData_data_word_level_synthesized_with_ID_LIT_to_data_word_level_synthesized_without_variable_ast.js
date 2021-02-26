const fs = require("fs");

const parser = require('./js-parsers/utils');

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

function getCallee(call) {
    const calleeName = call.callee;
    const calleeType = call.original.callee;

    return getIdOrLit(calleeType) === "LIT" ?
        "Literal " + calleeName + " "
        : "Identifier " + calleeName + " ";
}

function getArg1(call) {
    const arg1 = call.original.arguments[0];
    return getIdOrLit(arg1) === "LIT" ?
        "Literal "    + call.synthesizedArgumentTypes[0] + " " :
        "Identifier " + call.synthesizedArgumentTypes[0] + " ";
}

function getArg2(call) {
    const arg2 = call.original.arguments[1];
    return getIdOrLit(arg2) === "LIT" ?
        "Literal "    + call.synthesizedArgumentTypes[1] + " " :
        "Identifier " + call.synthesizedArgumentTypes[1] + " ";
}

fs.createReadStream('./dataset/data-test-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (call) {

        const currentCall = call.original;
        const baseAndCallee = call.base ? call.base + " . " + call.callee : call.callee;

        var baseAndCalleeAst = call.base ? " MemberExpression "+ getBase(call) + " " + getCallee(call) : getCallee(call);
        const correctCall = `Program ExpressionStatement CallExpression  
                    ${baseAndCalleeAst} 
                    ${getArg1(call)} 
                    ${getArg2(call)}`;

        const buggyCall = baseAndCallee
            + " "
            + "("
            + " "
            + getIdOrLit(currentCall.arguments[1])
            + " "
            + call.synthesizedArgumentTypes[1]
            + ","
            + " "
            + getIdOrLit(currentCall.arguments[0])
            + " "
            + call.synthesizedArgumentTypes[0]
            + " "
            + ")";

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
// end: handle the test calls

// handle the train calls
var index = 0;
fs.createReadStream('./dataset/data-training-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (call) {

        const currentCall = call.original;
        const baseAndCallee = call.base ? call.base + " . " + call.callee : call.callee;

        var baseAndCalleeAst = call.base ? " MemberExpression "+ getBase(call) + " " + getCallee(call) : getCallee(call);
        const correctCall = `Program ExpressionStatement CallExpression  
                    ${baseAndCalleeAst} 
                    ${getArg1(call)} 
                    ${getArg2(call)}`;

        let buggyCall = baseAndCallee
            + " "
            + "("
            + " "
            + getIdOrLit(currentCall.arguments[1])
            + " "
            + call.synthesizedArgumentTypes[1]
            + " "
            + ","
            + " "
            + getIdOrLit(currentCall.arguments[0])
            + " "
            + call.synthesizedArgumentTypes[0]
            + " "
            + ")";

        const isDevSet = index % 10 == 0;
        index = index + 1;
        if (isDevSet) {
            correctDev.push(parser.stem(correctCall))
            buggyDev.push(parser.stem(buggyCall))
        } else {
            correctTrain.push(parser.stem(correctCall))
            buggyTrain.push(parser.stem(buggyCall))
        }

        return currentCall;Ø
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