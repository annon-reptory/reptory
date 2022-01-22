const fs = require("fs");
const rimraf = require('rimraf');

const DataDir = process.env.dataDir;
const DataName = DataDir.replace('Data/', '').toLowerCase();
const TokensCorrectDir = process.env.correctDir;
const TokensBuggyDir = process.env.buggyDir;
const VocabBuggy = './vocab/vocab.buggy';
const VocabCorrect = './Vocab/vocab.correct';

if (!fs.existsSync(TokensCorrectDir) || !fs.existsSync(TokensBuggyDir)) {
    console.log("Please make sure you have Tokens.")
    process.exit(1);
}

if (!fs.existsSync(VocabCorrect) || !fs.existsSync(VocabBuggy)) {
    console.log("Please make sure you have generated vocabulary.")
    process.exit(1);
}

if (fs.existsSync(DataDir)) {
    rimraf.sync(DataDir);
}

fs.mkdirSync(DataDir);
fs.openSync(DataDir + DataName + '.correct', 'w');
fs.openSync(DataDir + DataName + '.buggy', 'w');

vocab_buggy = fs.readFileSync(VocabBuggy, 'utf8');
vocab_correct = fs.readFileSync(VocabCorrect, 'utf8');

var correct_examples = [];
var correct_files = fs.readdirSync(TokensCorrectDir);
correct_files.forEach(file => {
    let name = file.slice(0, -8);
    correct_examples.push(name);
});

var buggy_examples = [];
var buggy_files = fs.readdirSync(TokensBuggyDir);
buggy_files.forEach(file => {
    let name = file.slice(0, -5);
    buggy_examples.push(name);
});

duplicates_allowed = true;

correct_pattern_list = new Set();
correct_files.forEach(function (file) {
    var tokenCorrect = JSON.parse(fs.readFileSync(TokensCorrectDir + file, "utf-8"));
    var tokens = '';
    for (var i = 0; i < tokenCorrect.length; i++) {
        if (i != 0) {
            tokens += ' ';
        }

        if (tokenCorrect[i].type.label === 'eof') {
            continue;
        }

        if (!tokenCorrect[i].value) {
            tokens += tokenCorrect[i].type.label;
        } else {
            if (vocab_correct.includes(tokenCorrect[i].value)) {
                tokens += tokenCorrect[i].value;
            } else {
                tokens += '@' + tokenCorrect[i].type.label;
            }
        }
    }

    if (correct_pattern_list.has(tokens) & !duplicates_allowed) {
        return;
    }

    correct_pattern_list.add(tokens);
    fs.appendFileSync(DataDir + DataName + '.correct', tokens + "\n");
});

buggy_pattern_list = new Set();
buggy_files.forEach(function (file) {
    var tokenBuggy = JSON.parse(fs.readFileSync(TokensBuggyDir + file, "utf-8"));

    var tokens = '';
    for (var i = 0; i < tokenBuggy.length; i++) {
        if (i != 0) {
            tokens += ' ';
        }

        if (tokenBuggy[i].type.label === 'eof') {
            continue;
        }

        if (!tokenBuggy[i].value) {
            tokens += tokenBuggy[i].type.label;
        } else {
            if (vocab_buggy.includes(tokenBuggy[i].value)) {
                tokens += tokenBuggy[i].value;
            } else {
                tokens += '@' + tokenBuggy[i].type.label;
            }
        }
    }

    if (buggy_pattern_list.has(tokens) && !duplicates_allowed) {
        return;
    }

    buggy_pattern_list.add(tokens);
    fs.appendFileSync(DataDir + DataName + '.buggy', tokens + "\n");
});
