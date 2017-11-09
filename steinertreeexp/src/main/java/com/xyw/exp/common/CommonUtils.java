package com.xyw.exp.common;

import java.util.*;

/**
 * <P>author b4ping</P>
 * <p>created on 2017/10/19 10:35</p>
 */
public class CommonUtils {

    /**
     * <p>
     * Discription:笛卡尔乘积算法
     * 把一个List{[1,2],[3,4],[a,b]}转化成
     * List{[1,3,a],[1,3,b],[1,4,a],[1,4,b],[2,3,a],[2,3,b],[2,4,a],[2,4,b]}
     * 数组输出
     * </p>
     *
     * @param dimvalue 原List
     * @param result   通过乘积转化后的数组
     * @param layer    中间参数
     * @param curList  中间参数
     */
    public static void descartes(List<List<String>> dimvalue,
                                 List<List<String>> result, int layer, List<String> curList) {
        if (layer < dimvalue.size() - 1) {
            if (dimvalue.get(layer).size() == 0) {
                CommonUtils.descartes(dimvalue, result, layer + 1, curList);
            } else {
                for (int i = 0; i < dimvalue.get(layer).size(); i++) {
                    List<String> list = new ArrayList<String>(curList);
                    list.add(dimvalue.get(layer).get(i));
                    CommonUtils.descartes(dimvalue, result, layer + 1, list);
                }
            }
        } else if (layer == dimvalue.size() - 1) {
            if (dimvalue.get(layer).size() == 0) {
                result.add(curList);
            } else {
                for (int i = 0; i < dimvalue.get(layer).size(); i++) {
                    List<String> list = new ArrayList<String>(curList);
                    list.add(dimvalue.get(layer).get(i));
                    result.add(list);
                }
            }
        }
    }

    /**
     * 从已有列表中 随机获取数据
     * @param list
     * @param limit
     * @param <T>
     */
    public static <T> List<T> getRandoms(List<T> list, int limit) {
        List<T> result = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < limit; i++) {
            boolean always = true;
            while (always) {
                int index = random.nextInt(list.size());
                T ele = list.get(index);
                if (!result.contains(ele)) { // 重复元素不保存
                    result.add(ele);
                    always = false;
                }
            }
        }
        return result;
    }

    /**
     * 求交集
     * @param c1
     * @param c2
     * @param <T>
     * @return
     */
    public static <T> Set<T> intersection(Collection<? extends T> c1, Collection<? extends T> c2) {
        HashSet<T> set1 = new HashSet<>(c1);
        HashSet<T> set2 = new HashSet<>(c2);

        // 求交集（结果保存在了set1中）
        set1.retainAll(set2);
        return set1;
    }

    /**
     * 两个集合是否有交集
     * @param c1
     * @param c2
     * @param <T>
     * @return
     */
    public static <T> boolean haveIntersection(Collection<? extends T> c1, Collection<? extends T> c2) {
        for (T t1 : c1) {
            for (T t2 : c2) {
                if (t1.equals(t2)) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * 两个集合是否有交集(除去 exclude)
     * @param c1
     * @param c2
     * @param <T>
     * @return
     */
    public static <T> boolean haveIntersection(Collection<? extends T> c1, Collection<? extends T> c2, T ...excludes) {
        for (T t1 : c1) {
            for (T t2 : c2) {
                boolean need = true;
                for (T exclude : excludes) {
                    if (exclude.equals(t1) || exclude.equals(t2)) {
                        need = false;
                    }
                }
                if (need && t1.equals(t2)) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * 从一个数组集合中 抽取出 单个元素的集合
     * @param c
     * @param index
     * @param <T>
     * @return
     */
    public static <T> List<T> findEmelents(Collection<? extends T[]> c, int index) {
        List<T> result = new ArrayList<>();
        for (T[] ts : c) {
            result.add(ts[index]);
        }
        return result;
    }
}
