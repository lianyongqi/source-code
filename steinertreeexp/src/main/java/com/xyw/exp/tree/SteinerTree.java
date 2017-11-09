package com.xyw.exp.tree;

import com.xiaoleilu.hutool.lang.Console;
import com.xiaoleilu.hutool.util.CollectionUtil;
import com.xiaoleilu.hutool.util.StrUtil;
import com.xyw.exp.common.CommonUtils;
import com.xyw.exp.context.Context;
import com.xyw.exp.dao.ApiCategoryDao;
import com.xyw.exp.dao.CosttimeDao;
import com.xyw.exp.dao.MashupApiDao;

import java.util.*;

/**
 * 斯坦纳树帮助类
 * <div>终止条件：1. 深度范围超出终止； 2. 如果没有新生长树 则终止</div>
 * <p>author b4ping</p>
 * <p>created on 2017-10-20 16:34</p>
 */
public class SteinerTree {
    /** 实验环境上下文 */
    private Context context;
    /**
     * 第一棵斯坦纳树的节点个数
     */
    private int count = -1;
    /** 树的深度（按最深的树计算） */
    private int depth = 1;
    /**
     * 队列中的树
     */
    private List<Node> trees = new ArrayList<>();
    /**
     * 需要满足的categories
     */
    private List<String> categories;
    /**
     * 有效的斯坦纳树 作为结果 返回
     */
    private List<Node> validTrees = new ArrayList<>();
    private MashupApiDao mashupApiDao;
    private ApiCategoryDao apiCategoryDao;
    private CosttimeDao costtimeDao;

    private SteinerTree(List<String> apis, List<String> categories, Context context, MashupApiDao mashupApiDao, ApiCategoryDao apiCategoryDao, CosttimeDao costtimeDao) {
        this.categories = categories;
        this.context = context;
        this.mashupApiDao = mashupApiDao;
        this.apiCategoryDao = apiCategoryDao;
        this.costtimeDao = costtimeDao;
        initTrees(apis);
    }

    private void initTrees(List<String> originApis) {
        // 1. 去重
        Set<String> apis = new HashSet<>(originApis);
        // 2. 循环遍历 初始化 树
        for (String api : apis) {
            // 获取api 对应的 categories
            Set<String> categories = CommonUtils.intersection(this.categories, apiCategoryDao.findCategoriesByApi(api));
            Node tree = new Node(api, categories, api, categories);
            // 校验树的合法性
            valid(tree, null);
            // 添加到 队列
            trees.add(tree);

            Console.log("树: {}", Arrays.toString(tree.getNodes().toArray()));
        }

        Console.log("初始化树： {}", this.trees.size());
    }

    /**
     * 校验树的合法性
     *
     * @param tree
     * @param trees
     */
    private boolean valid(Node tree, List<Node> trees) {
        if (validNodeCount(tree)) {
            if (validSteinerTree(tree)) {
                if (-1 == this.count) {
                    this.count = tree.getNodeCount();
                }
                this.validTrees.add(tree);
                Console.log("斯坦纳树： {}", Arrays.toString(tree.getNodes().toArray()));
                return true;
            } else if (null != trees && toNeedDevelop(tree)) {
                Console.log("生长树: {}", Arrays.toString(tree.getNodes().toArray()));
                trees.add(tree);
            }
        }
        return false;
    }

    /**
     * 校验 斯坦纳树的 合法性
     *
     * @param tree
     * @return
     */
    private boolean validSteinerTree(Node tree) {
        return tree.getCategories().containsAll(this.categories);
    }

    /**
     * 校验 树的节点个数 合法性
     *
     * @param tree
     * @return
     */
    private boolean validNodeCount(Node tree) {
        if (this.count == -1) {
            return true;
        }
        if (tree.getNodeCount() <= this.count) {
            return true;
        }
        return false;
    }

    /**
     * 获取斯坦纳树
     */
    public static List<Node> findTrees(List<String> apis, List<String> categories, Context context, MashupApiDao mashupApiDao, ApiCategoryDao apiCategoryDao, CosttimeDao costtimeDao) {
        return new SteinerTree(apis, categories, context, mashupApiDao, apiCategoryDao, costtimeDao).start();
    }

