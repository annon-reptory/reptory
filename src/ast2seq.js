/* Replaces nodes of certain types with a new abstract node.
 * Adapted from https://github.com/jamen/estree-walk/blob/master/index.js */
const esprima = require('esprima');

module.exports = walk;
walk.step = step;

function walk(node) {
    ast_sequence = '';

    for (var stack = [node]; stack.length;) {
        node = stack.pop();
        ast_sequence = ast_sequence + ' ' + node.type;

        if (node.type === 'Identifier') {
            ast_sequence = ast_sequence + ' ' + node.name
            //console.log(node.name);
        }

        if (node.type === 'Literal') {
            ast_sequence = ast_sequence + ' ' + node.value
            //console.log(node.name);
        }

        // Skip a missing node
        if (!node) continue;

        // Continue walking
        step(node, stack);
    }

    return ast_sequence;
}


function handleCallExpression(child, queue) {
    if (child && child.type) {
        /* Otherwise push the node. */
        queue.push(child);
    }

    if (Array.isArray(child)) {
        for (let i = child.length; i >=0; i--) {
            const item = child[i];
            if (item && item.type) {
                queue.push(item);
            }
        }
    }
}

function step(node, queue) {
    var before = queue.length;

    if (node.type == 'CallExpression') {
        handleCallExpression(node.arguments, queue);
        handleCallExpression(node.callee, queue);
    } else if (node.type == 'MemberExpression') {
        handleCallExpression(node.property, queue);
        handleCallExpression(node.object, queue);
    }
    else {
        // Enumerate keys for possible children
        for (var key in node) {
            var child = node[key];

            if (child && child.type) {
                /* Otherwise push the node. */
                queue.push(child);
            }

            if (Array.isArray(child)) {
                for (let i = child.length; i >=0; i--) {
                    const item = child[i];
                    if (item && item.type) {
                        queue.push(item);
                    }
                }
            }
        }
    }

    // Return whether any children were pushed
    return queue.length !== before
}

function tokenize_esprima(line) {
    try {
        tree = esprima.parse(line);
    } catch (err) {
        console.log("problem: " + err + ", input==>" + line);
        tree = undefined
    }

    return tree;
}

// const ast_tree = tokenize_esprima("Math.sum(aa, bb)");
// const ast_tree = tokenize_esprima("Math.sum(aa, 10)");
let ast_tree = tokenize_esprima("sum(aa, bb)");
let ast_seq = walk(ast_tree)
console.log(ast_seq)

console.log("======")
console.log(walk(tokenize_esprima("Math.sum(aa, bb)")))

console.log("======")
console.log(walk(tokenize_esprima("setTimeout(delay,fn)")))

console.log("======")
console.log(walk(tokenize_esprima("window.setTimeout ( delay ,  fn )")))
