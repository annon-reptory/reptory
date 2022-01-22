(function() {

    const fs = require("fs");
    const estraverse = require("estraverse");
    const util = require("./jsExtractionUtil");
    const escodegen = require("escodegen");
    const esprima = require("esprima");

    const minArgs = 2;
    const maxLengthOfCalleeAndArguments = 200; 

    function visitCode(ast, locationMap, path, fileID, allCallsComplete) {

        const functionToParameters = {}; 
        let functionCounter = 0;
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

                if (node.type === "FunctionDeclaration" || node.type === "FunctionExpression") {
                    functionCounter++;
                    if (node.params.length > 1) {
                        let functionName = util.getNameOfFunction(node, parent);

                        if (functionName) {
                            if (!functionToParameters.hasOwnProperty(functionName)) {
                                const parameterNames = [];
                                for (let i = 0; i < node.params.length; i++) {
                                    const parameter = node.params[i];
                                    parameterNames.push("ID:"+parameter.name);
                                }
                                functionToParameters[functionName] = parameterNames;
                            } 
                        }
                    }
                }
            }
        });

        const callsComplete = [];
        const parentStack = [];
        
        estraverse.traverse(ast, {
            enter:function(node, parent) {
                if (parent) parentStack.push(parent);
                if (node && node.type === "CallExpression") {
                    if (node.arguments.length != minArgs) return;

                    let calleeString;
                    let baseString;
                    let calleeNode;
                    if (node.callee.type === "MemberExpression") {
                        if (node.callee.computed === false) {
                            calleeNode = node.callee.property;
                            calleeString = util.getNameOfASTNode(calleeNode);
                            baseString = util.getNameOfASTNode(node.callee.object);
                        } else {
                            calleeNode = node.callee.object;
                            calleeString = util.getNameOfASTNode(calleeNode);
                            baseString = "";
                        }
                    } else {
                        calleeNode = node.callee;
                        calleeString = util.getNameOfASTNode(calleeNode);
                        baseString = "";
                    }

                    if (typeof calleeString === "undefined" || typeof baseString === "undefined") return;
                    
                    const calleeLocation = fileID + util.getLocationOfASTNode(calleeNode, locationMap);

                    const argumentStrings = [];
               
                    const argumentTypes = [];
                    for (let i = 0; i < node.arguments.length; i++) {
                        const argument = node.arguments[i];
                        const argumentString = util.getNameOfASTNode(argument);
                        const argumentType = util.getTypeOfASTNode(argument);
                        if (typeof argumentString === "undefined") return;
                        argumentStrings.push(argumentString.slice(0, maxLengthOfCalleeAndArguments));
                        argumentTypes.push(argumentType);
                    }

                    calleeString = calleeString.slice(0, maxLengthOfCalleeAndArguments);
                    baseString = baseString.slice(0, maxLengthOfCalleeAndArguments);
                    let locString = path + " : " + node.loc.start.line + " - " + node.loc.end.line;


                    //////////////////////////////////////////////////////////////////
                    /* Added for context-ml project */
                    /////////////////////////////////////////////////////////////////
                    let index;
                    index = util.getNameOfASTNode(node.arguments[0]).indexOf(":");
                    const arg1 = util.getNameOfASTNode(node.arguments[0]).slice(index+1);
                    index = util.getNameOfASTNode(node.arguments[1]).indexOf(":");
                    const arg2 = util.getNameOfASTNode(node.arguments[1]).slice(index+1);
                    const myBaseName = baseString != "" ? baseString.split(":")[1] : "";
                    const myCalleeName = calleeString.split(":")[1];

            	    let srcDefinition = "";
    	       	    let enclosingFunction = "";
    	       	    let enclosingFunctionNode = null;
                    let buggyEnclosingFunction = "";
                    let surroundingStatement = "";
                    let buggySurroundingStatement = "";
                    let srcCode = "";
                    let tempArgument1 = JSON.parse(JSON.stringify(node.arguments[0]));
                    let tempArgument2 = JSON.parse(JSON.stringify(node.arguments[1]));
                    const swappedNode = JSON.parse(JSON.stringify(node));
                    swappedNode.arguments[0] = JSON.parse(JSON.stringify(tempArgument2));
                    swappedNode.arguments[1] = JSON.parse(JSON.stringify(tempArgument1));

                    let swappedSrcCode = "";
                    try{
                        srcCode = escodegen.generate(node);
                        swappedSrcCode = escodegen.generate(swappedNode);
                        

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
                        

                    }catch(err){
                    	//console.log("error ", err)

                    }

                    let code_id = (`${path}${calleeLocation}`)
                    code_id = code_id.replace(/\//g,"")

                    // try{
                    // 	esprima.parse(enclosingFunction)
                    // }catch(err){
                    // 	console.log(err);  
                    // }

                    parsable = true;
                    try{
                        buggySurroundingStatement = surroundingStatement.replace(srcCode, swappedSrcCode)
                        buggyEnclosingFunction = enclosingFunction.replace(srcCode, swappedSrcCode)
                        esprima.parse(srcCode)
                        esprima.parse(swappedSrcCode)
                        esprima.parse(enclosingFunction)
                        esprima.parse(surroundingStatement)
                        esprima.parse(buggyEnclosingFunction)
                        esprima.parse(buggySurroundingStatement)

                    }catch(e){
                        parsable = false;
                    }

                    if (!parsable)
                        return

    		        callsComplete.push({
        			    callee: myCalleeName,
        			    base:myBaseName,
        			    arg1: arg1,
        			    arg2: arg2,
                        correctCall: srcCode,
                        buggyCall: swappedSrcCode,
                        surroundingStatement: surroundingStatement,
                        buggySurroundingStatement: buggySurroundingStatement,
						synthesizedArgumentTypes: ["", ""],
                        enclosingFunction: enclosingFunction,
                        buggyEnclosingFunction: buggyEnclosingFunction,
                        codeId: code_id,
        			    original: {
                            base:baseString,
                            callee:calleeString,
                            arguments:argumentStrings,
                            argumentTypes:argumentTypes,
                            src:locString
                        }

                    });
                    /////////////////////////////////////////////////////////////////////////////
                    /* End of added for context-ml project */
                    /////////////////////////////////////////////////////////////////////////////

                }
                },
            leave:function(node, parent) {
                if (parent) parentStack.pop();
            }
        });
        allCallsComplete.push(...callsComplete);
    }
    module.exports.visitCode = visitCode;
})();
