# TrackingAddress

Address information for tracking the package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**city** | **str** | The city. | 
**state** | **str** | The state. | 
**country** | **str** | The country. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.tracking_address import TrackingAddress

# TODO update the JSON string below
json = "{}"
# create an instance of TrackingAddress from a JSON string
tracking_address_instance = TrackingAddress.from_json(json)
# print the JSON string representation of the object
print(TrackingAddress.to_json())

# convert the object into a dict
tracking_address_dict = tracking_address_instance.to_dict()
# create an instance of TrackingAddress from a dict
tracking_address_from_dict = TrackingAddress.from_dict(tracking_address_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


