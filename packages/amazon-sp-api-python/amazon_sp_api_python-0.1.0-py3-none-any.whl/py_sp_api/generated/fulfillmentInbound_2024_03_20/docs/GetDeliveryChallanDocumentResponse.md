# GetDeliveryChallanDocumentResponse

The `getDeliveryChallanDocumentResponse` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_download** | [**DocumentDownload**](DocumentDownload.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.get_delivery_challan_document_response import GetDeliveryChallanDocumentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeliveryChallanDocumentResponse from a JSON string
get_delivery_challan_document_response_instance = GetDeliveryChallanDocumentResponse.from_json(json)
# print the JSON string representation of the object
print(GetDeliveryChallanDocumentResponse.to_json())

# convert the object into a dict
get_delivery_challan_document_response_dict = get_delivery_challan_document_response_instance.to_dict()
# create an instance of GetDeliveryChallanDocumentResponse from a dict
get_delivery_challan_document_response_from_dict = GetDeliveryChallanDocumentResponse.from_dict(get_delivery_challan_document_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


