#set -x
mvn clean package

echo "DeepBugs Related Representations:"
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/bin-operands/row5/test.correct     representations/bin-operands/row3/test.correct    deepbugs-representation
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/bin-operands/row6/test.correct     representations/bin-operands/row3/test.correct    deepbugs-representation-with-types-incomplete-with-variable-value
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/bin-operands/row7/test.correct     representations/bin-operands/row3/test.correct    deepbugs-representation-with-types-incomplete-without-variable-value

echo "AST Related Representations:"
java -jar target/PatchabilityScore-jar-with-dependencies.jar representations/bin-operands/row16/test.correct     representations/bin-operands/row12/test.correct  ast-pre-order




