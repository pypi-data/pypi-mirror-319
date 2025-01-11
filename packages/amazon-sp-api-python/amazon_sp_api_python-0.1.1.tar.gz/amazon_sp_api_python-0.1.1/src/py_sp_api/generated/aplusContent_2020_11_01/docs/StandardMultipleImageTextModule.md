# StandardMultipleImageTextModule

Standard images with text, presented one at a time. The user clicks on thumbnails to view each block.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**blocks** | [**List[StandardImageTextCaptionBlock]**](StandardImageTextCaptionBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_multiple_image_text_module import StandardMultipleImageTextModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardMultipleImageTextModule from a JSON string
standard_multiple_image_text_module_instance = StandardMultipleImageTextModule.from_json(json)
# print the JSON string representation of the object
print(StandardMultipleImageTextModule.to_json())

# convert the object into a dict
standard_multiple_image_text_module_dict = standard_multiple_image_text_module_instance.to_dict()
# create an instance of StandardMultipleImageTextModule from a dict
standard_multiple_image_text_module_from_dict = StandardMultipleImageTextModule.from_dict(standard_multiple_image_text_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


