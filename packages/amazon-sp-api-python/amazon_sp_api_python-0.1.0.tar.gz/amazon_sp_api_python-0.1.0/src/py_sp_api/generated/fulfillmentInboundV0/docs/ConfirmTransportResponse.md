# ConfirmTransportResponse

The response schema for the confirmTransport operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CommonTransportResult**](CommonTransportResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.confirm_transport_response import ConfirmTransportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmTransportResponse from a JSON string
confirm_transport_response_instance = ConfirmTransportResponse.from_json(json)
# print the JSON string representation of the object
print(ConfirmTransportResponse.to_json())

# convert the object into a dict
confirm_transport_response_dict = confirm_transport_response_instance.to_dict()
# create an instance of ConfirmTransportResponse from a dict
confirm_transport_response_from_dict = ConfirmTransportResponse.from_dict(confirm_transport_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


