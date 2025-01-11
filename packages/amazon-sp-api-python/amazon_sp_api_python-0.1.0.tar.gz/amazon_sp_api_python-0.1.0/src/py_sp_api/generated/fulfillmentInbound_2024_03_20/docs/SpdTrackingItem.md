# SpdTrackingItem

Contains information used to track and identify a Small Parcel Delivery (SPD) item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**box_id** | **str** | The ID provided by Amazon that identifies a given box. This ID is comprised of the external shipment ID (which is generated after transportation has been confirmed) and the index of the box. | [optional] 
**tracking_id** | **str** | The tracking ID associated with each box in a non-Amazon partnered Small Parcel Delivery (SPD) shipment. | [optional] 
**tracking_number_validation_status** | **str** | Whether or not Amazon has validated the tracking number. If more than 24 hours have passed and the status is not yet &#39;VALIDATED&#39;, please verify the number and update if necessary. Possible values: &#x60;VALIDATED&#x60;, &#x60;NOT_VALIDATED&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.spd_tracking_item import SpdTrackingItem

# TODO update the JSON string below
json = "{}"
# create an instance of SpdTrackingItem from a JSON string
spd_tracking_item_instance = SpdTrackingItem.from_json(json)
# print the JSON string representation of the object
print(SpdTrackingItem.to_json())

# convert the object into a dict
spd_tracking_item_dict = spd_tracking_item_instance.to_dict()
# create an instance of SpdTrackingItem from a dict
spd_tracking_item_from_dict = SpdTrackingItem.from_dict(spd_tracking_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


