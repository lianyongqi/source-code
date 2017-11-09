package com.xyw.exp.dao;

import com.xyw.exp.tree.Node;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BatchPreparedStatementSetter;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.List;
import java.util.Set;

/**
 * <P>author b4ping</P>
 * <p>created on 2017/10/30 23:54</p>
 */
@Component
public class ResultDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public void save(int time, String type, List<Node> trees, int demand) {
        String sql = "insert into tb_result (f_apis, f_api_count, f_time, f_type, f_demand) values(?,?,?,?,?)";
        jdbcTemplate.batchUpdate(sql, new BatchPreparedStatementSetter() {
            @Override
            public void setValues(PreparedStatement ps, int i) throws SQLException {
                Node tree = trees.get(i);
                Set<String> content = tree.getNodes();
                ps.setString(1, Arrays.toString(content.toArray()));
                ps.setInt(2, content.size());
                ps.setInt(3, time);
                ps.setString(4, type);
                ps.setInt(5, demand);
            }

            @Override
            public int getBatchSize() {
                return trees.size();
            }
        });
    }
}
