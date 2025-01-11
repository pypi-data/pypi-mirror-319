# UpdateShipmentTrackingDetailsRequest

The `updateShipmentTrackingDetails` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tracking_details** | [**TrackingDetailsInput**](TrackingDetailsInput.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.update_shipment_tracking_details_request import UpdateShipmentTrackingDetailsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateShipmentTrackingDetailsRequest from a JSON string
update_shipment_tracking_details_request_instance = UpdateShipmentTrackingDetailsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateShipmentTrackingDetailsRequest.to_json())

# convert the object into a dict
update_shipment_tracking_details_request_dict = update_shipment_tracking_details_request_instance.to_dict()
# create an instance of UpdateShipmentTrackingDetailsRequest from a dict
update_shipment_tracking_details_request_from_dict = UpdateShipmentTrackingDetailsRequest.from_dict(update_shipment_tracking_details_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


