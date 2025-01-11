# ImageCropSpecification

The instructions for optionally cropping an image. If no cropping is desired, set the dimensions to the original image size. If the image is cropped and no offset values are provided, then the coordinates of the top left corner of the cropped image, relative to the original image, are defaulted to (0,0).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | [**ImageDimensions**](ImageDimensions.md) |  | 
**offset** | [**ImageOffsets**](ImageOffsets.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.image_crop_specification import ImageCropSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of ImageCropSpecification from a JSON string
image_crop_specification_instance = ImageCropSpecification.from_json(json)
# print the JSON string representation of the object
print(ImageCropSpecification.to_json())

# convert the object into a dict
image_crop_specification_dict = image_crop_specification_instance.to_dict()
# create an instance of ImageCropSpecification from a dict
image_crop_specification_from_dict = ImageCropSpecification.from_dict(image_crop_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


