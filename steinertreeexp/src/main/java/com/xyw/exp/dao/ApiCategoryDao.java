package com.xyw.exp.dao;

import com.xiaoleilu.hutool.util.CollectionUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * <P>author b4ping</P>
 * <p>created on 2017/10/19 9:21</p>
 */
@Component
public class ApiCategoryDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    @Autowired
    private NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    public List<String> findApisByCategory(String category) {
        String sql = "select t.f_api from tb_api_category t where t.f_category = ?";
        return jdbcTemplate.queryForList(sql, String.class, category);
    }

    @Cacheable(value = "common")
    public List<String> findCategoriesByApi(String api) {
        String sql = "select t.f_category from tb_api_category t where t.f_api = ?";
        return jdbcTemplate.queryForList(sql, String.class, api);
    }

    /**
     * 在表tb_mashup_api表中获取对应的APIs并在tb_api_category获取APIs对应的Categories
     * @param mashup
     * @return
     */
    public List<String> findCategoriesByApiByMashup(String mashup) {
        String sql = "select t.f_category from tb_api_category t WHERE t.f_api IN (SELECT t1.f_api FROM tb_mashup_api t1 WHERE t1.f_mashup = ?)";
        return jdbcTemplate.queryForList(sql, String.class, mashup);
    }

    public List<String> findApisByCategories(List<String> categories) {
        String sql = "select t.f_api from tb_api_category t where t.f_category in (:categories)";
        return namedParameterJdbcTemplate.queryForList(sql, new MapSqlParameterSource("categories", categories), String.class);
    }

    /**
     * 获取关联category最多的api
     * @param apis
     * @return
     */
    public String findApiByGreedyCategory(List<String> apis) {
        String sql = "select t.f_api from tb_api_category t where t.f_api in (:apis) group by t.f_api order by count(1) desc limit 1";
        List<String> query = namedParameterJdbcTemplate.query(sql, new MapSqlParameterSource("apis", apis), (rs, rowNum) -> rs.getString(1));
        if (CollectionUtil.isNotEmpty(query)) {
            return query.get(0);
        }
        return null;
//        return namedParameterJdbcTemplate.queryForObject(sql, new MapSqlParameterSource("apis", apis), String.class);
    }
}
