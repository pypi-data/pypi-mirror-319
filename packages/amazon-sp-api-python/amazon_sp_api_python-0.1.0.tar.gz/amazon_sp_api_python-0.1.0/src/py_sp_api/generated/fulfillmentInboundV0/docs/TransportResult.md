# TransportResult

The workflow status for a shipment with an Amazon-partnered carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_status** | [**TransportStatus**](TransportStatus.md) |  | 
**error_code** | **str** | An error code that identifies the type of error that occured. | [optional] 
**error_description** | **str** | A message that describes the error condition. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.transport_result import TransportResult

# TODO update the JSON string below
json = "{}"
# create an instance of TransportResult from a JSON string
transport_result_instance = TransportResult.from_json(json)
# print the JSON string representation of the object
print(TransportResult.to_json())

# convert the object into a dict
transport_result_dict = transport_result_instance.to_dict()
# create an instance of TransportResult from a dict
transport_result_from_dict = TransportResult.from_dict(transport_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


