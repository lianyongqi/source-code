package com.xyw.exp.dao;

import com.xiaoleilu.hutool.util.CollectionUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * <p>author b4ping</p>
 * <p>created on 2017-10-21 9:52</p>
 */
@Component
public class MashupApiDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    @Autowired
    private NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    @CacheEvict(value="common", allEntries = true)
    public void removeCache() {
        System.out.println("--正在清空整个缓存--");
    }
    /**
     * 获取相同mashup下面的API
     *
     * @param api
     */
//    @Cacheable(value = "common")
    public List<String> findApiInSameMashup(String api) {
        String sqlApi = "select t.f_mashup, t.f_id from tb_mashup_api t where t.f_api = ?";
        List<Integer[]> mashupIds = jdbcTemplate.query(sqlApi, (rs, rowNum) -> new Integer[]{ rs.getInt(1), rs.getInt(2) }, api);

        if (CollectionUtil.isEmpty(mashupIds)) {
            return new ArrayList<>();
        }

        Set<Integer> mashups = new HashSet<>();
        List<Integer> ids = new ArrayList<>();
        for (Integer[] mashupId : mashupIds) {
            mashups.add(mashupId[0]);
            ids.add(mashupId[1] - 1);
            ids.add(mashupId[1] + 1);
        }

        String sql = "select t.f_api from tb_mashup_api t where t.f_id in (:ids) AND t.f_mashup in (:mashups)";
        MapSqlParameterSource parameterSource = new MapSqlParameterSource();
        parameterSource.addValue("mashups", new ArrayList<>(mashups));
        parameterSource.addValue("ids", ids);
        return namedParameterJdbcTemplate.queryForList(sql, parameterSource, String.class);
    }

    /**
     * count(api) > x
     * @param x api的统计数量
     * @return
     */
    public List<Integer> findMashupsByApiCountGteX(int x) {
        String sql = "select t.f_mashup from tb_mashup_api t group by t.f_mashup having count(1) = ?";
        return jdbcTemplate.queryForList(sql, Integer.class, x);
    }

    public List<String> findApisByMashup(Integer mashup) {
        String sql = "select t.f_api from tb_mashup_api t where t.f_mashup = ?";
        return jdbcTemplate.queryForList(sql, String.class, mashup);
    }
}
