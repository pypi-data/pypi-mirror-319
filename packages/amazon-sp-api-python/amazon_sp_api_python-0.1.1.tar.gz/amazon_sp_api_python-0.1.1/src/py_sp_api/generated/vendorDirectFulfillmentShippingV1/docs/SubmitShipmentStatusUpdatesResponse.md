# SubmitShipmentStatusUpdatesResponse

The response schema for the submitShipmentStatusUpdates operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**TransactionReference**](TransactionReference.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.submit_shipment_status_updates_response import SubmitShipmentStatusUpdatesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitShipmentStatusUpdatesResponse from a JSON string
submit_shipment_status_updates_response_instance = SubmitShipmentStatusUpdatesResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitShipmentStatusUpdatesResponse.to_json())

# convert the object into a dict
submit_shipment_status_updates_response_dict = submit_shipment_status_updates_response_instance.to_dict()
# create an instance of SubmitShipmentStatusUpdatesResponse from a dict
submit_shipment_status_updates_response_from_dict = SubmitShipmentStatusUpdatesResponse.from_dict(submit_shipment_status_updates_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


