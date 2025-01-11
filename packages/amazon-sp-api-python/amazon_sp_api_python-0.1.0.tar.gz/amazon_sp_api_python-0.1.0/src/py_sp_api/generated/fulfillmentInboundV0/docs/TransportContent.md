# TransportContent

Inbound shipment information, including carrier details, shipment status, and the workflow status for a request for shipment with an Amazon-partnered carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_header** | [**TransportHeader**](TransportHeader.md) |  | 
**transport_details** | [**TransportDetailOutput**](TransportDetailOutput.md) |  | 
**transport_result** | [**TransportResult**](TransportResult.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.transport_content import TransportContent

# TODO update the JSON string below
json = "{}"
# create an instance of TransportContent from a JSON string
transport_content_instance = TransportContent.from_json(json)
# print the JSON string representation of the object
print(TransportContent.to_json())

# convert the object into a dict
transport_content_dict = transport_content_instance.to_dict()
# create an instance of TransportContent from a dict
transport_content_from_dict = TransportContent.from_dict(transport_content_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


