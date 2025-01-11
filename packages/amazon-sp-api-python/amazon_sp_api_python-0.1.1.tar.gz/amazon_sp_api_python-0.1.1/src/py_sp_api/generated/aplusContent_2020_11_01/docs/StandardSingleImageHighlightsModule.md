# StandardSingleImageHighlightsModule

A standard image with several paragraphs and a bulleted list.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**image** | [**ImageComponent**](ImageComponent.md) |  | [optional] 
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**text_block1** | [**StandardTextBlock**](StandardTextBlock.md) |  | [optional] 
**text_block2** | [**StandardTextBlock**](StandardTextBlock.md) |  | [optional] 
**text_block3** | [**StandardTextBlock**](StandardTextBlock.md) |  | [optional] 
**bulleted_list_block** | [**StandardHeaderTextListBlock**](StandardHeaderTextListBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_single_image_highlights_module import StandardSingleImageHighlightsModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardSingleImageHighlightsModule from a JSON string
standard_single_image_highlights_module_instance = StandardSingleImageHighlightsModule.from_json(json)
# print the JSON string representation of the object
print(StandardSingleImageHighlightsModule.to_json())

# convert the object into a dict
standard_single_image_highlights_module_dict = standard_single_image_highlights_module_instance.to_dict()
# create an instance of StandardSingleImageHighlightsModule from a dict
standard_single_image_highlights_module_from_dict = StandardSingleImageHighlightsModule.from_dict(standard_single_image_highlights_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


