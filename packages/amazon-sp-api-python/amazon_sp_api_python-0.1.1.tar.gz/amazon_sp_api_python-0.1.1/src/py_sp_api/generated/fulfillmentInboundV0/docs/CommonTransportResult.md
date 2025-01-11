# CommonTransportResult

Common container for transport result

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_result** | [**TransportResult**](TransportResult.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.common_transport_result import CommonTransportResult

# TODO update the JSON string below
json = "{}"
# create an instance of CommonTransportResult from a JSON string
common_transport_result_instance = CommonTransportResult.from_json(json)
# print the JSON string representation of the object
print(CommonTransportResult.to_json())

# convert the object into a dict
common_transport_result_dict = common_transport_result_instance.to_dict()
# create an instance of CommonTransportResult from a dict
common_transport_result_from_dict = CommonTransportResult.from_dict(common_transport_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


