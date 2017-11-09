package com.xyw.exp.dao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

/**
 * <P>author b4ping</P>
 * <p>created on 2017/10/30 23:54</p>
 */
@Component
public class CosttimeDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public void save(int time, String type, int demand, double costtime) {
        String sql = "insert into tb_costtime (f_time, f_type, f_demand, f_costtime) values(?,?,?,?)";
        jdbcTemplate.update(sql, time, type, demand, costtime);
    }
}
