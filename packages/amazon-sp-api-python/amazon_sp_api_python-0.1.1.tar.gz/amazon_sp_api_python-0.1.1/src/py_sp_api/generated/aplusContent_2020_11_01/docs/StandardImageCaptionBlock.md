# StandardImageCaptionBlock

The A+ Content standard image and caption block.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**image** | [**ImageComponent**](ImageComponent.md) |  | [optional] 
**caption** | [**TextComponent**](TextComponent.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_image_caption_block import StandardImageCaptionBlock

# TODO update the JSON string below
json = "{}"
# create an instance of StandardImageCaptionBlock from a JSON string
standard_image_caption_block_instance = StandardImageCaptionBlock.from_json(json)
# print the JSON string representation of the object
print(StandardImageCaptionBlock.to_json())

# convert the object into a dict
standard_image_caption_block_dict = standard_image_caption_block_instance.to_dict()
# create an instance of StandardImageCaptionBlock from a dict
standard_image_caption_block_from_dict = StandardImageCaptionBlock.from_dict(standard_image_caption_block_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


