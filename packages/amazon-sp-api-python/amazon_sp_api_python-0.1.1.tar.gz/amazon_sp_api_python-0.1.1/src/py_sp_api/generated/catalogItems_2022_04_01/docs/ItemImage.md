# ItemImage

Image for an item in the Amazon catalog.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**variant** | **str** | Variant of the image, such as &#x60;MAIN&#x60; or &#x60;PT01&#x60;. | 
**link** | **str** | Link, or URL, for the image. | 
**height** | **int** | Height of the image in pixels. | 
**width** | **int** | Width of the image in pixels. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_image import ItemImage

# TODO update the JSON string below
json = "{}"
# create an instance of ItemImage from a JSON string
item_image_instance = ItemImage.from_json(json)
# print the JSON string representation of the object
print(ItemImage.to_json())

# convert the object into a dict
item_image_dict = item_image_instance.to_dict()
# create an instance of ItemImage from a dict
item_image_from_dict = ItemImage.from_dict(item_image_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


