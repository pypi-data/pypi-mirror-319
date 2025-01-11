# TrackingDetailsInput

Tracking information input for Less-Than-Truckload (LTL) and Small Parcel Delivery (SPD) shipments.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ltl_tracking_detail** | [**LtlTrackingDetailInput**](LtlTrackingDetailInput.md) |  | [optional] 
**spd_tracking_detail** | [**SpdTrackingDetailInput**](SpdTrackingDetailInput.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.tracking_details_input import TrackingDetailsInput

# TODO update the JSON string below
json = "{}"
# create an instance of TrackingDetailsInput from a JSON string
tracking_details_input_instance = TrackingDetailsInput.from_json(json)
# print the JSON string representation of the object
print(TrackingDetailsInput.to_json())

# convert the object into a dict
tracking_details_input_dict = tracking_details_input_instance.to_dict()
# create an instance of TrackingDetailsInput from a dict
tracking_details_input_from_dict = TrackingDetailsInput.from_dict(tracking_details_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


