# GetTransportDetailsResult

Result for the get transport details operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_content** | [**TransportContent**](TransportContent.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_transport_details_result import GetTransportDetailsResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetTransportDetailsResult from a JSON string
get_transport_details_result_instance = GetTransportDetailsResult.from_json(json)
# print the JSON string representation of the object
print(GetTransportDetailsResult.to_json())

# convert the object into a dict
get_transport_details_result_dict = get_transport_details_result_instance.to_dict()
# create an instance of GetTransportDetailsResult from a dict
get_transport_details_result_from_dict = GetTransportDetailsResult.from_dict(get_transport_details_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


