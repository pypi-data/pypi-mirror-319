# StandardImageTextBlock

The A+ Content standard image and text box block.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**image** | [**ImageComponent**](ImageComponent.md) |  | [optional] 
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**body** | [**ParagraphComponent**](ParagraphComponent.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_image_text_block import StandardImageTextBlock

# TODO update the JSON string below
json = "{}"
# create an instance of StandardImageTextBlock from a JSON string
standard_image_text_block_instance = StandardImageTextBlock.from_json(json)
# print the JSON string representation of the object
print(StandardImageTextBlock.to_json())

# convert the object into a dict
standard_image_text_block_dict = standard_image_text_block_instance.to_dict()
# create an instance of StandardImageTextBlock from a dict
standard_image_text_block_from_dict = StandardImageTextBlock.from_dict(standard_image_text_block_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


