package com.xyw.exp.dao;

import com.xiaoleilu.hutool.lang.Console;
import junit.framework.TestCase;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

/**
 * <p>author b4ping</p>
 * <p>created on 2017-10-21 17:22</p>
 */
public class TestMashupDao extends TestCase {
    private MashupDao mashupDao;

    @Override
    public void setUp() throws Exception {
        ApplicationContext context = new ClassPathXmlApplicationContext("spring.xml");
        mashupDao = context.getBean(MashupDao.class);
    }

    public void testFindOneByRandom() {
        String category = mashupDao.findOneByRandom();
        Console.log(category);
    }
}
