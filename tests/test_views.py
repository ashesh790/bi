import pytest
from unittest.mock import Mock, patch
from user_1.apis.fetch_api.advance_filter_functions import search_properties
from user_1.apis.fetch_api.main_functions import get_location_name
from user_1.views import show_property_location_wise

@pytest.fixture
def mock_request():
    # Create a mock request object with session data
    request = Mock()
    request.session = {"location_number": {"latitude": 123, "longitude": 456}}
    return request

@patch('your_module.get_location_name')
@patch('your_module.search_properties')
def test_show_property_location_wise(mock_search_properties, mock_get_location_name, mock_request):
    # Mock return values of get_location_name
    mock_get_location_name.return_value = {
        "city": "Mock City",
        "state": "Mock State",
        "country": "Mock Country"
    } 
    # Mock return value of search_properties 
    mock_search_properties.return_value = "Mock Property"

    # Call the function
    property_result, location_result = show_property_location_wise(mock_request)

    # Assert the results
    assert property_result == "Mock Property"
    assert location_result == "Mock City"  # City should be chosen first

