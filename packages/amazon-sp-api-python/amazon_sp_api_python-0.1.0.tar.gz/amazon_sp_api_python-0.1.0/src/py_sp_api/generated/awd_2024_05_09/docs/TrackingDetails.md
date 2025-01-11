# TrackingDetails

Tracking details for the shipment. If using SPD transportation, this can be for each case. If not using SPD transportation, this is a single tracking entry for the entire shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_code** | [**CarrierCode**](CarrierCode.md) |  | [optional] 
**ship_by** | **datetime** | Timestamp denoting when the shipment will be shipped Date should be in ISO 8601 format as defined by date-time. | 
**booking_id** | **str** | The identifier that is received from transportation to uniquely identify a booking. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.tracking_details import TrackingDetails

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


