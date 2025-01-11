# GetTransportDetailsResponse

The response schema for the getTransportDetails operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetTransportDetailsResult**](GetTransportDetailsResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_transport_details_response import GetTransportDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetTransportDetailsResponse from a JSON string
get_transport_details_response_instance = GetTransportDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(GetTransportDetailsResponse.to_json())

# convert the object into a dict
get_transport_details_response_dict = get_transport_details_response_instance.to_dict()
# create an instance of GetTransportDetailsResponse from a dict
get_transport_details_response_from_dict = GetTransportDetailsResponse.from_dict(get_transport_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


