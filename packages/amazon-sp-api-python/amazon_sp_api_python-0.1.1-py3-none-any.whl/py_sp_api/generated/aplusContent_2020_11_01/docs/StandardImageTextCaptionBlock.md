# StandardImageTextCaptionBlock

The A+ Content standard image and text block, with a related caption. The caption may not display on all devices.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**block** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | [optional] 
**caption** | [**TextComponent**](TextComponent.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_image_text_caption_block import StandardImageTextCaptionBlock

# TODO update the JSON string below
json = "{}"
# create an instance of StandardImageTextCaptionBlock from a JSON string
standard_image_text_caption_block_instance = StandardImageTextCaptionBlock.from_json(json)
# print the JSON string representation of the object
print(StandardImageTextCaptionBlock.to_json())

# convert the object into a dict
standard_image_text_caption_block_dict = standard_image_text_caption_block_instance.to_dict()
# create an instance of StandardImageTextCaptionBlock from a dict
standard_image_text_caption_block_from_dict = StandardImageTextCaptionBlock.from_dict(standard_image_text_caption_block_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


