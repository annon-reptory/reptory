const fs = require("fs");
const rimraf = require('rimraf');

// dataDir='./TrainData/'
// correctDir='TokensTrainCorrect/'
// buggyDir='TokensTrainBuggy/'

// var DataDir = './TrainData/' // process.env.dataDir
// var DataName = DataDir.replace('Data/', '').toLowerCase()
// var TokensCorrectDir = 'TokensTrainCorrect/' //process.env.correctDir
// var TokensBuggyDir = 'TokensTrainBuggy/' //process.env.buggyDir

const DataDir = process.env.dataDir;
const DataName = DataDir.replace('Data/', '').toLowerCase();
const TokensCorrectDir = process.env.correctDir;
const TokensBuggyDir = process.env.buggyDir;
const ASTsCorrectDir = process.env.astCorrectDir;
const ASTsBuggyDir = process.env.astBuggyDir;

const VocabBuggy = './Vocab/vocab.buggy'
const VocabCorrect = './Vocab/vocab.correct'

// const DataDir ='./TrainData/'
// const TokensCorrectDir='TokensTrainCorrect/'
// const TokensBuggyDir='TokensTrainBuggy/'

if (!fs.existsSync(TokensCorrectDir) || !fs.existsSync(TokensBuggyDir)) {
    console.log("Please make sure you have Tokens.")
    process.exit(1)
}

if (!fs.existsSync(VocabCorrect) || !fs.existsSync(VocabBuggy)) {
    console.log("Please make sure you have generated vocabulary.")
    process.exit(1)
}

if (fs.existsSync(DataDir)) {
    rimraf.sync(DataDir)
}

fs.mkdirSync(DataDir);
fs.openSync(DataDir + DataName + '.correct', 'w')
fs.openSync(DataDir + DataName + '.buggy', 'w')

vocab_buggy = fs.readFileSync(VocabBuggy, 'utf8')
vocab_correct = fs.readFileSync(VocabCorrect, 'utf8')

var ast_correct_files = fs.readdirSync(ASTsCorrectDir)
var ast_buggy_files = fs.readdirSync(ASTsBuggyDir);

function getArgumentType(input) {
    return input.type;
}

function getArgumentValue(input) {
    return input.type === "Literal" ? input.value :
        input.name;
}

function getCallee(input) {
    return input.type === 'MemberExpression' ?
        (input.object.type === "ThisExpression" ?
                "this " + ' ' + input.property.name :
                input.object.name + ' ' + input.property.name
        )
        : input.name
}

function getFeature(astCorrect) {
    const expressionStatement = astCorrect.body[0]      // ExpressionStatement
    const expressionStatementType = astCorrect.body[0].type // ExpressionStatement
    const expression = expressionStatement.expression
    const expressionType = expression.type
    // console.log(expressionStatement)

    const callee = getCallee(expression.callee);

    const arguments = expression.arguments
    const left = getArgumentValue(arguments[0])
    const leftType = getArgumentType(arguments[0])
    const right = getArgumentValue(arguments[1])
    const rightType = getArgumentType(arguments[1])

    const featureString = leftType + ' ' + left + ' '
        + expressionStatementType + " "
        + expressionType + " "
        + callee + ' '
        + rightType + ' ' + right;

    return featureString;
}

correct_pattern_list = new Set();
ast_correct_files.forEach(function (file) {
    var astCorrect = JSON.parse(fs.readFileSync(ASTsCorrectDir + file, "utf-8"))
    tokens = getFeature(astCorrect);

    correct_pattern_list.add(tokens)
    fs.appendFileSync(DataDir + DataName + '.correct', tokens + "\n")
});

buggy_pattern_list = new Set();
ast_buggy_files.forEach(function (file) {
    var astBuggy = JSON.parse(fs.readFileSync(ASTsBuggyDir + file, "utf-8"))
    tokens = getFeature(astBuggy);

    buggy_pattern_list.add(tokens);
    fs.appendFileSync(DataDir + DataName + '.buggy', tokens + "\n");
});
