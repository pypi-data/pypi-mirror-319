# DocumentSize

The size dimensions of the label.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**width** | **float** | The width of the document measured in the units specified. | 
**length** | **float** | The length of the document measured in the units specified. | 
**unit** | **str** | The unit of measurement. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.document_size import DocumentSize

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentSize from a JSON string
document_size_instance = DocumentSize.from_json(json)
# print the JSON string representation of the object
print(DocumentSize.to_json())

# convert the object into a dict
document_size_dict = document_size_instance.to_dict()
# create an instance of DocumentSize from a dict
document_size_from_dict = DocumentSize.from_dict(document_size_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


