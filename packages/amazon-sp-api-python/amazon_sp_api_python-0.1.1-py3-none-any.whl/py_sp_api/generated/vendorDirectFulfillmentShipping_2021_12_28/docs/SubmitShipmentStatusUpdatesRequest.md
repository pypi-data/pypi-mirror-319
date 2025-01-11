# SubmitShipmentStatusUpdatesRequest

The request schema for the `submitShipmentStatusUpdates` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_status_updates** | [**List[ShipmentStatusUpdate]**](ShipmentStatusUpdate.md) | Contains a list of one or more &#x60;ShipmentStatusUpdate&#x60; objects. Each &#x60;ShipmentStatusUpdate&#x60; object represents an update to the status of a specific shipment. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.submit_shipment_status_updates_request import SubmitShipmentStatusUpdatesRequest

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


