package com.xyw.exp.dao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BatchPreparedStatementSetter;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;

/**
 * 数据准备时，随机抽取的数据保存，保持数据一致性
 * <P>author b4ping</P>
 * <p>created on 2017/10/27 22:35</p>
 */
@Component
public class RandomCategoryDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    /**
     * 获取最新time次的Categories
     * @param time
     * @param demand
     * @return
     */
    public List<String[]> findCategoryAndApis(int time, int demand) {
        String sql = "select t.f_category, t.f_api from tb_random_category t where t.f_time = ? AND t.f_demand = ?";
        return jdbcTemplate.query(sql, (rs, rowNum) -> new String[]{ rs.getString(1), rs.getString(2) }, time, demand);
    }

    public void save(int time, Integer mashup, List<String[]> categoryAndApis, int demand) {
        String sql = String.format("insert into tb_random_category (f_time, f_category, f_api, f_mashup_id, f_demand) values (%d, ?, ?, ?,?)", time);
        jdbcTemplate.batchUpdate(sql, new BatchPreparedStatementSetter() {
            @Override
            public void setValues(PreparedStatement ps, int i) throws SQLException {
                ps.setString(1, categoryAndApis.get(i)[0]);
                ps.setString(2, categoryAndApis.get(i)[1]);
                ps.setInt(3, mashup);
                ps.setInt(4, demand);
            }

            @Override
            public int getBatchSize() {
                return categoryAndApis.size();
            }
        });

    }
}
