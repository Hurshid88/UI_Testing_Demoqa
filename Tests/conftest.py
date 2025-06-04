import os.path
import time

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from Config.config import TestData
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope='function', autouse=True)
def cleanup(request):
    yield
    request.cls.driver.get(TestData.base_url)
    print("Cleaned up state")


@pytest.fixture(params=["chrome"], scope="class")
def init_driver(request):
    print("Sit tight while we are trying to setup")
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOADS_FOLDER = os.path.join(ROOT_DIR, 'Downloads')

    if request.param == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        # chrome_options.add_argument("— ignore-certificate-errors")
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": DOWNLOADS_FOLDER,  # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
        chrome_options.add_experimental_option("prefs", prefs)
        web_driver: WebDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        # web_driver = webdriver.Chrome(executable_path=chrome_executable_path, options=chrome_options)

    if request.param == "firefox":
        pass
        # options = Options()
        # options.binary_location = TestData.FIREFOX_BINARY
        # web_driver = webdriver.Firefox(executable_path=TestData.FIREFOX_EXECUTABLE_PATH, options=options)

    request.cls.driver = web_driver
    web_driver.get(TestData.base_url)
    print(TestData.base_url + " homepage loaded")
    yield web_driver
    time.sleep(2)
    web_driver.close()
    print("Tear Down")


def pytest_configure(config):
    try:
        response = requests.get(TestData.base_url)
        if str(response.status_code).startswith('5'):
            raise Exception(f"INTERNAL SERVER ERROR. {TestData.base_url} IS NOT RESPONDING")
    except requests.exceptions.ConnectionError:
        msg = f'ERR_INTERNET_DISCONNECTED OR {TestData.base_url} IS NOT RESPONDING'
        pytest.exit(msg)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    try:
        pytest_html = item.config.pluginmanager.getplugin("html")
        outcome = yield
        report = outcome.get_result()
        extra = getattr(report, "extra", [])
        if report.when == "call":
            # always add url to report
            extra.append(pytest_html.extras.url("https://my.gov.uz/"))
            xfail = hasattr(report, "wasxfail")
            if (report.skipped and xfail) or (report.failed and not xfail):
                # only add additional html on failure
                report_directory = os.path.dirname(item.config.option.htmlpath)
                file_name = report.nodeid.replace("::", "_") + ".png"
                destination_file = os.path.join(report_directory, file_name)
                feature_request = item.funcargs["request"]
                web_driver = feature_request.getfixturevalue("init_driver")
                web_driver.save_screenshot(destination_file)
                if file_name:
                    html = '<div><img src = "%s" alt="screenshot" style = "width:300px;height:300px" onclick = ' \
                           '"window.open(this.src)" align = "right" </div>' % file_name
                extra.append(pytest_html.extras.html(html))
            report.extras = extra
    except Exception as e:
        print(e)


def pytest_html_report_title(report):
    report.title = "My Gov Functional Testing"
