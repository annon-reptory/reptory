const esprima = require('esprima');
var natural = require('natural');
var tokenizer = new natural.WordTokenizer();
var crude_tokenization = require("./crude_tokenization")

exports._test = {
    tokenize_esprima: tokenize_esprima
}

function tokenize_esprima(line) {
    var tokens = []

    try {
        tokens = esprima.tokenize(line);
    } catch (err) {
        console.log("problem: " + err + ", input==>" + line);
        tokens = tokenizer.tokenize(line);
        tokens1 = crude_tokenization(line);
        console.log("problem: " + err + ", input==>" + line);
    }


    token_vals = []
    tokens.forEach(token => token_vals.push(token.value));

    if (tokens.size == 0) {
        console.log("cannot process =>", line)
    }
    return token_vals.join(' ');
}