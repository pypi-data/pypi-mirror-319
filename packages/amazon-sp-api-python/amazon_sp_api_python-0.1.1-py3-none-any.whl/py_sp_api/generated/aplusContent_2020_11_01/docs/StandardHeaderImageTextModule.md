# StandardHeaderImageTextModule

Standard headline text, an image, and body text.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**block** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_header_image_text_module import StandardHeaderImageTextModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardHeaderImageTextModule from a JSON string
standard_header_image_text_module_instance = StandardHeaderImageTextModule.from_json(json)
# print the JSON string representation of the object
print(StandardHeaderImageTextModule.to_json())

# convert the object into a dict
standard_header_image_text_module_dict = standard_header_image_text_module_instance.to_dict()
# create an instance of StandardHeaderImageTextModule from a dict
standard_header_image_text_module_from_dict = StandardHeaderImageTextModule.from_dict(standard_header_image_text_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


