# ItemImage

The image for the listings item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**link** | **str** | The link, or URL, to the image. | 
**height** | **int** | The height of the image in pixels. | 
**width** | **int** | The width of the image in pixels. | 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.item_image import ItemImage

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


