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

fileStream = fs.createReadStream("dataset/data-test-all-calls.json", {encoding: 'utf8'});
var JSONStream = require('JSONStream');
var es = require('event-stream');

fs.createReadStream('./dataset/data-test-all-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (currentCall) {
        const baseAndCallee = currentCall.base ? currentCall.base + " . " + currentCall.callee : currentCall.callee;

        const correctCall = baseAndCallee
            + " "
            + "("
            + " "
            + currentCall.arg1
            + " "
            + ","
            + " "
            + currentCall.arg2
            + " "
            + ")";

        const buggyCall = baseAndCallee
            + " "
            + "("
            + " "
            + currentCall.arg2
            + " "
            + ","
            + " "
            + currentCall.arg1
            + " "
            + ")";

        correctTest.push(parser.stem(correctCall))
        buggyTest.push(parser.stem(buggyCall).replace(/(\u0085|\u000a\u000d|\u2028|\u2029)/gm," ").replace(/[\x00-\x1F\x7F-\x9F]/g, "").replace(/:/g, ' ').replace(/(\r\n|\n|\r)/gm," ").replace(/\s\s+/g, ' ').replace(/[\r\n\x0B\x0C\u0085\u2028\u2029]+/g," ").trim())

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
    .pipe(es.mapSync(function (currentCall) {

        const baseAndCallee = currentCall.base ? currentCall.base + " . " + currentCall.callee : currentCall.callee;

        const correctCall = baseAndCallee
            + " "
            + "("
            + " "
            + currentCall.arg1
            + " "
            + ","
            + " "
            + currentCall.arg2
            + " "
            + ")";

        const buggyCall = baseAndCallee
            + " "
            + "("
            + " "
            + currentCall.arg2
            + " "
            + ","
            + " "
            + currentCall.arg1
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
