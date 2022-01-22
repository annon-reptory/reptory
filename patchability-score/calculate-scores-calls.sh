#set -x
mvn clean package

echo "DeepBugs Related Representations:"
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/2-deepbugs-representation/test.correct                                               representations/calls/1a-word-tokenization/test.correct    deepbugs-representation
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/3-deepbugs-representation-with-types-incomplete-with-variable-value/test.correct     representations/calls/1a-word-tokenization/test.correct    deepbugs-representation-with-types-incomplete-with-variable-value
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/4-deepbugs-representation-with-types-incomplete-without-variable-value/test.correct  representations/calls/1a-word-tokenization/test.correct    deepbugs-representation-with-types-incomplete-without-variable-value

echo "Code Simplification Related Representations:"
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/5-code-simplification-signatures/test.correct                                        representations/calls/1a-word-tokenization/test.correct         code-simplification
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/6-code-simplification-signatures-with-position-anchor/test.correct                   representations/calls/1a-word-tokenization/test.correct         code-simplification-signatures-with-position-anchor
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/7-code-simplification-signatures-with-lit-id/test.correct                            representations/calls/1a-word-tokenization/test.correct         code-simplification-signatures-with-lit-id
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/8-code-simplification-signatures-with-position-anchor-and-lit-id/test.correct        representations/calls/1a-word-tokenization/test.correct         code-simplification-signatures-with-position-anchor-and-lit-id

echo "AST Related Representations:"
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/10-ast-of-code-simplification-type-with-variable-value/test.correct                  representations/calls/9-ast-of-original-code/test.correct       ast-of-code-simplification-type-with-variable-value
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/11-ast-of-code-simplification-types-without-variable-value/test.correct              representations/calls/9-ast-of-original-code/test.correct       ast-of-code-simplification-type-without-variable-value
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/calls/12-preorder-ast-of-original-code/test.correct                                        representations/calls/9-ast-of-original-code/test.correct       pre-order-ast-tufano




