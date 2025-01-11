# PackageDocument

A document related to a package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**DocumentType**](DocumentType.md) |  | 
**format** | [**DocumentFormat**](DocumentFormat.md) |  | 
**contents** | **str** | A Base64 encoded string of the file contents. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.package_document import PackageDocument

# TODO update the JSON string below
json = "{}"
# create an instance of PackageDocument from a JSON string
package_document_instance = PackageDocument.from_json(json)
# print the JSON string representation of the object
print(PackageDocument.to_json())

# convert the object into a dict
package_document_dict = package_document_instance.to_dict()
# create an instance of PackageDocument from a dict
package_document_from_dict = PackageDocument.from_dict(package_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


