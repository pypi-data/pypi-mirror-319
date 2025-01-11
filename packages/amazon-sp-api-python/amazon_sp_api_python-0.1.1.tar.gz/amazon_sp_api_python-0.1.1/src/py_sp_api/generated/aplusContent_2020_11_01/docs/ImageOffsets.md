# ImageOffsets

The top left corner of the cropped image, specified in the original image's coordinate space.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**x** | [**IntegerWithUnits**](IntegerWithUnits.md) |  | 
**y** | [**IntegerWithUnits**](IntegerWithUnits.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.image_offsets import ImageOffsets

# TODO update the JSON string below
json = "{}"
# create an instance of ImageOffsets from a JSON string
image_offsets_instance = ImageOffsets.from_json(json)
# print the JSON string representation of the object
print(ImageOffsets.to_json())

# convert the object into a dict
image_offsets_dict = image_offsets_instance.to_dict()
# create an instance of ImageOffsets from a dict
image_offsets_from_dict = ImageOffsets.from_dict(image_offsets_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


