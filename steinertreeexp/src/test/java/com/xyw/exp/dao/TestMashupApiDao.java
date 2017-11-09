package com.xyw.exp.dao;

import junit.framework.TestCase;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.util.List;

/**
 * <p>author b4ping</p>
 * <p>created on 2017-10-21 17:22</p>
 */
public class TestMashupApiDao extends TestCase {
    private MashupApiDao mashupApiDao;

    @Override
    public void setUp() throws Exception {
        ApplicationContext context = new ClassPathXmlApplicationContext("spring.xml");
        mashupApiDao = (MashupApiDao) context.getBean("mashupApiDao");
    }

    public void testFindApiInSameMashup() {
        List<String> apis = mashupApiDao.findApiInSameMashup("Google Maps");
        for (String api : apis) {
            System.out.println(api);
        }
    }

    public void testRemoveCache() {
        mashupApiDao.removeCache();
    }
}
