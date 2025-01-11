# GetShipmentDocumentsResponse

The response schema for the the getShipmentDocuments operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetShipmentDocumentsResult**](GetShipmentDocumentsResult.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_shipment_documents_response import GetShipmentDocumentsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentDocumentsResponse from a JSON string
get_shipment_documents_response_instance = GetShipmentDocumentsResponse.from_json(json)
# print the JSON string representation of the object
print(GetShipmentDocumentsResponse.to_json())

# convert the object into a dict
get_shipment_documents_response_dict = get_shipment_documents_response_instance.to_dict()
# create an instance of GetShipmentDocumentsResponse from a dict
get_shipment_documents_response_from_dict = GetShipmentDocumentsResponse.from_dict(get_shipment_documents_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


