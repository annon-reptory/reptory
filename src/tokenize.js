const fs = require("fs");
const acorn = require("acorn");
const walk = require("acorn/dist/walk");
const rimraf = require('rimraf');

const TrainSourceCorrectDir = "./TrainSourceCorrect/";
const TrainSourceBuggyDir = "./TrainSourceBuggy/";

const TestSourceCorrectDir = "./TestSourceCorrect/";
const TestSourceBuggyDir = "./TestSourceBuggy/";

const DevSourceCorrectDir = "./DevSourceCorrect/";
const DevSourceBuggyDir = "./DevSourceBuggy/";

var code_sources = [TrainSourceCorrectDir, TrainSourceBuggyDir, TestSourceCorrectDir, TestSourceBuggyDir, DevSourceCorrectDir, DevSourceBuggyDir]

// train
const TrainASTBuggyDir = "./ASTsTrainBuggy/"
const TrainTokenBuggyDir = "./TokensTrainBuggy/"
const TrainASTCorrectDir = "./ASTsTrainCorrect/"
const TrainTokenCorrectDir = "./TokensTrainCorrect/"

// test
const TestASTBuggyDir = "./ASTsTestBuggy/"
const TestTokenBuggyDir = "./TokensTestBuggy/"
const TestASTCorrectDir = "./ASTsTestCorrect/"
const TestTokenCorrectDir = "./TokensTestCorrect/"

// dev
const DevASTBuggyDir = "./ASTsDevBuggy/"
const DevTokenBuggyDir = "./TokensDevBuggy/"
const DevASTCorrectDir = "./ASTsDevCorrect/"
const DevTokenCorrectDir = "./TokensDevCorrect/"

var astList = [TrainASTCorrectDir, TrainASTBuggyDir, TestASTCorrectDir, TestASTBuggyDir, DevASTCorrectDir, DevASTBuggyDir];
var tokenList = [TrainTokenCorrectDir, TrainTokenBuggyDir, TestTokenCorrectDir, TestTokenBuggyDir, DevTokenCorrectDir, DevTokenBuggyDir];

for (let i in astList) {
    if (fs.existsSync(astList[i])) {
        rimraf.sync(astList[i])
    }
}

for (let i in astList) {
    fs.mkdirSync(astList[i])
}

for (let i in tokenList) {
    if (fs.existsSync(tokenList[i])) {
        rimraf.sync(tokenList[i])
    }
}

for (var i in tokenList) {
    fs.mkdirSync(tokenList[i])
}


for (var i in code_sources) {
    var code_dir = code_sources[i];
    var sources = [];
    var files = fs.readdirSync(code_dir);

    files.forEach(file => {
        let name = file.slice(0, -3);
        sources.push(name);
    });

    sources.forEach(source => process(code_dir, source));
}

function process(code_dir, source) {
    var text = fs.readFileSync(code_dir + source + ".js", "utf-8");
    var parsed = parse(text);

    var test1 = parse("attr.attr(stroke,#ccc)")
    if (parsed === null) {
        console.log("===");
        console.log("OMG - its null");
        console.log(text);
        console.log("===");
        return
    }

    var tokens = parsed.tokens;
    var ast = parsed.ast;

    fs.writeFileSync(astList[i] + source + "_AST.json", JSON.stringify(ast, null, 2), function (err) {
        if (err) throw err;
        console.log('Created AST for file ' + source);
    });

    fs.writeFileSync(tokenList[i] + source + "_Tokens.json", JSON.stringify(tokens, null, 2), function (err) {
        if (err) {
            console.log('error ' + source);
            throw err;
        }
        console.log('Created tokens for file ' + source);
    });
}

function parse(text) {

    var tokens = [];
    var ast;
    try {
        ast = acorn.parse(text, {
            onToken: tokens
        });
    } catch (err) {
        //skipping unparsable react elements
        return null;
    }

    var intervals = [];

    walk.simple(acorn.parse(text), {
        Function(node) {
            var isOverlapping = false;
            for (var j = 0; j < intervals.length; j++) {
                if (intervals[j].start <= node.start
                    && intervals[j].end >= node.end) {
                    isOverlapping = true;
                }

            }
            if (!isOverlapping) {
                intervals.push({'start': node.start, 'end': node.end});
            }
        }
    });

    var ftokens = [];
    for (var j in tokens) {
        var token = tokens[j];
        var ignored = false;
        for (var i = 0; i < intervals.length; i++) {
            var tokenStart = parseInt(token.start);
            var tokenEnd = parseInt(token.end);
            var intervalStart = parseInt(intervals[i].start);
            var intervalEnd = parseInt(intervals[i].end);

            //if(token.type.label === "function")
            //{
            //	console.log("Start: " + token.start);
            //	console.log("End: " + token.end);
            //	console.log("Interval: " + intervals[i].start + " , "+ intervals[i].end);
            //	console.log("Start in: " + (parseInt(tokens[j].start) >= parseInt(intervals[i].start)));
            //	console.log("End in: " + (parseInt(tokens[j].end) <= parseInt(intervals[i].end)));
            //}

            if (tokenStart >= intervalStart && tokenEnd <= intervalEnd) {
                if (token.type.label !== "function") {
                    ignored = true;
                }
                break;
            }
        }

        if (!ignored) {
            ftokens.push(tokens[j]);
        }
    }

    return {'tokens': ftokens, 'ast': ast};
}
