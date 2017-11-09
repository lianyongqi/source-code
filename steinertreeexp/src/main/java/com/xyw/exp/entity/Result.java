package com.xyw.exp.entity;

/**
 * 结果
 * <P>author b4ping</P>
 * <p>created on 2017/10/30 23:50</p>
 */
public class Result {
    /** 主键；自增 */
    private Integer id;
    /** 树的API节点 */
    private String apis;
    /** 树的API节点的个数 */
    private Integer apiCount;
    /** 实验次数 */
    private Integer time;
    /** 实验类型 */
    private String type;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getApis() {
        return apis;
    }

    public void setApis(String apis) {
        this.apis = apis;
    }

    public Integer getApiCount() {
        return apiCount;
    }

    public void setApiCount(Integer apiCount) {
        this.apiCount = apiCount;
    }

    public Integer getTime() {
        return time;
    }

    public void setTime(Integer time) {
        this.time = time;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}
