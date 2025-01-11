# Location

The location where the person, business or institution is located.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state_or_region** | **str** | The state, county or region where the person, business or institution is located. | [optional] 
**city** | **str** | The city or town where the person, business or institution is located. | [optional] 
**country_code** | **str** | The two digit country code. Follows ISO 3166-1 alpha-2 format. | [optional] 
**postal_code** | **str** | The postal code of that address. It contains a series of letters or digits or both, sometimes including spaces or punctuation. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.location import Location

# TODO update the JSON string below
json = "{}"
# create an instance of Location from a JSON string
location_instance = Location.from_json(json)
# print the JSON string representation of the object
print(Location.to_json())

# convert the object into a dict
location_dict = location_instance.to_dict()
# create an instance of Location from a dict
location_from_dict = Location.from_dict(location_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


