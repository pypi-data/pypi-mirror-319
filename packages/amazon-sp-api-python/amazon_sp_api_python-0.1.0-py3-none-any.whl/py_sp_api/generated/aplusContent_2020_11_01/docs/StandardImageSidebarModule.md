# StandardImageSidebarModule

Two images, two paragraphs, and two bulleted lists. One image is smaller and displayed in the sidebar.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**image_caption_block** | [**StandardImageCaptionBlock**](StandardImageCaptionBlock.md) |  | [optional] 
**description_text_block** | [**StandardTextBlock**](StandardTextBlock.md) |  | [optional] 
**description_list_block** | [**StandardTextListBlock**](StandardTextListBlock.md) |  | [optional] 
**sidebar_image_text_block** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | [optional] 
**sidebar_list_block** | [**StandardTextListBlock**](StandardTextListBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_image_sidebar_module import StandardImageSidebarModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardImageSidebarModule from a JSON string
standard_image_sidebar_module_instance = StandardImageSidebarModule.from_json(json)
# print the JSON string representation of the object
print(StandardImageSidebarModule.to_json())

# convert the object into a dict
standard_image_sidebar_module_dict = standard_image_sidebar_module_instance.to_dict()
# create an instance of StandardImageSidebarModule from a dict
standard_image_sidebar_module_from_dict = StandardImageSidebarModule.from_dict(standard_image_sidebar_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


