package com.xyw.exp.app;

import com.xiaoleilu.hutool.lang.Console;
import com.xyw.exp.context.Context;
import com.xyw.exp.context.impl.SteinerContext;

/**
 * 实验程序 入口
 * <P>author b4ping</P>
 * <p>created on 2017/10/19 9:03</p>
 */
public class App {
    public static void main(String[] args) {
        // 1. 初始化上下文环境
        Context context = new SteinerContext();

        for (int i = 5; i <= 6; i++) {
            context.setCategoryCount(i);

            // 2. 开启 基础实验
            Console.log("开启 基础实验");

            context.setType(Context.Type.fundamental);
            CommonApp.run(context);

            // 3. 开启 随机实验
            Console.log("开启 随机实验");

            context.setType(Context.Type.random);
            context.setRandomOneGroupApi(true);
            CommonApp.run(context);

            // 4. 开启 贪婪实验
            Console.log("开启 贪婪实验");

            context.setType(Context.Type.greedy);
            context.setRandomOneGroupApi(true);
            CommonApp.run(context);
        }
    }
}
