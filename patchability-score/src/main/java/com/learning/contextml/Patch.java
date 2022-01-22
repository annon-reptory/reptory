package com.learning.contextml;

class Patch {
    int lineNumber;
    String inferred;
    String groundTruth;
    Double simailarity;
    Double levenshteinDistance;

    public Patch(int lineNumber,
                 String inferred,
                 String groundTruth,
                 Double simailarity,
                 Double levenshteinDistance) {
        this.lineNumber = lineNumber;
        this.inferred = inferred;
        this.groundTruth = groundTruth;
        this.simailarity = simailarity;
        this.levenshteinDistance = levenshteinDistance;
    }

    public int getLineNumber() {
        return lineNumber;
    }

    public String getInferred() {
        return inferred;
    }

    public String getGroundTruth() {
        return groundTruth;
    }

    public Double getSimailarity() {
        return simailarity;
    }

    public Double getLevenshteinDistance() {
        return levenshteinDistance;
    }

    public Double getNormalizedLevenshteinDistance() {
        // Then chose the highest score. 1.0 means an exact match.
        // ref: https://stackoverflow.com/questions/45783385/normalizing-the-edit-distance

        Integer maxLength = Utils.getLongestString(inferred, groundTruth).length();
        // normalize by length, high score wins
        Double normalizedLevenshteinDistance = (maxLength - getLevenshteinDistance()) / maxLength.doubleValue();

        return normalizedLevenshteinDistance;
    }

    @Override
    public String toString() {
        return String.format("patch=>" +
                        "lineNumber=%d," +
                        "inferred=%s" +
                        ",groundTruth=%s" +
                        ",score= %.2f" +
                        ",levenshteinDistance= %.2f" +
                        ",normalizedLevenshteinDistance= %.2f\n",
                getLineNumber(),
                getInferred(),
                getGroundTruth(),
                getSimailarity(),
                getLevenshteinDistance(),
                getNormalizedLevenshteinDistance());
    }

}
