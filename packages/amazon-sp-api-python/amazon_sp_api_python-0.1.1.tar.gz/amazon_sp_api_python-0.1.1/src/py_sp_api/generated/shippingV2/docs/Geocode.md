# Geocode

Defines the latitude and longitude of the access point.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**latitude** | **str** | The latitude of access point. | [optional] 
**longitude** | **str** | The longitude of access point. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.geocode import Geocode

# TODO update the JSON string below
json = "{}"
# create an instance of Geocode from a JSON string
geocode_instance = Geocode.from_json(json)
# print the JSON string representation of the object
print(Geocode.to_json())

# convert the object into a dict
geocode_dict = geocode_instance.to_dict()
# create an instance of Geocode from a dict
geocode_from_dict = Geocode.from_dict(geocode_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


