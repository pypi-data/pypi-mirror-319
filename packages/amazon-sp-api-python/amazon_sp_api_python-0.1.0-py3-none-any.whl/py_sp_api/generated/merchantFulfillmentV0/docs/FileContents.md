# FileContents

The document data and checksum.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contents** | **str** | Data for printing labels encoded into a Base64, GZip-compressed string. | 
**file_type** | [**FileType**](FileType.md) |  | 
**checksum** | **str** | An MD5 hash to validate the PDF document data, in the form of a Base64 string. | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.file_contents import FileContents

# TODO update the JSON string below
json = "{}"
# create an instance of FileContents from a JSON string
file_contents_instance = FileContents.from_json(json)
# print the JSON string representation of the object
print(FileContents.to_json())

# convert the object into a dict
file_contents_dict = file_contents_instance.to_dict()
# create an instance of FileContents from a dict
file_contents_from_dict = FileContents.from_dict(file_contents_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


