# PackageDocumentDetail

The post-purchase details of a package that will be shipped using a shipping service.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_client_reference_id** | **str** | A client provided unique identifier for a package being shipped. This value should be saved by the client to pass as a parameter to the getShipmentDocuments operation. | 
**package_documents** | [**List[PackageDocument]**](PackageDocument.md) | A list of documents related to a package. | 
**tracking_id** | **str** | The carrier generated identifier for a package in a purchased shipment. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.package_document_detail import PackageDocumentDetail

# TODO update the JSON string below
json = "{}"
# create an instance of PackageDocumentDetail from a JSON string
package_document_detail_instance = PackageDocumentDetail.from_json(json)
# print the JSON string representation of the object
print(PackageDocumentDetail.to_json())

# convert the object into a dict
package_document_detail_dict = package_document_detail_instance.to_dict()
# create an instance of PackageDocumentDetail from a dict
package_document_detail_from_dict = PackageDocumentDetail.from_dict(package_document_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


