package com.learning.contextml;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.commons.io.FileUtils;
import static com.learning.contextml.ComparePatches.jaroWinklerSimilarity;
import static com.learning.contextml.ComparePatches.levenshteinDistance;

public class Runner {

    public static void main(String args[]) throws IOException {
        File inferredPatchesFile = new File(args[0]);
        File groundTruthPatchesFile = new File(args[1]);
        String codeRepresentation = args[2];

        List<String> inferredPatches = FileUtils.readLines(inferredPatchesFile, "utf-8");
        List<String> groundTruthPatches = FileUtils.readLines(groundTruthPatchesFile, "utf-8");

        if (inferredPatches.size() != groundTruthPatches.size()) {
            System.out.println("file sizes dont match");
            System.exit(-1);
        }

        List<Patch> patches = new ArrayList<>();
        for (int index = 0; index < inferredPatches.size(); index++) {

            String inferredRepresentation = inferredPatches.get(index);
            String groundTruthRepresentation = groundTruthPatches.get(index);

            Patch patch = new Patch(index,
                    inferredRepresentation,
                    groundTruthRepresentation,
                    jaroWinklerSimilarity(inferredRepresentation, groundTruthRepresentation),
                    levenshteinDistance(inferredRepresentation, groundTruthRepresentation));
            patches.add(patch);
        }

        double score = patches.stream()
                .mapToDouble(p -> p.getLevenshteinDistance())
                .average()
                .orElse(Double.NaN);

        System.out.format("score: for %s: %f \n", codeRepresentation, score);
    }
}
