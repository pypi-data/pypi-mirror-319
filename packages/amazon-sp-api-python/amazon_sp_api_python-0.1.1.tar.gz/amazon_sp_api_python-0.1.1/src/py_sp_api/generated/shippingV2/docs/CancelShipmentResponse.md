# CancelShipmentResponse

Response schema for the cancelShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | **Dict[str, object]** | The payload for the cancelShipment operation. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.cancel_shipment_response import CancelShipmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CancelShipmentResponse from a JSON string
cancel_shipment_response_instance = CancelShipmentResponse.from_json(json)
# print the JSON string representation of the object
print(CancelShipmentResponse.to_json())

# convert the object into a dict
cancel_shipment_response_dict = cancel_shipment_response_instance.to_dict()
# create an instance of CancelShipmentResponse from a dict
cancel_shipment_response_from_dict = CancelShipmentResponse.from_dict(cancel_shipment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


