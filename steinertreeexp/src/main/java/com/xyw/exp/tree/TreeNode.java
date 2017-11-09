package com.xyw.exp.tree;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * 树节点
 * <p>author b4ping</p>
 * <p>created on 2017-10-20 14:56</p>
 * @deprecated 目前使用 Node
 */
public class TreeNode implements Serializable {
    private String id;
    private TreeNode parentNode;
    private List<TreeNode> children = new ArrayList<>();

    /** 是否已经生长 */
    private boolean developed;

    public TreeNode(String id) {
        this.id = id;
    }

    /**
     * 判断是否为叶子结点
     */
    public boolean isLeaf() {
        if (null == children || children.isEmpty()) {
            return true;
        }
        return false;
    }

    /**
     * 为当前节点插入一个父节点
     */
    public void addParentNode(TreeNode node) {
        node.addChildNode(this);
    }

    /**
     * 插入一个子节点到当前节点
     */
    public void addChildNode(TreeNode node) {
        node.parentNode = this;
        children.add(node);
    }

    /**
     * 插入多个子节点
     * @param nodes
     */
    public void addChildren(List<TreeNode> nodes) {
        for (TreeNode node : nodes) {
            this.addChildNode(node);
        }
    }

    /**
     * 返回当前节点的父节点集合【一字上升】
     */
    public List<TreeNode> findElders() {
        List<TreeNode> result = new ArrayList<>();
        if (null != this.getParentNode()) {
            result.add(this.getParentNode());
            // 此处使用了递归
            result.addAll(this.getParentNode().findElders());
        }
        return result;
    }

    /**
     * 返回当前节点的子节点集合【所有】
     */
    public List<TreeNode> findJuniors() {
        List<TreeNode> result = new ArrayList<>();
        if (null != children && !children.isEmpty()) {
            for (TreeNode child : children) {
                result.add(child);
                // 此处使用了递归
                result.addAll(child.findJuniors());
            }
        }
        return result;
    }

    /**
     * 删除当前节点及其子节点
     */
    public void deleteNode() {
        if (null != this.getParentNode()) {
            this.getParentNode().deleteChildNode(this.id);
        }
    }

    /**
     * 删除当前节点的某个子节点
     * @param id 子节点ID
     */
    public void deleteChildNode(String id) {
        int index = -1;
        for (int i = 0; i < this.getChildren().size(); i++) {
            if (this.getChildren().get(i).getId().equals(id)) {
                index = i;
                break;
            }
        }
        if (index > -1) {
            this.getChildren().remove(index);
        }
    }

    /**
     * 动态的插入一个新的节点到当前树中
     */
    public boolean insertJuniorNode(TreeNode node) {
        if (this.getId().equals(node.getParentNode().getId())) {
            addChildNode(node);
            return true;
        } else {

            boolean insertFlag;
            for (TreeNode treeNode : this.getChildren()) {
                // 此处使用了遍历
                insertFlag = treeNode.insertJuniorNode(node);
                if (insertFlag) {
                    return true;
                }
            }
            return false;
        }
    }

    /**
     * 找到一棵树中某个节点
     */
    public TreeNode findNodeById(String id) {
        if (this.id.equals(id)) {
            return this;
        }
        if (null != children && !children.isEmpty()) {
            for (TreeNode child : children) {
                // 此处使用了遍历
                TreeNode result = child.findNodeById(id);
                if (null != result) {
                    return result;
                }
            }
        }
        return null;
    }

    /**
     * 验证树的合法性
     */
    public boolean isValidTree() {
        return true;
    }

    /**
     * 遍历一棵树【层次遍历】
     */
    private void traverse(List<String> all) {
        if (null == all) {
            return;
        }
        all.add(this.id);
        if (null != children && !children.isEmpty()) {
            for (TreeNode child : children) {
                child.traverse(all);
            }
        }
    }

    public String getId() {
        return id;
    }

    public TreeNode getParentNode() {
        return parentNode;
    }

    public List<TreeNode> getChildren() {
        return children;
    }

    public boolean isDeveloped() {
        return developed;
    }

    public void setDeveloped(boolean developed) {
        this.developed = developed;
    }

    public List<String> getContent() {
        List<String> content = new ArrayList<>();
        this.traverse(content);
        return content;
    }

}
