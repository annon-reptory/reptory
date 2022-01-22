const fs = require("fs");

const parser = require('./js-parsers/utils');
const representations = require('./code-representations/word-tokenization');
var tokenization = require('./code-representations/tokenization_utils')

const PINO = require('pino');
const LOGGER = PINO({
    prettyPrint: {colorize: true}
})

function directoryNames() {
    const TrainSourceCorrectDir = "./TrainSourceCorrect/";
    const TrainSourceBuggyDir = "./TrainSourceBuggy/";

    const DevSourceCorrectDir = "./DevSourceCorrect/";
    const DevSourceBuggyDir = "./DevSourceBuggy/";

    const TestSourceCorrectDir = "./TestSourceCorrect/";
    const TestSourceBuggyDir = "./TestSourceBuggy/";
    return {
        TrainSourceCorrectDir,
        TrainSourceBuggyDir,
        DevSourceCorrectDir,
        DevSourceBuggyDir,
        TestSourceCorrectDir,
        TestSourceBuggyDir
    };
}

const {TrainSourceCorrectDir, TrainSourceBuggyDir, DevSourceCorrectDir, DevSourceBuggyDir, TestSourceCorrectDir, TestSourceBuggyDir} = directoryNames();

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

fileStream = fs.createReadStream("dataset/data-test-calls.json", {encoding: 'utf8'});
var JSONStream = require('JSONStream');
var es = require('event-stream');

//start: handle the test calls
fs.createReadStream('./dataset/data-test-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (currentCall) {
        const { buggyCall, correctCall } = representations.wordTokenizationEnhanced(currentCall);

        correctTest.push(tokenization.tokenize(parser.stem(correctCall)))
        buggyTest.push(tokenization.tokenize(parser.stem(buggyCall)))

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
                console.log('error processing ' + j + '.js' + ' in ' + dir);
            });
        }
    }
});
//end: handle the test calls


//start: handle the train calls
var index = 0;
fs.createReadStream('./dataset/data-training-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (currentCall) {
        const { buggyCall, correctCall } = representations.wordTokenizationEnhanced(currentCall);

        const isDevSet = index % 10 == 0;
        index = index + 1;
        if (isDevSet) {
            correctDev.push(tokenization.tokenize(parser.stem(correctCall)))
            buggyDev.push(tokenization.tokenize(parser.stem(buggyCall)))
        } else {
            correctTrain.push(tokenization.tokenize(parser.stem(correctCall)))
            buggyTrain.push(tokenization.tokenize(parser.stem(buggyCall)))
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
//end: handle the test calls

// start: handle the real-bugs
var realbugsBuggyTest = [];
var realbugsCorrectTest = [];
const realbugsExamplesTest = [realbugsCorrectTest, realbugsBuggyTest];

const RealBugsTestSourceCorrectDir = "./RealBugsTestSourceCorrect/";
const RealBugsTestSourceBuggyDir = "./RealBugsTestSourceBuggy/";
const realbugsDirsTest = [RealBugsTestSourceCorrectDir, RealBugsTestSourceBuggyDir];

for (let i in realbugsDirsTest) {
    const dir = realbugsDirsTest[i]
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir)
    }
}

fs.createReadStream('./dataset/real-bugs-calls.json')
    .pipe(JSONStream.parse('*'))
    .pipe(es.mapSync(function (currentCall) {
        const { buggyCall, correctCall } = representations.wordTokenizationEnhanced(currentCall);

        realbugsCorrectTest.push(tokenization.tokenize(parser.stem(correctCall)))
        realbugsBuggyTest.push(tokenization.tokenize(parser.stem(buggyCall)))

        return currentCall;
    })).on('end', function () {
    console.log("finished running....");
    LOGGER.info({
        'RealBugs Stats:': {
            "buggy instances": realbugsBuggyTest.length,
            "correct instances": realbugsCorrectTest.length
        }
    });

    // write dataset
    for (var i = 0; i < realbugsExamplesTest.length; i++) {
        const exampleSet = realbugsExamplesTest[i];
        var dir = realbugsDirsTest[i];
        for (var j = 0; j < exampleSet.length; j++) {
            fs.writeFileSync(dir + j + '.js', exampleSet[j], function (err) {
                if (err) throw err;
                console.log('error processing ' + j + '.js' + ' in ' + dir);
            });
        }
    }
});
// end: handle the real-bugs