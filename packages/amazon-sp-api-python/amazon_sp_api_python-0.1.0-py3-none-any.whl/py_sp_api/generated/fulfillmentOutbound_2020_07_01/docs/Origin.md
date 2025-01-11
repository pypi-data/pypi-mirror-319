# Origin

The origin for the delivery offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**country_code** | **str** | The two digit country code the items should ship from. In ISO 3166-1 alpha-2 format. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.origin import Origin

# TODO update the JSON string below
json = "{}"
# create an instance of Origin from a JSON string
origin_instance = Origin.from_json(json)
# print the JSON string representation of the object
print(Origin.to_json())

# convert the object into a dict
origin_dict = origin_instance.to_dict()
# create an instance of Origin from a dict
origin_from_dict = Origin.from_dict(origin_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


