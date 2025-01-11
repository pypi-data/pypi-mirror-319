# SpdTrackingDetailInput

Contains input information to update Small Parcel Delivery (SPD) tracking information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**spd_tracking_items** | [**List[SpdTrackingItemInput]**](SpdTrackingItemInput.md) | List of Small Parcel Delivery (SPD) tracking items input. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.spd_tracking_detail_input import SpdTrackingDetailInput

# TODO update the JSON string below
json = "{}"
# create an instance of SpdTrackingDetailInput from a JSON string
spd_tracking_detail_input_instance = SpdTrackingDetailInput.from_json(json)
# print the JSON string representation of the object
print(SpdTrackingDetailInput.to_json())

# convert the object into a dict
spd_tracking_detail_input_dict = spd_tracking_detail_input_instance.to_dict()
# create an instance of SpdTrackingDetailInput from a dict
spd_tracking_detail_input_from_dict = SpdTrackingDetailInput.from_dict(spd_tracking_detail_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


