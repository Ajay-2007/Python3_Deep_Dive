from tests.web.nginx import nginxServer
import pytest
from selenium import webdriver
import time
import os
from tests.web.nginx import nginxServer


@pytest.mark.web
class WebTest(object):
    def test_page_is_up(self):
        driver = webdriver.Firefox()
        driver.get("https://convertlive.com/c/convert/data-size")
        assert "converter" in driver.title, "Cannot detect website being available"
        driver.close()

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

    def test_local_site(self):
        driver = webdriver.Firefox()
        # start nginx
        with nginxServer(os.path.join(os.getcwd(), "web", "nginx.conf")):
            driver.get("http://localhost:8090")
            assert (
                "Test Form" in driver.title
            ), "Cannot detect the site being accessible"

            firstint = driver.find_element_by_id("firstint")
            firstint.clear()
            firstint.send_keys("4")

            secondint = driver.find_element_by_id("secondint")
            secondint.clear()
            secondint.send_keys("5")

            calculate_button = driver.find_element_by_id("calculate")
            calculate_button.click()

            time.sleep(0.5)
            result = driver.find_element_by_id("result")
            assert "9" in result.text, "The sum result was invalid!"
        driver.close()
