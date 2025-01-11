# GetShipmentDocumentsResult

The payload for the getShipmentDocuments operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The unique shipment identifier provided by a shipping service. | 
**package_document_detail** | [**PackageDocumentDetail**](PackageDocumentDetail.md) |  | 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_shipment_documents_result import GetShipmentDocumentsResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentDocumentsResult from a JSON string
get_shipment_documents_result_instance = GetShipmentDocumentsResult.from_json(json)
# print the JSON string representation of the object
print(GetShipmentDocumentsResult.to_json())

# convert the object into a dict
get_shipment_documents_result_dict = get_shipment_documents_result_instance.to_dict()
# create an instance of GetShipmentDocumentsResult from a dict
get_shipment_documents_result_from_dict = GetShipmentDocumentsResult.from_dict(get_shipment_documents_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


