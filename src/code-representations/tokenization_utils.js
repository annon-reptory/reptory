var _ = require('lodash');

// https://stackoverflow.com/questions/18379254/regex-to-split-camel-case
CamelCaseSplit = (inputString) => {
    // this regex can handle camelcase split
    const splittedString = inputString.replace(/(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])/g, ' <CAMEL> ')

    // const camelCaseToWords = s => _.words(s).join(' <CAMEL> ');
    // const splittedString = camelCaseToWords(inputString)
    //
    // if(!inputString.trim()){
    //     return inputString;
    // }
    return splittedString;
}

SnakeCaseSplit = (inputString) => {
    const splittedString = inputString.split('_');
    return splittedString.join(' ');
}

// https://stackoverflow.com/questions/42827884/split-a-number-from-a-string-in-javascript
NumberSplit = (inputString) => {
    const splittedString = inputString.replace(/\'/g, '').split(/(\d+)/)
    return splittedString.join(' ');
}

Tokenize = (input_string) => {
    result = CamelCaseSplit(input_string)
    result = SnakeCaseSplit(result)
    result = NumberSplit(result)
    result = result.replace(/\s\s+/g, ' ');
    result = rtrim(result)
    result = ltrim(result)
    return result
}

function ltrim(x) {
    // This implementation removes whitespace from the left side of the input string.
    return x.replace(/^\s+/gm, '');
}

function rtrim(x) {
    // This implementation removes whitespace from the right side of the input string.
    return x.replace(/\s+$/gm, '');
}


module.exports = {
    camelCaseSplit: CamelCaseSplit,
    snakeCaseSplit: SnakeCaseSplit,
    numberSplit: NumberSplit,
    tokenize: Tokenize
}
