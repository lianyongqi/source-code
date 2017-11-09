package com.xyw.exp;

import com.xiaoleilu.hutool.lang.Console;
import com.xiaoleilu.hutool.util.CollectionUtil;
import com.xiaoleilu.hutool.util.NumberUtil;
import com.xyw.exp.common.CommonUtils;
import junit.framework.TestCase;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * <p>author b4ping</p>
 * <p>created on 2017-10-21 9:33</p>
 */
public class TestCommon extends TestCase {

    public void testIntersection() {
        List<String> list1 = new ArrayList<>();
        list1.add("1");
        list1.add("2");
        list1.add("3");

        List<String> list2 = new ArrayList<>();
//        list2.add("2");
//        list2.add("3");
        list2.add("4");

        Set<String> set = CommonUtils.intersection(list1, list2);
        Console.log(CollectionUtil.isEmpty(set));
        for (String s : set) {
            Console.log(s);
        }
    }

    /**
     * 去重
     */
    public void testDeleteRepetition() {
        List<String> list = new ArrayList<>();
        list.add("1");
        list.add("2");
        list.add("2");
        list.add("1");
        list.add("3");
        for (String s : list) {
            System.out.println(MessageFormat.format("list_ele: {0}", s));
        }
        Set<String> set = new HashSet<>(list);
        for (String s : set) {
            System.out.println(MessageFormat.format("set_ele: {0}", s));
        }
    }

    public void testListContainAll() {
        List<String> list = new ArrayList<>();
        list.add("1");
        list.add("2");
        list.add("3");

        List<String> list2 = new ArrayList<>();
        list2.add("1");
        list2.add("4");

        Console.log(list.containsAll(list2));
    }

    public void testIntegerEquals() {
        Console.log(new Integer(876).equals("876"));
    }

    public void testHaveIntersection() {
        List<String> list1 = new ArrayList<>();
        list1.add("1");
        list1.add("2");
        list1.add("3");
        List<String> list2 = new ArrayList<>();
        list2.add("6");
        list2.add("2");
        list2.add("5");

        Console.log(CommonUtils.haveIntersection(list1, list2, "2"));
    }

    public void testDiv() {
        Console.log(NumberUtil.div(20.0, 1000.0, 3));
    }

    @Override
    public void setUp() throws Exception {
        super.setUp();
    }

    @Override
    public void tearDown() throws Exception {
        super.tearDown();
    }
}
