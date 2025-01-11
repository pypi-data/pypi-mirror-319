# InboundShipmentResponse

The response schema for this operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**InboundShipmentResult**](InboundShipmentResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_response import InboundShipmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentResponse from a JSON string
inbound_shipment_response_instance = InboundShipmentResponse.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentResponse.to_json())

# convert the object into a dict
inbound_shipment_response_dict = inbound_shipment_response_instance.to_dict()
# create an instance of InboundShipmentResponse from a dict
inbound_shipment_response_from_dict = InboundShipmentResponse.from_dict(inbound_shipment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


