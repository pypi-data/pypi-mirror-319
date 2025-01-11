# TrackingDetails

Tracking information for Less-Than-Truckload (LTL) and Small Parcel Delivery (SPD) shipments.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ltl_tracking_detail** | [**LtlTrackingDetail**](LtlTrackingDetail.md) |  | [optional] 
**spd_tracking_detail** | [**SpdTrackingDetail**](SpdTrackingDetail.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.tracking_details import TrackingDetails

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


