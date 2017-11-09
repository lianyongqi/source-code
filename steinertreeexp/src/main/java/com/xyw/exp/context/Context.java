package com.xyw.exp.context;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

/**
 * 实验环境上下文配置
 * <P>author b4ping</P>
 * <p>created on 2017/10/28 11:00</p>
 */
public abstract class Context {
    protected ApplicationContext context;
    /** 实验类型 */
    protected Type type;
    /** 数据准备时，是否随机抽取一组api，满足需求 C1C2C3 （即每组category随机抽取一个API，API可以重复） */
    public boolean randomOneGroupApi;
    /** 获取 实验需求的随机抽取category的数量 */
    public int categoryCount;
    /** 第X次试验 */
    private int time;

    public Context() {
        this.context = new ClassPathXmlApplicationContext("spring.xml");
    }

    /** 斯坦纳树深度限制 */
    public abstract int depthLimit();
    /** 实验次数 */
    public abstract int expTime();

    public ApplicationContext getContext() {
        return context;
    }

    public Type getType() {
        return type;
    }

    public void setType(Type type) {
        this.type = type;
    }

    public boolean isRandomOneGroupApi() {
        return randomOneGroupApi;
    }

    public void setRandomOneGroupApi(boolean randomOneGroupApi) {
        this.randomOneGroupApi = randomOneGroupApi;
    }

    public int getCategoryCount() {
        return categoryCount;
    }

    public void setCategoryCount(int categoryCount) {
        this.categoryCount = categoryCount;
    }

    public int getTime() {
        return time;
    }

    public void setTime(int time) {
        this.time = time;
    }

    public enum Type {
        /** 基础实验 */
        fundamental,
        /** 随机实验 */
        random,
        /** 贪婪实验 */
        greedy;
    }
}
