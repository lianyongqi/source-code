package com.xyw.exp.tree;

import java.io.Serializable;
import java.util.*;

/**
 * 树节点
 * <p>author b4ping</p>
 * <p>created on 2017-10-20 14:56</p>
 */
public class Node implements Serializable, Comparable<Node> {
    private String id;
    private Node parentNode;
//    private List<Node> children = new ArrayList<>();

    /** 是否已经生长 */
    private boolean developed;
    /** 拥有的类别(树本身) */
    private Set<String> categories = new HashSet<>();
    /** 拥有的类别(叶子节点) */
    private Set<String> leafCategories = new HashSet<>();
    /** 叶子结点 */
    private List<String> leaves = new ArrayList<>();
    /** 树的节点（每次遍历树来获取，花费时间太长） */
    private Set<String> nodes = new HashSet<>();
    /** 树的节点个数 */
    private int nodeCount;

    public Node(String id, Collection<? extends String> categories, List<String> leaves, Collection<? extends String> nodes, Collection<? extends String> leafCategories) {
        this.id = id;
        this.categories.addAll(categories);
        this.leaves.addAll(leaves);
        this.nodes.add(id);
        this.nodes.addAll(nodes);
        this.nodeCount = this.nodes.size();
        this.leafCategories.addAll(leafCategories);
    }

    public Node(String id, Collection<? extends String> categories, String leaf, Collection<? extends String> leafCategories) {
        this.id = id;
        this.categories.addAll(categories);
        this.leaves.add(leaf);
        this.nodes.add(id);
        this.nodeCount = this.nodes.size();
        this.leafCategories.addAll(leafCategories);
    }

//    /**
//     * 判断是否为叶子结点
//     */
//    public boolean isLeaf() {
//        if (null == children || children.isEmpty()) {
//            return true;
//        }
//        return false;
//    }
//
//    /**
//     * 插入一个子节点到当前节点
//     */
//    public void addChildNode(Node node) {
//        node.parentNode = this;
//        this.children.add(node);
//    }
//
//    /**
//     * 插入多个子节点
//     * @param nodes
//     */
//    public void addChildren(List<Node> nodes) {
//        for (Node node : nodes) {
//            this.addChildNode(node);
//        }
//    }

    /**
     * 添加一个类别
     * @param category
     */
    public void addCategory(String category) {
        this.categories.add(category);
    }

    /**
     * 添加多个类别
     * @param c
     */
    public void addCategories(Collection<? extends String> c) {
        this.categories.addAll(c);
    }

//    /**
//     * 遍历一棵树【层次遍历】
//     */
//    private void traverse(List<String> all) {
//        if (null == all) {
//            return;
//        }
//        all.add(this.id);
//        if (null != children && !children.isEmpty()) {
//            for (Node child : children) {
//                child.traverse(all);
//            }
//        }
//    }

    public String getId() {
        return id;
    }

    public Node getParentNode() {
        return parentNode;
    }

//    public List<Node> getChildren() {
//        return children;
//    }

    public boolean isDeveloped() {
        return developed;
    }

    public void setDeveloped(boolean developed) {
        this.developed = developed;
    }

//    /**
//     * 获取节点内容
//     * @return
//     */
//    public List<String> getContent() {
//        List<String> content = new ArrayList<>();
//        this.traverse(content);
//        return content;
//    }

    public Set<String> getCategories() {
        return categories;
    }

    public Set<String> getLeafCategories() {
        return leafCategories;
    }

    public List<String> getLeaves() {
        return leaves;
    }

    public Set<String> getNodes() {
        return nodes;
    }

    public int getNodeCount() {
        return nodeCount;
    }

    /**
     * 实现排序功能（按节点个数排序）
     * @param o
     * @return
     */
    @Override
    public int compareTo(Node o) {
        return this.getNodeCount() - o.getNodeCount();
    }
}
