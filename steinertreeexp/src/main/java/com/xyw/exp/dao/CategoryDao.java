package com.xyw.exp.dao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.util.*;

/**
 * <P>author b4ping</P>
 * <p>created on 2017/10/16 22:45</p>
 */
@Component
public class CategoryDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public long count() {
        String sql = "select count(1) from tb_category;";
        return jdbcTemplate.queryForObject(sql, Long.class);
    }

    /**
     * 因为主键是varchar类型，没有想到好方法随机抽取，
     * 但因为数据不多，便使用笨方法吧
     */
    public List<String> random(int categoryCount) {
        // 定位
        int count = (int) count();
        Set<Integer> randoms = new HashSet<>();
        while (randoms.size() < categoryCount) {
            int r = (new Random()).nextInt(count);
            randoms.add(r);
        }
        // 获取数据
        List<String> result = new ArrayList<>();
        for (Integer random : randoms) {
            String sql = "select t.f_category from tb_category t limit ?,1;";
            result.add(jdbcTemplate.queryForObject(sql, String.class, random));
        }
        return result;
    }
}
