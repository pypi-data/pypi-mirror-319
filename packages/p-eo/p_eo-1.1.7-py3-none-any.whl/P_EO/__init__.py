from P_EO.common.config import Default, LogConfig
from P_EO.core.driver import WebDriverManager, chrome_driver, debug_chrome_driver
from P_EO.core.elements import Element, Elements, IFrame
from P_EO.core.page import Page

VERSION = '1.1.7'

__all__ = [
    Element,
    Elements,
    IFrame,
    Page,
    Default,
    LogConfig,
    WebDriverManager,
    chrome_driver,
    debug_chrome_driver,
]
