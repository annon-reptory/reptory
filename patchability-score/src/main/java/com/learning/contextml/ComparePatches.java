package com.learning.contextml;

import org.apache.commons.text.similarity.JaroWinklerSimilarity;
import org.apache.commons.text.similarity.LevenshteinDistance;
import org.apache.commons.lang3.StringUtils;

public class ComparePatches {

    public static Double jaroWinklerSimilarity(String candidate, String groundTruth) {
        JaroWinklerSimilarity similarity = new JaroWinklerSimilarity();

        // start with the assumption there is no similarity
        Double overallSimilarity = Double.valueOf(0);

        if (!StringUtils.isEmpty(candidate) && !StringUtils.isEmpty(groundTruth)) {
            candidate = candidate.trim();
            groundTruth = groundTruth.trim();
            overallSimilarity = similarity.apply(candidate, groundTruth);
        }

        return overallSimilarity;
    }

    public static Double levenshteinDistance(String candidate, String groundTruth) {
        LevenshteinDistance levenshteinDistance = new LevenshteinDistance();

        // start with the assumption there is no similarity
        Integer distance = getLongestString(candidate, groundTruth).length();

        if (!StringUtils.isEmpty(candidate) && !StringUtils.isEmpty(groundTruth)) {
            candidate = candidate.trim();
            groundTruth = groundTruth.trim();
            distance = levenshteinDistance.apply(candidate, groundTruth);
        }

        return distance.doubleValue();
    }

    private static String getLongestString(String s1, String s2) {
        if (s1.length() > s2.length())
            return s1;
        else
            return s2;
    }
}
