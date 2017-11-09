package com.xyw.exp.dao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

/**
 * <P>author b4ping</P>
 * <p>created on 2017/10/30 23:54</p>
 */
@Component
public class SuccessDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public void save(int time, String type, boolean success, int demand) {
        String sql = "insert into tb_success (f_success, f_time, f_type, f_demand) values(?,?,?,?)";
        jdbcTemplate.update(sql, success ? "Y" : "N", time, type, demand);
    }
}
