package com.learning.contextml;

import java.util.Collections;
import java.util.LinkedList;
import java.util.List;

public class Utils {

    public static List<Patch> pickNRandom(List<Patch> patches, int n) {
        List<Patch> copy = new LinkedList<>(patches);
        Collections.shuffle(copy);
        return copy.subList(0, n);
    }

    static String getLongestString(String s1, String s2) {
        if (s1.length() > s2.length())
            return s1;
        else
            return s2;
    }
}
