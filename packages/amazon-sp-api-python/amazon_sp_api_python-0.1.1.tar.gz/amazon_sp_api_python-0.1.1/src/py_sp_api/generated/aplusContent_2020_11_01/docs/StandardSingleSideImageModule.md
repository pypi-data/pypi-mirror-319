# StandardSingleSideImageModule

A standard headline and body text with an image on the side.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**image_position_type** | [**PositionType**](PositionType.md) |  | 
**block** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_single_side_image_module import StandardSingleSideImageModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardSingleSideImageModule from a JSON string
standard_single_side_image_module_instance = StandardSingleSideImageModule.from_json(json)
# print the JSON string representation of the object
print(StandardSingleSideImageModule.to_json())

# convert the object into a dict
standard_single_side_image_module_dict = standard_single_side_image_module_instance.to_dict()
# create an instance of StandardSingleSideImageModule from a dict
standard_single_side_image_module_from_dict = StandardSingleSideImageModule.from_dict(standard_single_side_image_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


