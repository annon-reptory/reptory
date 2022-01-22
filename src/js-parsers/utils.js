/*
-- LF:    Line Feed, U+000A (10 in decimal)
-- VT:    Vertical Tab, U+000B (11 in decimal)
-- FF:    Form Feed, U+000C (12 in decimal)
-- CR:    Carriage Return, U+000D (13 in decimal)
-- CR+LF: CR (U+000D) (13 in decimal) followed by LF (U+000A) (10 in decimal)
-- NEL:   Next Line, U+0085 (133 in decimal)
-- LS:    Line Separator, U+2028 (8232 in decimal)
-- PS:    Paragraph Separator, U+2029 (8233 in decimal)
*/

function stem(input) {
    return input
        .replace(/[\r\n\x0B\x0C\u0085\u2028\u2029]+/g," ")
        .replace(/[\x00-\x1F\x7F-\x9F]/g, "")
        .replace(/:/g, ' ')
        .replace(/(\r\n|\n|\r)/gm," ")
        .replace(/\s\s+/g, ' ')
        .trim();
}

module.exports = {
    stem
};
