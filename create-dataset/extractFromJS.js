(function() {

    const process = require("process");
    const fs = require("fs");
    const walkSync = require("walk-sync");
    const {spawn} = require('child_process');

    const util = require("./jsExtractionUtil");

    const filesPerParallelInstance = 200;

    const fileToIDFileName = "fileIDs.json";

    function spawnSingleInstance(worklist, what) {
        //console.log("Left in worklist: " + worklist.length + ". Spawning an instance.");
        const jsFiles = worklist.pop();
        if (jsFiles) {
            const argsToPass = [process.argv[1], what, "--files"].concat(jsFiles);
            const cmd = spawn("node", argsToPass);
            cmd.on("close", (code) => {
                //console.log("Instance has finished with exit code " + code);
                if (worklist.length > 0) {
                    spawnSingleInstance(worklist, what);
                }
            });
            cmd.stdout.on('data', (data) => {
                console.log(`${data}`);
            });
            cmd.stderr.on('data', (data) => {
                console.log(`${data}`);
            });
        }
    }

    function spawnInstances(nbInstances, jsFiles, what) {
        const worklist = [];
        for (let i = 0; i < jsFiles.length; i += filesPerParallelInstance) {
            const chunkOfJSFiles = jsFiles.slice(i, i + filesPerParallelInstance);
            worklist.push(chunkOfJSFiles);
        }

        for (let instance = 0; instance < nbInstances; instance++) {
            spawnSingleInstance(worklist, what);
        }
    }

    function getOrCreateFileToID(files) {
        let fileToID;
        try {
            fileToID = JSON.parse(fs.readFileSync(fileToIDFileName, {encoding:"utf8"}));
        } catch (_) {
            fileToID = {};
        }
        let maxID = 1;
        for (let file in fileToID) {
            if (fileToID[file] > maxID) maxID = fileToID[file];
        }
        let haveAdded = false;
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (!fileToID.hasOwnProperty(file)) {
                maxID += 1;
                fileToID[file] = maxID;
                haveAdded = true;
            }
        }
        if (haveAdded) fs.writeFileSync(fileToIDFileName, JSON.stringify(fileToID, 0, 2));
        return fileToID;
    }

    function visitFile(jsFile, extractor, fileID, allDataComplete) {
        const code = fs.readFileSync(jsFile);
        const tokens = util.getTokens(code);
        const ast = util.getAST(code);
        if (tokens && ast) {
            const locationMap = util.computeLocationMap(tokens);
            extractor.visitCode(ast, locationMap, jsFile, fileID, allDataComplete);
        } else {
            //console.log("Ignoring file with parse errors: " + jsFile);
        }
    }

    // read command line arguments
    const args = process.argv.slice(2);
    const what = args[0];

    
    if (args[1] === "--parallel") {
        if (args.length !== 5) {
            //console.log(usage);
            process.exit(1);
        }
        const nbInstances = args[2];
        const fileListFile = args[3];
        const dir = args[4];

        // filter to use only files in file list
        const relativeJsFiles = walkSync(dir, {globs:["**/*.js"], directories:false});
        let jsFiles;

        const filesToConsider = new Set(fs.readFileSync(fileListFile, {encoding:"utf8"}).split(/\r?\n/));
        jsFiles = relativeJsFiles.map(f => dir + (dir.endsWith("/") ? "" : "/") + f).filter(p => filesToConsider.has(p));

        //console.log("Total number of files: " + jsFiles.length);
        getOrCreateFileToID(jsFiles);
        spawnInstances(nbInstances, jsFiles, what);
    } else if (args[1] === "--files") {
        let extractor;
        if (what === "calls") extractor = require("./extractorOfCalls");
        else if (what === "binOps") extractor = require("./extractorOfBinOps");

        const allDataComplete = [];

        const jsFiles = args.slice(2);
        let fileToID = getOrCreateFileToID(jsFiles);
        for (let i = 0; i < jsFiles.length; i++) {
            const jsFile = jsFiles[i];
            const fileID = fileToID[jsFile]; 

        	visitFile(jsFile, extractor, fileID, allDataComplete);
        }
        const completeFileName = what + "_complete_" + Date.now() + ".json";

        const log = fs.createWriteStream(what + "_extra_" + Date.now() + ".txt", { flags: 'a' });

        if (what === "calls"){
        	allDataComplete.map((single_element)=>{
            	log.write(single_element.codeId + "\nfield_separator\n" + single_element.arg1 + "\nfield_separator\n" + single_element.arg2 + "\nfield_separator\n" + single_element.correctCall + "\nfield_separator\n" + single_element.buggyCall + "\nfield_separator\n" + single_element.enclosingFunction + "\nfield_separator\n" + single_element.buggyEnclosingFunction + "\nfield_separator\n" + single_element.surroundingStatement + "\nfield_separator\n" + single_element.buggySurroundingStatement + "\nfield_separator\n" + single_element.callee + "\ndatapoint_separator\n")
        	})
        } else if (what === "binOps"){
        	allDataComplete.map((single_element)=>{
            	log.write(single_element.codeId + "\nfield_separator\n" + single_element.correctOp + "\nfield_separator\n" + single_element.buggyOperand + "\nfield_separator\n" + single_element.buggyOperator + "\nfield_separator\n" + single_element.leftOperand + "\nfield_separator\n" + single_element.rightOperand + "\nfield_separator\n" + single_element.enclosingFunction + "\nfield_separator\n" + single_element.buggyEnclosingFunctionOperand + "\nfield_separator\n" +  single_element.buggyEnclosingFunctionOperator + "\nfield_separator\n" +single_element.surroundingStatement + "\nfield_separator\n" + single_element.buggySurroundingStatementOperand + "\nfield_separator\n" + single_element.buggySurroundingStatementOperator + "\ndatapoint_separator\n")
        	})
        }
        
        log.end();

        if (what === "calls"){
        	fs.writeFile(completeFileName, JSON.stringify(allDataComplete, ['callee', 'base', 'synthesizedArgumentTypes', 'codeId', 'original', 'arguments', 'argumentTypes', 'arg1', 'arg2'], 2), ()=>{});
    	} else if (what === "binOps"){
    		fs.writeFile(completeFileName, JSON.stringify(allDataComplete, ['codeId', 'leftOperand', 'rightOperand', 'original', 'left', 'right', 'op', 'leftType', 'rightType'], 2), ()=>{});
    	}

    } else {
        //console.log(usage);
        process.exit(1);
    }

})();
