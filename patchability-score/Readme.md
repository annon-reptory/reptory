**Patchability Score:**:

- **Build Package**: mvn clean package
- **Run** : `java -jar target/PatchabilityScore-jar-with-dependencies.jar inferred.txt ground-truth.txt code-representation-name`

**Edit-distance:**

|Code Representation   	                                                    |Ground Truth   	   |
|---	                                                                    |---	               |
|**Non AST Based:**                                                         |                      |
|deepbugs-representation   	                                                |word-tokenization     |
|deepbugs-representation-with-types-incomplete-with-variable-value   	    |word-tokenization     |
|deepbugs-representation-with-types-incomplete-without-variable-value   	|word-tokenization     |
|code-simplification                                                        |word-tokenization     | 
|code-simplification-signatures-with-position-anchor                        |word-tokenization     |
|code-simplification-signatures-with-lit-id                                 |word-tokenization     |
|code-simplification-signatures-with-position-anchor-and-lit-id             |word-tokenization     |
|**AST Based:**                                                             |                      |
|ast-of-code-simplification-type-with-variable-value                        |ast-of-original-code  |
|ast-of-code-simplification-type-without-variable-value                     |ast-of-original-code  |

**Calculate Scores:**
- Edit-distance score for calls dataset: `calculate-scores-calls.sh`







