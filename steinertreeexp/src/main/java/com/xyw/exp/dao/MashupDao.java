package com.xyw.exp.dao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

/**
 * <P>author b4ping</P>
 * <p>created on 2017/10/27 22:47</p>
 */
@Component
public class MashupDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    /**
     * 随机抽取一个mashup
     *
     * @return
     */
    public String findOneByRandom() {
        String sql = "SELECT t.f_mashup FROM tb_mashup t WHERE t.f_id >= ((SELECT MAX(f_id) FROM tb_mashup) - (SELECT min(f_id) FROM tb_mashup)) * rand() + (SELECT min(f_id) FROM tb_mashup) limit 1";
        return jdbcTemplate.queryForObject(sql, String.class);
    }
}
