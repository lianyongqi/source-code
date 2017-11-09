package com.xyw.exp.context.impl;

import com.xyw.exp.context.Context;

/**
 * 斯坦纳树实验 上下文 配置要求
 * <P>author b4ping</P>
 * <p>created on 2017/10/28 11:16</p>
 */
public class SteinerContext extends Context {
    @Override
    public int depthLimit() {
        return 10;
    }

    @Override
    public int expTime() {
        return 10;
    }
}
