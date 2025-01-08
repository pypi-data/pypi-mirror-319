import os
import sys
import pytest
from tiutools import CanvasScraper


@pytest.fixture(scope='session')
def canvas_scraper():
    reset_keys = False
    options = ["--headless=new",
               "--window-size=10000,2080"]

    canvas_scraper = CanvasScraper(options=options,
                                   namespace="canvassso",
                                   reset_keys=reset_keys)
    return canvas_scraper
