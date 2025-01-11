# SpdTrackingDetail

Contains information related to Small Parcel Delivery (SPD) shipment tracking.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**spd_tracking_items** | [**List[SpdTrackingItem]**](SpdTrackingItem.md) | List of Small Parcel Delivery (SPD) tracking items. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.spd_tracking_detail import SpdTrackingDetail

# TODO update the JSON string below
json = "{}"
# create an instance of SpdTrackingDetail from a JSON string
spd_tracking_detail_instance = SpdTrackingDetail.from_json(json)
# print the JSON string representation of the object
print(SpdTrackingDetail.to_json())

# convert the object into a dict
spd_tracking_detail_dict = spd_tracking_detail_instance.to_dict()
# create an instance of SpdTrackingDetail from a dict
spd_tracking_detail_from_dict = SpdTrackingDetail.from_dict(spd_tracking_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


