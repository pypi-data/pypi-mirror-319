# SpdTrackingItemInput

Small Parcel Delivery (SPD) tracking items input information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**box_id** | **str** | The ID provided by Amazon that identifies a given box. This ID is comprised of the external shipment ID (which is generated after transportation has been confirmed) and the index of the box. | 
**tracking_id** | **str** | The tracking Id associated with each box in a non-Amazon partnered Small Parcel Delivery (SPD) shipment. The seller must provide this information. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.spd_tracking_item_input import SpdTrackingItemInput

# TODO update the JSON string below
json = "{}"
# create an instance of SpdTrackingItemInput from a JSON string
spd_tracking_item_input_instance = SpdTrackingItemInput.from_json(json)
# print the JSON string representation of the object
print(SpdTrackingItemInput.to_json())

# convert the object into a dict
spd_tracking_item_input_dict = spd_tracking_item_input_instance.to_dict()
# create an instance of SpdTrackingItemInput from a dict
spd_tracking_item_input_from_dict = SpdTrackingItemInput.from_dict(spd_tracking_item_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


