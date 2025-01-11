# UpdateShipmentTrackingDetailsResponse

The `updateShipmentTrackingDetails` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.update_shipment_tracking_details_response import UpdateShipmentTrackingDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateShipmentTrackingDetailsResponse from a JSON string
update_shipment_tracking_details_response_instance = UpdateShipmentTrackingDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateShipmentTrackingDetailsResponse.to_json())

# convert the object into a dict
update_shipment_tracking_details_response_dict = update_shipment_tracking_details_response_instance.to_dict()
# create an instance of UpdateShipmentTrackingDetailsResponse from a dict
update_shipment_tracking_details_response_from_dict = UpdateShipmentTrackingDetailsResponse.from_dict(update_shipment_tracking_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


