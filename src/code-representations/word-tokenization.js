wordTokenization = (call) => {
    const baseAndCallee = call.base ? call.base + " . " + call.callee : call.callee;

    const correctCall = baseAndCallee
        + " "
        + "("
        + " "
        + call.arg1
        + " "
        + ","
        + " "
        + call.arg2
        + " "
        + ")";

    const buggyCall = baseAndCallee
        + " "
        + "("
        + " "
        + call.arg2
        + " "
        + ","
        + " "
        + call.arg1
        + " "
        + ")";

    return {
        buggyCall,
        correctCall
    };
}

getValue = (input_arg, input_type) => {
    numbers = [0, 1]
    numbers_str = ["0", "1"]
    strings = ["0", "1"]
    result = input_arg

    if (input_type === 'string') {
        if (strings.includes(input_arg)) {
            result = input_arg
        } else {
            result = "String"
        }
    } else if (input_type === 'number'){
        if (numbers.includes(input_arg) || numbers_str.includes(input_arg)) {
            result = input_arg
        } else {
            result = "Number"
        }
    }
    return result;
}

wordTokenizationEnhanced = (call) => {
    const baseAndCallee = call.base ? call.base + " . " + call.callee : call.callee;

    const arg1Type = call.synthesizedArgumentTypes[0];
    const arg2Type = call.synthesizedArgumentTypes[1];

    const correctCall = baseAndCallee
        + " "
        + "("
        + " "
        + getValue(call.arg1, arg1Type)
        + " "
        + ","
        + " "
        + getValue(call.arg2, arg2Type)
        + " "
        + ")";

    const buggyCall = baseAndCallee
        + " "
        + "("
        + " "
        + getValue(call.arg2, arg2Type)
        + " "
        + ","
        + " "
        + getValue(call.arg1, arg1Type)
        + " "
        + ")";

    return {
        buggyCall,
        correctCall
    };
}

module.exports = {
    wordTokenization: wordTokenization,
    wordTokenizationEnhanced: wordTokenizationEnhanced
}
