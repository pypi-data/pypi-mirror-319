# TrackingDetails

Representation of tracking metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tracking_id** | **str** | A string of up to 255 characters. | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.tracking_details import TrackingDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TrackingDetails from a JSON string
tracking_details_instance = TrackingDetails.from_json(json)
# print the JSON string representation of the object
print(TrackingDetails.to_json())

# convert the object into a dict
tracking_details_dict = tracking_details_instance.to_dict()
# create an instance of TrackingDetails from a dict
tracking_details_from_dict = TrackingDetails.from_dict(tracking_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


