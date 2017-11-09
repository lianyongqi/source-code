package com.xyw.exp.entity;

/**
 * 随机抽取的category
 * <P>author b4ping</P>
 * <p>created on 2017/10/27 22:11</p>
 */
public class RandomCategory {
    private int id;
    private int time;
    private String category;

    public RandomCategory(int time, String category) {
        this.time = time;
        this.category = category;
    }

    public RandomCategory() {
    }

    public int getTime() {
        return time;
    }

    public void setTime(int time) {
        this.time = time;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }
}
