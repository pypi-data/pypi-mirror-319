# ImageComponent

A reference to an image, hosted in the A+ Content media library.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upload_destination_id** | **str** | This identifier is provided by the Selling Partner API for Uploads. | 
**image_crop_specification** | [**ImageCropSpecification**](ImageCropSpecification.md) |  | 
**alt_text** | **str** | The alternative text for the image. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.image_component import ImageComponent

# TODO update the JSON string below
json = "{}"
# create an instance of ImageComponent from a JSON string
image_component_instance = ImageComponent.from_json(json)
# print the JSON string representation of the object
print(ImageComponent.to_json())

# convert the object into a dict
image_component_dict = image_component_instance.to_dict()
# create an instance of ImageComponent from a dict
image_component_from_dict = ImageComponent.from_dict(image_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


