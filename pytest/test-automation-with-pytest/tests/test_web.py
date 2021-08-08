import pytest
from selenium import webdriver
import time
import os
from tests.web.nginx import nginxServer, NginxConfig
from utils import wait_for


@pytest.mark.web
class WebTest(object):
    def test_page_is_up(self, web_driver, expensive_operations):
        web_driver.get("https://convertlive.com/c/convert/data-size")
        assert "converter" in web_driver.title, "Cannot detect website being available"

    def test_convert_Mb_to_mb(self, web_driver):
        web_driver.get("https://convertlive.com/c/convert/data-size")
        input_field = web_driver.find_element_by_id("convert-value")
        input_field.clear()
        input_field.send_keys("350")
        web_driver.find_element_by_id("convert-submit").click()
        result_field = web_driver.find_element_by_class_name("result-to")
        assert "2800" in result_field.text, "Cannot detect right result for conversion"

    def test_local_site(self, web_driver):
        config = NginxConfig(location=os.path.join(os.getcwd(), "tests", "web"))
        # start nginx
        with nginxServer(config):
            web_driver.get("http://localhost:8090")
            assert (
                "Test Form" in web_driver.title
            ), "Cannot detect the site being accessible"

            firstint = web_driver.find_element_by_id("firstint")
            firstint.clear()
            firstint.send_keys("4")

            secondint = web_driver.find_element_by_id("secondint")
            secondint.clear()
            secondint.send_keys("5")

            calculate_button = web_driver.find_element_by_id("calculate")
            calculate_button.click()

            wait_for(
                condition=lambda: web_driver.find_element_by_id("result").text.strip()
                != "",
                timeout=10,
                poll_frequency=0.5,
                msg="Cannot detect the result of the sum in time!",
            )
            result = web_driver.find_element_by_id("result")
            assert "9" in result.text, "The sum result was invalid!"
