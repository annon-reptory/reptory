(function() {

    const fs = require("fs");
    const estraverse = require("estraverse");
    const util = require("./jsExtractionUtil");
    const escodegen = require("escodegen");
    const esprima = require("esprima");

    function visitCode(ast, locationMap, path, fileIDStr, allBinOpsDefs) {
        //console.log("Reading " + path);

        let totalBinOps = 0;
        let totalBinOpsConsidered = 0;

        allFunctions = {}
        allFunctionsNode = {}

        estraverse.traverse(ast, {
            enter:function(node, parent) {
                if (parent === null || node.type === "FunctionDeclaration" || node.type === "FunctionExpression"){
                    
                    oneFunction = ""
                    const dummyNode = JSON.parse(JSON.stringify(node));
                        
                    let result = estraverse.replace(dummyNode, {
                        enter: function (innernode, innerparent) {
                            if (dummyNode !== innernode && (innernode.type === "FunctionDeclaration" || innernode.type === "FunctionExpression")){  
                               
                                innernode.body = {  "type": "BlockStatement",
                                                "body": []
                                             };   
                                this.skip(); 
                            }
                        }
                    });

                    oneFunction = escodegen.generate(result);

                    if (node.type === "FunctionExpression")
                        oneFunction = "var a = " + escodegen.generate(result);
                    else
                        oneFunction = escodegen.generate(result);

                    allFunctions[dummyNode.start] = oneFunction;
                    allFunctionsNode[dummyNode.start] = dummyNode;
                }
            }
        });

	    let srcCode = "";
        let srcDef = "";

        const parentStack = [];
        const binOps = [];
		const binOpsDefs = [];
        let tokenID = 1;
        estraverse.traverse(ast, {
            enter:function(node, parent) {
                if (parent) parentStack.push(parent);
                if (node.type === "BinaryExpression") {
                    totalBinOps += 1;
                    const leftName = util.getNameOfASTNode(node.left);
                    const rightName = util.getNameOfASTNode(node.right);
                    const leftType = util.getTypeOfASTNode(node.left);
                    const rightType = util.getTypeOfASTNode(node.right);
                    const parentName = parent.type;
		            let locString = null;
                    const grandParentName = parentStack.length > 1 ? parentStack[parentStack.length - 2].type : "";
                    if (typeof leftName !== "undefined" && typeof rightName !== "undefined") {
                        locString = path + " : " + node.loc.start.line + " - " + node.loc.end.line;
                        
                        totalBinOpsConsidered += 1;
                        tokenID += 1;

                        //////////////////////////////////////////////////////////////////
                        /* Added for context-ml project */
                        /////////////////////////////////////////////////////////////////
                        let srcCode = "";
                        let swappedNodeCode = "";
                        let wrongOperatorCode = "";

                        const swappedNode = JSON.parse(JSON.stringify(node));
                        const wrongOperator = JSON.parse(JSON.stringify(node)); 
                        swappedNode.left = JSON.parse(JSON.stringify(node.right));
                        swappedNode.right = JSON.parse(JSON.stringify(node.left));
                        let enclosingFunction = ""
                        let buggyEnclosingFunctionOperand = ""
                        let buggyEnclosingFunctionOperator = ""
                        let surroundingStatement = ""
                        let buggySurroundingStatementOperand = ""
                        let buggySurroundingStatementOperator = ""

                        const opLocation = fileIDStr + util.getLocationOfASTNode(node, locationMap);

                        all_operators = ["*", "%", "/", "+", "-", ">>", "<<", ">>>", ">", "<", ">=", "<=", "in", "instanceof", "==", "!=", "===", "!==", "&", "^", "|", "&&", "||"]
                        incorrect_operator = node.operator;
                        while (incorrect_operator == node.operator){
                            incorrect_operator = all_operators[Math.floor(Math.random() * all_operators.length)];
                        }
                        wrongOperator.operator = incorrect_operator;

                        try{
                            srcCode = escodegen.generate(node);
                            swappedNodeCode = escodegen.generate(swappedNode);
                            wrongOperatorCode = escodegen.generate(wrongOperator);
                            

                            for(let i = parentStack.length - 1; i >= 0; i--){
                                if (parentStack[i].type === "FunctionDeclaration" || parentStack[i].type === "FunctionExpression" || i === 0) {

                                    enclosingFunction = allFunctions[parentStack[i].start]
                                    enclosingFunctionNode = allFunctionsNode[parentStack[i].start].body.body !== undefined ? allFunctionsNode[parentStack[i].start].body.body : allFunctionsNode[parentStack[i].start].body;
                                    let targetIndex;
                                    try{

                                        for (j = 0; j < enclosingFunctionNode.length; j++){
                                            if (node.start >= enclosingFunctionNode[j].start && node.end <= enclosingFunctionNode[j].end){
                                                targetIndex = j;
                                                break;
                                            }
                                        }

                                        surroundingStatement = escodegen.generate(enclosingFunctionNode[targetIndex])
                                        surroundingStatement = (targetIndex-1) >= 0 ? (escodegen.generate(enclosingFunctionNode[targetIndex-1]) + surroundingStatement) : surroundingStatement;
                                        surroundingStatement = (targetIndex+1) <= (enclosingFunctionNode.length - 1) ? (surroundingStatement + escodegen.generate(enclosingFunctionNode[targetIndex+1])) : surroundingStatement;
                                        esprima.parse(surroundingStatement)
                                        
                                    }catch(error){
                                        surroundingStatement = enclosingFunction;
                                    }
                                    break
                                }
                            }
                            buggyEnclosingFunctionOperand = enclosingFunction.replace(srcCode, swappedNodeCode)
                            buggyEnclosingFunctionOperator = enclosingFunction.replace(srcCode, wrongOperatorCode)

                        }catch(err){
                            //console.log("error ", err)

                        }


                        let code_id = (`${path}${opLocation}.txt`);
                        code_id = code_id.replace(/\//g,"");


                        buggySurroundingStatementOperand = surroundingStatement.replace(srcCode, swappedNodeCode)
                        buggySurroundingStatementOperator = surroundingStatement.replace(srcCode, wrongOperatorCode)

                        let parsable = true;
                        try{
                            esprima.parse(srcCode)
                            esprima.parse(swappedNodeCode)
                            esprima.parse(wrongOperatorCode)
                            esprima.parse(enclosingFunction)
                            esprima.parse(surroundingStatement)
                            esprima.parse(buggyEnclosingFunctionOperand)
                            esprima.parse(buggyEnclosingFunctionOperator)
                            esprima.parse(buggySurroundingStatementOperand)
                            esprima.parse(buggySurroundingStatementOperator)
                        }catch(err){
                            parsable = false;
                        }

                        let index = leftName.indexOf(":");
                        const leftOp = leftName.slice(index+1);
                        index = rightName.indexOf(":");
                        const rightOp = rightName.slice(index+1);

                        if (parsable)
    					    binOpsDefs.push({
    						    //correctOp: leftName.split(":")[1]+" "+node.operator+" "+rightName.split(":")[1],
    						    //buggyOperand: rightName.split(":")[1]+" "+node.operator+" "+leftName.split(":")[1],
    			   			    //correct_operator: leftName.split(":")[1]+" "+node.operator+" "+rightName.split(":")[1],
    						    //buggyOperator: leftName.split(":")[1]+" "+incorrect_operator+" "+rightName.split(":")[1],
                                leftOperand: leftOp,
                                rightOperand: rightOp,
                                codeId: code_id,
                                correctOp: srcCode,
                                buggyOperand: swappedNodeCode,
                                buggyOperator: wrongOperatorCode,
                                enclosingFunction: enclosingFunction,
                                buggyEnclosingFunctionOperand: buggyEnclosingFunctionOperand,
                                buggyEnclosingFunctionOperator: buggyEnclosingFunctionOperator,
                                surroundingStatement: surroundingStatement,
                                buggySurroundingStatementOperand: buggySurroundingStatementOperand,
                                buggySurroundingStatementOperator: buggySurroundingStatementOperator,
                                //filename:path,
    						    original: {
    							    left:leftName,
    			                    right:rightName,
    			                    op:node.operator,
    			                    leftType:leftType,
    			                    rightType:rightType,
    			                    parent:parentName,
    			                    grandParent:grandParentName,
    			                    src:locString
    	                        }

    	                    });

                        /////////////////////////////////////////////////////////////////////////////
                        /* End of added for context-ml project */
                        /////////////////////////////////////////////////////////////////////////////
                    }
		    
                }
            },
            leave:function(node, parent) {
                if (parent) parentStack.pop();
            }
        });
	    allBinOpsDefs.push(...binOpsDefs)
        //console.log("Added binary operations. Total now: " + allBinOps.length);
        //console.log("Considered binary operations: "+totalBinOpsConsidered+" out of "+totalBinOps+" ("+Math.round(100*totalBinOpsConsidered/totalBinOps)+"%)");
    }
    module.exports.visitCode = visitCode;
})();
