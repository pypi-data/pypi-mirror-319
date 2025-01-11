# UpdateShipmentStatusErrorResponse

The error response schema for the `UpdateShipmentStatus` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.update_shipment_status_error_response import UpdateShipmentStatusErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateShipmentStatusErrorResponse from a JSON string
update_shipment_status_error_response_instance = UpdateShipmentStatusErrorResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateShipmentStatusErrorResponse.to_json())

# convert the object into a dict
update_shipment_status_error_response_dict = update_shipment_status_error_response_instance.to_dict()
# create an instance of UpdateShipmentStatusErrorResponse from a dict
update_shipment_status_error_response_from_dict = UpdateShipmentStatusErrorResponse.from_dict(update_shipment_status_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