    /**
     * 开始
     */
    private List<Node> start() {
        long startTime = System.currentTimeMillis();

        // 生长
        develop();

        long endTime = System.currentTimeMillis();
        costtimeDao.save(context.getTime(), context.getType().toString(), context.getCategoryCount(), endTime - startTime);

        Collections.sort(validTrees);
        return this.validTrees;
    }

    /**
     * 合并
     */
    private void merger() {
        Console.log("合并操作");

        List<Node> newTrees = new ArrayList<>();
        for (int i = 0; i < trees.size(); i++) {
            Node tree1 = trees.get(i);
            for (int j = i + 1; j < trees.size(); j++) {
                Node tree2 = trees.get(j);

                // 1. 不同category的树 进行合并操作
                // 2. 判断根节点是否一致
                // 3. 判断除根节点外不允许有其他相同节点
                // 暂时去掉 需求增加限定 && !CommonUtils.haveIntersection(tree1.getLeafCategories(), tree2.getLeafCategories())
                if (toNeedMerge(tree1, tree2) && tree1.getId().equals(tree2.getId()) && notHaveSameNode(tree1, tree2)) {
                    // 合并
                    Node rootTree = merger(tree1, tree2);
                    if (!haveOptimal(newTrees, rootTree)) {
                        // 校验树的合法性
                        boolean valid = valid(rootTree, newTrees);
                        // 是否结束递归
                        if (isEnd(valid)) {
                            return;
                        }
                    }
                }
            }
        }
        this.trees.addAll(newTrees);
        Collections.sort(trees);

        Console.log("目前斯坦纳树的个数： {}", this.validTrees.size());

        // 递归 到 生长操作
        develop();
    }

    /**
     * 是否需要合并
     * @param tree1
     * @param tree2
     * @return
     */
    private boolean toNeedMerge(Node tree1, Node tree2) {
        // 需求增加
        if (isSumAdd(tree1, tree2)) {
            if (count == -1) {
                return true;
            }
            if (tree1.getNodeCount() + tree2.getNodeCount() <= count + 1) {
                return true;
            }
        }
        return false;
    }

    private boolean isSumAdd(Node tree1, Node tree2) {
        HashSet<String> set = new HashSet<>(tree1.getCategories());
        set.addAll(tree2.getCategories());
        if (set.size() > tree1.getCategories().size() && set.size() > tree2.getCategories().size()) {
            return true;
        }
        return false;
    }

    private boolean isEnd(boolean valid) {
        // 随机实验 只获取第一个结果
        if (valid && Context.Type.random == context.getType()) {
            return true;
        }
        return false;
    }

    /**
     * 合并两棵树
     *
     * @param tree1
     * @param tree2
     */
    private Node merger(Node tree1, Node tree2) {
        // 获取api 对应的 categories
        List<String> categories = new ArrayList<>();
        categories.addAll(tree1.getCategories());
        categories.addAll(tree2.getCategories());
        // 叶子节点
        List<String> leaves = new ArrayList<>();
        leaves.addAll(tree1.getLeaves());
        leaves.addAll(tree2.getLeaves());
        // 所有节点
        Set<String> nodes = new HashSet<>();
        nodes.addAll(tree1.getNodes());
        nodes.addAll(tree2.getNodes());
        // 获取叶子结点 对应 的API
        List<String> leafCategories = new ArrayList<>();
        leafCategories.addAll(tree1.getLeafCategories());
        leafCategories.addAll(tree2.getLeafCategories());

        Node rootTree = new Node(tree1.getId(), categories, leaves, nodes, leafCategories);

        return rootTree;
    }

    /**
     * 判断除根节点外没有其他相同节点
     *
     * @param tree1
     * @param tree2
     * @return
     */
    private boolean notHaveSameNode(Node tree1, Node tree2) {
        return !CommonUtils.haveIntersection(tree1.getNodes(), tree2.getNodes(), tree1.getId());
    }

