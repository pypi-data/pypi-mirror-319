# StandardSingleImageSpecsDetailModule

A standard image with paragraphs and a bulleted list, and extra space for technical details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**image** | [**ImageComponent**](ImageComponent.md) |  | [optional] 
**description_headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**description_block1** | [**StandardTextBlock**](StandardTextBlock.md) |  | [optional] 
**description_block2** | [**StandardTextBlock**](StandardTextBlock.md) |  | [optional] 
**specification_headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**specification_list_block** | [**StandardHeaderTextListBlock**](StandardHeaderTextListBlock.md) |  | [optional] 
**specification_text_block** | [**StandardTextBlock**](StandardTextBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_single_image_specs_detail_module import StandardSingleImageSpecsDetailModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardSingleImageSpecsDetailModule from a JSON string
standard_single_image_specs_detail_module_instance = StandardSingleImageSpecsDetailModule.from_json(json)
# print the JSON string representation of the object
print(StandardSingleImageSpecsDetailModule.to_json())

# convert the object into a dict
standard_single_image_specs_detail_module_dict = standard_single_image_specs_detail_module_instance.to_dict()
# create an instance of StandardSingleImageSpecsDetailModule from a dict
standard_single_image_specs_detail_module_from_dict = StandardSingleImageSpecsDetailModule.from_dict(standard_single_image_specs_detail_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


