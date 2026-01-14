import pytest
from dash.testing.browser import Browser
from app import app


@pytest.fixture
def dash_app():
    """Fixture to provide the Dash app for testing."""
    return app


def test_header_is_present(dash_app):
    """Test that the header with the app title is present."""
    assert dash_app.layout is not None
    
    # Convert layout to string to check for the header text
    layout_str = str(dash_app.layout)
    assert "Soul Foods Pink Morsel Sales Visualiser" in layout_str


def test_visualization_is_present(dash_app):
    """Test that the visualization (Graph component) is present."""
    assert dash_app.layout is not None
    
    # Check that the graph component with id 'sales-chart' exists
    layout_str = str(dash_app.layout)
    assert "sales-chart" in layout_str


def test_region_picker_is_present(dash_app):
    """Test that the region picker (RadioItems component) is present."""
    assert dash_app.layout is not None
    
    # Check that the radio filter component with id 'region-filter' exists
    layout_str = str(dash_app.layout)
    assert "region-filter" in layout_str
    
    # Check that all region options are present
    assert "all" in layout_str.lower()
    assert "north" in layout_str.lower()
    assert "east" in layout_str.lower()
    assert "south" in layout_str.lower()
    assert "west" in layout_str.lower()