    /**
     * 生长
     */
    private void develop() {
        Console.log("生长操作");
        // 深度范围超出终止
        if (depth > context.depthLimit()) {
            return;
        }
        // 树的生长
        List<Node> newTrees = new ArrayList<>();
        if (!develop(newTrees)) {
            return;
        }

        // 第一次生长完毕后，清空原来的单节点树（因为只有叶子节点才能满足实验条件，所以单节点树不能进行合并操作）
        if (1 == depth) {
            trees.clear();
        }

        // 如果没有新生长树 则终止
        if (0 == newTrees.size()) {
            return;
        }

        // 添加到队列
        trees.addAll(newTrees);
        Collections.sort(trees);

        // 深度+1
        depth++;

        Console.log("目前斯坦纳树的个数： {}", this.validTrees.size());

        // 递归 到 合并操作
        merger();
    }

    /**
     * 树的生长
     * @param newTrees
     * @return
     */
    private boolean develop(List<Node> newTrees) {
        Console.log("树的数量： {}", this.trees.size());
        for (Node tree : trees) {
            // 判断该树 是否 已经生长 过，已生长则不需再生长
            if (!tree.isDeveloped() && toNeedDevelop(tree)) {
                // 该树中已存在的节点
                Set<String> already = null;

                // 实验不同 生长方式不同
                // 获取 待生长 的节点
                List<String> apis = findApis4Develop(tree);
                for (String api : apis) {
                    if (null == already) {
                        already = tree.getNodes();
                    }
                    // 判断树中是否已存在该节点 若存在不生长
                    if (!already.contains(api)) {
                        // 执行生长操作
                        // 获取api 对应的 categories（使用子节点的categories）
                        Set<String> categories = CommonUtils.intersection(this.categories, apiCategoryDao.findCategoriesByApi(api));
                        categories.addAll(tree.getCategories());
                        Node rootTree = new Node(api, categories, tree.getLeaves(), tree.getNodes(), tree.getLeafCategories());

                        // 判断 新生长树 是否在 队列中 已有最优树，有则不添加到队列中
                        if (!haveOptimal(newTrees, rootTree)) {
                            // 校验树的合法性
                            boolean valid = valid(rootTree, newTrees);
                            // 是否结束递归
                            if (isEnd(valid)) {
                                return false;
                            }
                        }
                    }
                }
            }
            // 将该树设置为已生成
            tree.setDeveloped(true);
        }
        return true;
    }

    /**
     * 判断该树是否需要生长
     * @param tree
     * @return
     */
    private boolean toNeedDevelop(Node tree) {
        if (this.count == -1) {
            return true;
        }
        if (tree.getNodeCount() < this.count) {
            return true;
        }
        return false;
    }

    /**
     * 判断 新生长树 是否在 队列中 已有最优树
     * <div>判断叶子结点是否包含与根节点是否一样</div>
     *
     * @param otherTrees
     * @param newTree
     * @return
     */
    private boolean haveOptimal(List<Node> otherTrees, Node newTree) {
        for (Node tree : this.trees) {
            if (newTree.getId().equals(tree.getId()) && tree.getLeaves().size() == newTree.getLeaves().size() && tree.getLeaves().containsAll((newTree.getLeaves()))) {
                return true;
            }
        }
        for (Node tree : otherTrees) {
            if (newTree.getId().equals(tree.getId()) && tree.getLeaves().size() == newTree.getLeaves().size() && tree.getLeaves().containsAll((newTree.getLeaves()))) {
                return true;
            }
        }
        return false;
    }

    /**
     * 实验不同 获取的节点 不同
     * @return
     * @param tree
     */
    private List<String> findApis4Develop(Node tree) {
        List<String> result = new ArrayList<>();

        List<String> list = mashupApiDao.findApiInSameMashup(tree.getId());
        // 基础实验 获取所有api
        if (context.getType() == Context.Type.fundamental) {
            return list;
        }

        // 随机实验 随机一个api
        if (context.getType() == Context.Type.random) {
            return list;
        }

        // 贪婪实验 选择关联category最多的节点
        if (context.getType() == Context.Type.greedy) {
            if (CollectionUtil.isNotEmpty(list)) {
                String api = apiCategoryDao.findApiByGreedyCategory(list);
                if (StrUtil.isNotBlank(api)) {
                    result.add(api);
                }
            }
        }

        return result;
    }
}
