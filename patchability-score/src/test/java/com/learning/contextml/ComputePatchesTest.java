package com.learning.contextml;

import java.util.List;
import java.util.ArrayList;
import org.junit.jupiter.api.Test;
import static com.learning.contextml.ComparePatches.jaroWinklerSimilarity;
import static com.learning.contextml.ComparePatches.levenshteinDistance;

public class ComputePatchesTest {

    @Test
    public void nonAstBasedRepresentations() {
        List<String> inferredRepresentations = new ArrayList<>();
        String groundTruthRepresentation = "setTimeout ( delay , fn )";

        // DeepBugs Representation
        inferredRepresentations.add("ID setTimeout ( ID delay , ID fn )");

        // DeepBugs Representation (with Types Incomplete with variable value)
        inferredRepresentations.add("ID setTimeout ( ID unknown delay , ID unknown fn )");

        // DeepBugs Representation (with Types Incomplete without variable value)
        inferredRepresentations.add("ID setTimeout ( ID unknown , ID unknown )");

        // Code Simplification (function signatures with synthesized types)
        inferredRepresentations.add("setTimeout ( function , number )");

        //Code Simplification (function signatures with synthesized types and position anchor)
        inferredRepresentations.add("setTimeout ( arg0 function , arg1 number )");

        //Code Simplification (function signatures with synthesized types and LIT/ID)
        inferredRepresentations.add("setTimeout ( ID function , ID number )");

        //Code Simplification (function signatures with synthesized types along with position anchor and LIT/ID)");
        inferredRepresentations.add("setTimeout ( arg0 ID function , arg1 ID number )");

        for (String inferredRepresentation : inferredRepresentations) {
            Patch patch = new Patch(0,
                    inferredRepresentation,
                    groundTruthRepresentation,
                    jaroWinklerSimilarity(inferredRepresentation, groundTruthRepresentation),
                    levenshteinDistance(inferredRepresentation, groundTruthRepresentation));

            System.out.println(patch);
        }

    }

    @Test
    public void astBasedRepresentations() {
        List<String> inferredRepresentations = new ArrayList<>();
        String groundTruthRepresentation = "Program ExpressionStatement CallExpression Identifier setTimeout Identifier delay Identifier fn";

        // DeepBugs Representation
        inferredRepresentations.add("Program ExpressionStatement CallExpression  Identifier setTimeout Identifier function delay Identifier number fn");

        // DeepBugs Representation (with Types Incomplete with variable value)
        inferredRepresentations.add("Program ExpressionStatement CallExpression Identifier setTimeout Identifier function Identifier number");

        for (String inferredRepresentation : inferredRepresentations) {
            Patch patch = new Patch(0,
                    inferredRepresentation,
                    groundTruthRepresentation,
                    jaroWinklerSimilarity(inferredRepresentation, groundTruthRepresentation),
                    levenshteinDistance(inferredRepresentation, groundTruthRepresentation));

            System.out.println(patch);
        }
    }

    @Test
    public void experimentWithRepresentations() {

        List<String> inferredRepresentations = new ArrayList<>();
        String groundTruthRepresentation = "setTimeout ( arg0 ID function fn, arg1 ID number delay )";

        inferredRepresentations.add("setTimeout ( arg0 function fn, arg1 number delay )");
        inferredRepresentations.add("setTimeout ( ID function fn, ID delay )");
        inferredRepresentations.add("setTimeout ( function fn, ID delay )");

        for (String inferredRepresentation : inferredRepresentations) {
            Patch patch = new Patch(0,
                    inferredRepresentation,
                    groundTruthRepresentation,
                    jaroWinklerSimilarity(inferredRepresentation, groundTruthRepresentation),
                    levenshteinDistance(inferredRepresentation, groundTruthRepresentation));

            System.out.println(patch);
        }
    }


    @Test
    public void moreExperiments() {
        List<String> inferredRepresentations = new ArrayList<>();
        String groundTruthRepresentation = "setTimeout ( arg0 ID function fn, arg1 ID number delay )";

        inferredRepresentations.add("setTimeout ( function , number )");
        inferredRepresentations.add("setTimeout ( arg0 function , arg1 number )");
        inferredRepresentations.add("setTimeout ( ID function , ID delay )");
        inferredRepresentations.add("setTimeout ( arg0 ID function , arg1 ID number )");

        for (String inferredRepresentation : inferredRepresentations) {
            Patch patch = new Patch(0,
                    inferredRepresentation,
                    groundTruthRepresentation,
                    jaroWinklerSimilarity(inferredRepresentation, groundTruthRepresentation),
                    levenshteinDistance(inferredRepresentation, groundTruthRepresentation));

            System.out.println(patch);
        }
    }

}
