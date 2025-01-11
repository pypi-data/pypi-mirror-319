# StandardThreeImageTextModule

Three standard images with text, presented across a single row.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**block1** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | [optional] 
**block2** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | [optional] 
**block3** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_three_image_text_module import StandardThreeImageTextModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardThreeImageTextModule from a JSON string
standard_three_image_text_module_instance = StandardThreeImageTextModule.from_json(json)
# print the JSON string representation of the object
print(StandardThreeImageTextModule.to_json())

# convert the object into a dict
standard_three_image_text_module_dict = standard_three_image_text_module_instance.to_dict()
# create an instance of StandardThreeImageTextModule from a dict
standard_three_image_text_module_from_dict = StandardThreeImageTextModule.from_dict(standard_three_image_text_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


