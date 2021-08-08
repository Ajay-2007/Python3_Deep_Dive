import pytest
from selenium import webdriver
import time


@pytest.mark.web
class WebTest(object):
    # def test_page_is_up(self):
    #     driver = webdriver.Firefox()
    #     driver.get("https://convertlive.com/c/convert/data-size")
    #     assert "converter" in driver.title, "Cannot detect website being available"
    #     driver.close()

    def test_convert_Mb_to_mb(self):
        driver = webdriver.Firefox()
        driver.get("https://convertlive.com/c/convert/data-size")
        input_field = driver.find_element_by_id("convert-value")
        input_field.clear()
        input_field.send_keys("350")
        driver.find_element_by_id("convert-submit").click()
        time.sleep(0.5)
        result_field = driver.find_element_by_class_name("result-to")
        assert "2800" in result_field.text, "Cannot detect right result for conversion"
        driver.close()
