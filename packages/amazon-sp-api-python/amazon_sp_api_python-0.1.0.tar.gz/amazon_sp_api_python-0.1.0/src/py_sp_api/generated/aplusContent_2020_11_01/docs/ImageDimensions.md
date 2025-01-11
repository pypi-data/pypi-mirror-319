# ImageDimensions

The dimensions extending from the top left corner of the cropped image, or the top left corner of the original image if there is no cropping. Only `pixels` is allowed as the units value for ImageDimensions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**width** | [**IntegerWithUnits**](IntegerWithUnits.md) |  | 
**height** | [**IntegerWithUnits**](IntegerWithUnits.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.image_dimensions import ImageDimensions

# TODO update the JSON string below
json = "{}"
# create an instance of ImageDimensions from a JSON string
image_dimensions_instance = ImageDimensions.from_json(json)
# print the JSON string representation of the object
print(ImageDimensions.to_json())

# convert the object into a dict
image_dimensions_dict = image_dimensions_instance.to_dict()
# create an instance of ImageDimensions from a dict
image_dimensions_from_dict = ImageDimensions.from_dict(image_dimensions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


