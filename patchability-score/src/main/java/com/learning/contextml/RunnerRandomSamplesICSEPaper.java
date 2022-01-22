package com.learning.contextml;

import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

import static com.learning.contextml.ComparePatches.jaroWinklerSimilarity;

public class RunnerRandomSamplesICSEPaper {

    public static void main(String args[]) throws IOException {
        String inferredPatchesFileName = args[0];
        String groundTruthPatchesFileName = args[1];
        Integer howManySamples = new Integer(args[2]);

        File inferredPatchesFile = new File(args[0]);
        File groundTruthPatchesFile = new File(args[1]);

        List<String> inferredPatches = FileUtils.readLines(inferredPatchesFile, "utf-8");
        List<String> groundTruthPatches = FileUtils.readLines(groundTruthPatchesFile, "utf-8");

        if (inferredPatches.size() != groundTruthPatches.size()) {
            System.out.println("sizes dont match");
            System.exit(-1);
        }

        String s1 = "setTimeout ( fn ,  delay )";
        String s2 = "setTimeout ( function fn , number  delay )";
        String s3 = "setTimeout ( function , number )";
        System.out.println(jaroWinklerSimilarity(s1, s2));
        System.out.println(jaroWinklerSimilarity(s1, s3));

        System.exit(1);

        List<Patch> patches = new ArrayList<>();
        for (int index = 0; index < inferredPatches.size(); index++) {

            String inferredRepresentation = inferredPatches.get(index);
            String groundTruthRepresentation = groundTruthPatches.get(index);

            Patch patch = new Patch(
                    index,
                    inferredRepresentation,
                    groundTruthRepresentation,
                    jaroWinklerSimilarity(inferredRepresentation, groundTruthRepresentation),
                    -1.0);
            patches.add(patch);
        }

        List<Patch> sortedPatches = patches.stream()
                .sorted(Comparator.comparingDouble(Patch::getSimailarity))
                .collect(Collectors.toList());

        List<Patch> results = new ArrayList<>();
        List<Patch> firstNElementsList = sortedPatches.stream()
                .limit(howManySamples.intValue())
                .collect(Collectors.toList());

        List<Patch> lastNElementsList =
                sortedPatches.subList(
                        sortedPatches.size() - howManySamples.intValue(),
                        sortedPatches.size()
                );

        results.addAll(firstNElementsList);
        results.addAll(lastNElementsList);
        // results.addAll(Utils.pickNRandom(patches, 8));
        // just take the same random samples and use them across all the representations

        results.add(patches.get(11264));
        results.add(patches.get(26076));
        results.add(patches.get(100145));
        results.add(patches.get(14891));
        results.add(patches.get(10091));
        results.add(patches.get(77564));
        results.add(patches.get(33446));
        results.add(patches.get(991));

        for (Patch patch : sortedPatches) {
            String output = String.format("representation=%s " +
                            "\ngroundTruth   =%s\n\n",
                    patch.getInferred(), patch.getGroundTruth());
            //System.out.println(output);
            System.out.println(patch);
        }
    }
}
