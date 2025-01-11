# SubmitShipmentStatusUpdatesRequest

Represents the request payload for submitting updates to the status of shipments, containing an array of one or more ShipmentStatusUpdate objects.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_status_updates** | [**List[ShipmentStatusUpdate]**](ShipmentStatusUpdate.md) | Contains a list of one or more ShipmentStatusUpdate objects, each representing an update to the status of a specific shipment. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.submit_shipment_status_updates_request import SubmitShipmentStatusUpdatesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitShipmentStatusUpdatesRequest from a JSON string
submit_shipment_status_updates_request_instance = SubmitShipmentStatusUpdatesRequest.from_json(json)
# print the JSON string representation of the object
print(SubmitShipmentStatusUpdatesRequest.to_json())

# convert the object into a dict
submit_shipment_status_updates_request_dict = submit_shipment_status_updates_request_instance.to_dict()
# create an instance of SubmitShipmentStatusUpdatesRequest from a dict
submit_shipment_status_updates_request_from_dict = SubmitShipmentStatusUpdatesRequest.from_dict(submit_shipment_status_updates_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


