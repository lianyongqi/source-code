package com.xyw.exp.config;

import com.alibaba.druid.pool.DruidDataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;

import javax.sql.DataSource;

/**
 * Spring上下文配置
 * <P>author b4ping</P>
 * <p>created on 2017/10/15 20:46</p>
 */
@Configuration
@PropertySource(value = { "classpath:application.properties" })
public class ContextConfig {

    @Value("${datasource.url}")
    private String url;
    @Value("${datasource.username}")
    private String username;
    @Value("${datasource.password}")
    private String password;

    /**
     * 数据源配置
     */
    @Bean
    public DataSource dataSource() {
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setUrl(url); // 数据库路径
        dataSource.setUsername(username); // 账号
        dataSource.setPassword(password); // 密码
        dataSource.setInitialSize(1); // 池启动时创建的链接数量
        dataSource.setMinIdle(1); // 在不创建新连接的情况下，池中保持空闲的最小连接数
        dataSource.setMaxActive(10); // 同一时间可从池中分配的最多连接数（如果设置为0，表示无限制）

        return dataSource;
    }

    /**
     * Spring JDBC配置
     */
    @Bean
    public JdbcTemplate jdbcTemplate() {
        JdbcTemplate jdbcTemplate = new JdbcTemplate();
        jdbcTemplate.setDataSource(dataSource());
        return  jdbcTemplate;
    }

    /**
     * Spring JDBC配置(升级版)
     * @return
     */
    @Bean
    public NamedParameterJdbcTemplate namedParameterJdbcTemplate() {
        return new NamedParameterJdbcTemplate(dataSource());
    }
}
