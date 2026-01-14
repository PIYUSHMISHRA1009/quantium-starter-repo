import sys
from pathlib import Path

import pytest
import requests
from bs4 import BeautifulSoup
from dash.testing.application_runners import ThreadedRunner

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app


@pytest.fixture
def server():
    runner = ThreadedRunner(app)
    with runner:
        runner.start()
        yield runner


def get_soup(runner):
    response = requests.get(runner.url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def test_header_present(server):
    soup = get_soup(server)
    header = soup.find("h1")
    assert header is not None
    assert "Soul Foods Pink Morsel Sales Visualiser" in header.text


def test_visualisation_present(server):
    soup = get_soup(server)
    graph = soup.find(id="sales-chart")
    assert graph is not None


def test_region_picker_present(server):
    soup = get_soup(server)
    radio_root = soup.find(id="region-filter")
    options = soup.select("#region-filter input[type='radio']")
    assert radio_root is not None
    assert len(options) == 5
