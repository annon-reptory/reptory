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

module.exports = {
    wordTokenization: wordTokenization
}
