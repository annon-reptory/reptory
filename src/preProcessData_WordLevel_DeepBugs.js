const fs = require("fs");

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

// start: handle test all calls and build dataset-test.json
var datasetTestAllCalls = fs.readFileSync("dataset/data-test-all-calls.json");
//var datasetTrainingAllCalls = fs.readFileSync("dataset/data-training-all-calls.json");

var datasetTestAllCallsJson = JSON.parse(datasetTestAllCalls);
// var datasetTrainingAllCallsJson = JSON.parse(datasetTrainingAllCalls);

const buggyTrain = [];
const correctTrain = [];

var buggyDev = [];
var correctDev = [];

var buggyTest = [];
var correctTest = [];

const examples = [correctTrain, buggyTrain, correctTest, buggyTest, correctDev, buggyDev];
const examplesTrain = [correctTrain, buggyTrain, correctDev, buggyDev];
const examplesTest = [correctTest, buggyTest];

//start: handle the test calls
// for (let index = 0; index < datasetTestAllCallsJson.length; index++) {
//     const currentCall = datasetTestAllCallsJson[index]
//
//     const baseAndCallee = currentCall.base ? currentCall.base + "." + currentCall.callee : currentCall.callee
//
//     const correctCall = baseAndCallee
//         + "("
//         + currentCall.arg1
//         + ","
//         + currentCall.arg2
//         + ")";
//
//     const buggy  Call = baseAndCallee
//         + "("
//         + currentCall.arg2
//         + ","
//         + currentCall.arg1
//         + ")";
//
//     correctTest.push(correctCall)
//     buggyTest.push(buggyCall)
//     // console.log(correctCall)
//     // console.log(buggyCall)
// }

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

        correctTest.push(correctCall.replace(/:/g, ' ').replace(/\n/g, " "))
        buggyTest.push(buggyCall.replace(/:/g, ' ').replace(/\n/g, " "))

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
/*
for (let index = 0; index < datasetTrainingAllCallsJson.length; index++) {
    const currentCall = datasetTrainingAllCallsJson[index]

    const baseAndCallee = currentCall.base ? currentCall.base + "." + currentCall.callee : currentCall.callee

    const correctCall = baseAndCallee
        + "("
        + currentCall.arg1
        + ","
        + currentCall.arg2
        + ")";

    const buggyCall = baseAndCallee
        + "("
        + currentCall.arg2
        + ","
        + currentCall.arg1
        + ")";


    const isDevSet = index % 10 == 0;
    if (isDevSet) {
        correctDev.push(correctCall)
        buggyDev.push(buggyCall)
    } else {
        correctTrain.push(correctCall)
        buggyTrain.push(buggyCall)
    }

    // console.log(correctCall)
    // console.log(buggyCall)
}

// end: handle test all calls and build dataset-test.json

for (var i = 0; i < examples.length; i++) {
    const exampleSet = examples[i];
    var dir = dirs[i]
    for (var j = 0; j < exampleSet.length; j++) {
        fs.writeFileSync(dir + j + '.js', exampleSet[j], function (err) {
            if (err) throw err
            console.log('Processed ' + j + '.js' + ' in ' + dir)
        })
    }
}
 */


var index = 0;
fs.createReadStream('./dataset/data-training-all-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (call) {
        //console.log(currentCall);
        const currentCall = call.original;
        const baseAndCallee = currentCall.base ? currentCall.base + " . " + currentCall.callee : currentCall.callee

        let correctCall = baseAndCallee
            + " "
            + "("
            + " "
            + currentCall.arguments[0]
            + " "
            + ","
            + " "
            + currentCall.arguments[1]
            + " "
            + ")";

        let buggyCall = baseAndCallee
            + " "
            + "("
            + " "
            + currentCall.arguments[1]
            + " "
            + ","
            + " "
            + currentCall.arguments[0]
            + " "
            + ")";

        correctCall = correctCall.replace(/:/g, ' ')
        buggyCall = buggyCall.replace(/:/g, ' ')

        const isDevSet = index % 10 == 0;
        index = index + 1;
        if (isDevSet) {
            correctDev.push(correctCall.replace(/:/g, ' ').replace(/\n/g, " "))
            buggyDev.push(buggyCall.replace(/:/g, ' ').replace(/\n/g, " "))
        } else {
            correctTrain.push(correctCall.replace(/:/g, ' ').replace(/\n/g, " "))
            buggyTrain.push(buggyCall.replace(/:/g, ' ').replace(/\n/g, " "))
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

