# VoidTransportResponse

The response schema for the voidTransport operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CommonTransportResult**](CommonTransportResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.void_transport_response import VoidTransportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of VoidTransportResponse from a JSON string
void_transport_response_instance = VoidTransportResponse.from_json(json)
# print the JSON string representation of the object
print(VoidTransportResponse.to_json())

# convert the object into a dict
void_transport_response_dict = void_transport_response_instance.to_dict()
# create an instance of VoidTransportResponse from a dict
void_transport_response_from_dict = VoidTransportResponse.from_dict(void_transport_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


