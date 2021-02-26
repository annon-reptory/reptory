const fs = require("fs");
const rimraf = require('rimraf');

const VocabText = './vocab.txt';
const TokensBuggyDir = "./TokensTrainBuggy/";
const TokensCorrectDir = "./TokensTrainCorrect/";
const VocabDir = "./Vocab/";

if(!fs.existsSync(TokensCorrectDir) || !fs.existsSync(TokensBuggyDir)){
        console.log("Please make sure you have Tokens.")
        process.exit(1);
}

if(fs.existsSync(VocabDir)){
  rimraf.sync(VocabDir)
}

fs.mkdirSync(VocabDir)

var correct_examples = []
var correct_files = fs.readdirSync(TokensCorrectDir)
correct_files.forEach(file => {
    let name = file.slice(0, -8)
    correct_examples.push(name)
});

var buggy_examples = []
var buggy_files = fs.readdirSync(TokensBuggyDir)
buggy_files.forEach(file => {
    let name = file.slice(0, -8)
    buggy_examples.push(name)
})

correct_files.forEach(function(file){
  var tokenCorrect = JSON.parse(fs.readFileSync(TokensCorrectDir + file, "utf-8"))
  var tokens = ''
  for(var i = 0; i < tokenCorrect.length; i++)
  {
    if(i != 0)
    {
      tokens += ' '
    }    

    if(tokenCorrect[i].type.label === 'eof'){
      continue
    }

    if(!tokenCorrect[i].value){
      tokens += tokenCorrect[i].type.label
    }
    else
    {
        tokens += tokenCorrect[i].value
    }
  }

  fs.appendFileSync(VocabDir + 'VocabCorpus.correct', tokens + "\n");
});

buggy_files.forEach(function(file){
  var tokenBuggy = JSON.parse(fs.readFileSync(TokensBuggyDir + file, "utf-8"));
  var tokens = '';
  for(var i = 0; i < tokenBuggy.length; i++)
  {
    if(i != 0)
    {
      tokens += ' '
    }   

    if(tokenBuggy[i].type.label === 'eof'){
      continue
    }

    if(!tokenBuggy[i].value){
      tokens += tokenBuggy[i].type.label
    }
    else
    {
        tokens += tokenBuggy[i].value
    }
  }

  fs.appendFileSync(VocabDir + 'VocabCorpus.buggy', tokens + "\n");
});


