package com.xyw.exp.common;

import com.xiaoleilu.hutool.util.CollectionUtil;
import com.xyw.exp.context.Context;
import com.xyw.exp.dao.ApiCategoryDao;
import com.xyw.exp.dao.MashupApiDao;
import com.xyw.exp.dao.MashupDao;
import com.xyw.exp.dao.RandomCategoryDao;

import java.util.*;

/**
 * 基础数据处理
 * <P>author b4ping</P>
 * <p>created on 2017/10/27 22:17</p>
 */
public class CommonData {
    private Context context;
    private CommonData(Context context) {
        this.context = context;
        daoInit();
    }

    /**
     * 随机抽取Mashup，获取对应的APIs （随机抽取 X 组），获取每组 APIs 对应的 一个Category（category不允许重复），获取每组Category的所有API
     * @param context 实验需要的上下文配置
     * @param time 第几次随机抽取
     * @return 抽取的category及其对应的apis
     */
    public static Map<String, List<String>> findCommonData(Context context, int time) {
        return new CommonData(context).findCommonData(time);
    }

    private Map<String,List<String>> findCommonData(int time) {
        // 1. 判断是否已存在抽取的数据
        List<String[]> categoryAndApis = randomCategoryDao.findCategoryAndApis(time, context.getCategoryCount());
        if (CollectionUtil.isEmpty(categoryAndApis)) {
            // 重新抽取数据
            categoryAndApis = extract(time);
        }

        return commonData(categoryAndApis);
    }

    private Map<String,List<String>> commonData(List<String[]> categoryAndApis) {
        // 获取 categories 对应的所有 apis
        List<String> categories = CommonUtils.findEmelents(categoryAndApis, 0);
        List<String> apis;
        if (context.isRandomOneGroupApi()) {
            apis = CommonUtils.findEmelents(categoryAndApis, 1);
        } else {
            apis = apiCategoryDao.findApisByCategories(categories);
        }

        Map<String, List<String>> result = new HashMap<>();
        result.put("categories", categories);
        result.put("apis", apis);
        return result;
    }

    /**
     * 抽取数据
     * @param time
     */
    private List<String[]> extract(int time) {
        // 1. 随机抽取Mashup（满足对应的API的数量 >= x）
        Integer mashup = randomMashup();
        // 2. 获取 mashup 对应的 api
        List<String> apis = mashupApiDao.findApisByMashup(mashup);
        // 3. 随机抽取 X 组 category
        return ramdomCategories(mashup, apis, time);
    }

    private Integer randomMashup() {
        List<Integer> mashups = mashupApiDao.findMashupsByApiCountGteX(context.getCategoryCount());
        return mashups.get(new Random().nextInt(mashups.size()));
    }

    /**
     * 随机抽取 x 组category 并保存到数据库
     * @param mashup
     * @param apis
     * @param time
     */
    private List<String[]> ramdomCategories(Integer mashup, List<String> apis, int time) {
//        List<String[]> result;
//
//        while (true) {
//            result = new ArrayList<>();
//            // 1. 随机抽取
//            List<String> randomApis = CommonUtils.getRandoms(apis, context.categoryCount());
//            // 2. 获取 每组 API 对应的 category（category不允许重复）
//            for (String api : randomApis) {
//                List<String> categories = apiCategoryDao.findCategoriesByApi(api);
//                if (!randomCategory(result, categories, api)) {
//                    break;
//                }
//            }
//            if (result.size() == context.categoryCount()) {
//                break;
//            }
//        }
//        // 保存到数据库
//        randomCategoryDao.save(time, result);
//        return result;
        List<String[]> result = new ArrayList<>();
        // 1. 随机抽取
        List<String> randomApis = CommonUtils.getRandoms(apis, context.getCategoryCount());
        // 2. 获取 每组 API 对应的 category（category不允许重复）
        for (String api : randomApis) {
            List<String> categories = apiCategoryDao.findCategoriesByApi(api);
            if (!randomCategory(result, categories, api)) {
                break;
            }
        }
        if (result.size() != context.getCategoryCount()) {
            return extract(time);
        } else {
            // 保存到数据库
            randomCategoryDao.save(time, mashup, result, context.getCategoryCount());
            return result;
        }
    }

    private boolean randomCategory(List<String[]> result, List<String> categories, String api) {
        if (CollectionUtil.isEmpty(categories)) {
            return false;
        }
        int index = new Random().nextInt(categories.size());
        String category = categories.get(index);
        if (!contains(result, 0, category)) {
            result.add(new String[]{ category, api });
            return true;
        } else {
            // 删除该categories 递归循环
            categories.remove(index);
            return randomCategory(result, categories, api);
        }
    }

    private boolean contains(List<String[]> result, int index, String category) {
        for (String[] strings : result) {
            if (category.equals(strings[index])) {
                return true;
            }
        }
        return false;
    }

    private void daoInit() {
        randomCategoryDao = context.getContext().getBean(RandomCategoryDao.class);
        mashupDao = context.getContext().getBean(MashupDao.class);
        apiCategoryDao = context.getContext().getBean(ApiCategoryDao.class);
        mashupApiDao = context.getContext().getBean(MashupApiDao.class);
    }

    private RandomCategoryDao randomCategoryDao;
    private MashupDao mashupDao;
    private ApiCategoryDao apiCategoryDao;
    private MashupApiDao mashupApiDao;
}
