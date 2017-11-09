package com.xyw.exp.app;

import com.xiaoleilu.hutool.util.CollectionUtil;
import com.xyw.exp.common.CommonData;
import com.xyw.exp.context.Context;
import com.xyw.exp.dao.*;
import com.xyw.exp.tree.Node;
import com.xyw.exp.tree.SteinerTree;

import java.util.List;
import java.util.Map;

/**
 * 通用实验
 * <P>author b4ping</P>
 * <p>created on 2017/10/15 21:22</p>
 */
public class CommonApp {
    /**
     * 开启实验 唯一入口
     * @param context
     */
    public static void run(Context context) {
        (new CommonApp(context)).star();
    }

    /**
     * 开始试验
     */
    public void star() {
        for (int time = 0; time < context.expTime(); time++) {
            context.setTime(time);
            // 1. 获取随机抽取 X 组Category 及其 对应的 APIs
            Map<String, List<String>> commonData = CommonData.findCommonData(context, time);
            // 2. 获取 斯坦纳树
            List<Node> steinerTrees = findSteinerTrees(commonData.get("categories"), commonData.get("apis"));
            // 3. 保存到数据库
            resultDao.save(time, context.getType().toString(), steinerTrees, context.getCategoryCount());
            // 4. 成功率
            successDao.save(time, context.getType().toString(), CollectionUtil.isNotEmpty(steinerTrees), context.getCategoryCount());
        }
    }

    /**
     * 斯坦纳树 部分
     * @param categories
     * @param apis
     * @return
     */
    private List<Node> findSteinerTrees(List<String> categories, List<String> apis) {
        return SteinerTree.findTrees(apis, categories, this.context, mashupApiDao, apiCategoryDao, costtimeDao);
    }

    private CommonApp(Context context) {
        this.context = context;
        // 初始化 所使用的DAO
        daoInit();
    }

    /**
     * 初始化 所使用的DAO
     */
    private void daoInit() {
        categoryDao = context.getContext().getBean(CategoryDao.class);
        apiCategoryDao = context.getContext().getBean(ApiCategoryDao.class);
        mashupApiDao = context.getContext().getBean(MashupApiDao.class);
        resultDao = context.getContext().getBean(ResultDao.class);
        successDao = context.getContext().getBean(SuccessDao.class);
        costtimeDao = context.getContext().getBean(CosttimeDao.class);
    }

    /** 上下文 */
    private Context context;

    private CategoryDao categoryDao;
    private ApiCategoryDao apiCategoryDao;
    private MashupApiDao mashupApiDao;
    private ResultDao resultDao;
    private SuccessDao successDao;
    private CosttimeDao costtimeDao;
}
