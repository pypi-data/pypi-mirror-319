# StandardFourImageTextQuadrantModule

Four standard images with text, presented on a grid of four quadrants.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**block1** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | 
**block2** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | 
**block3** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | 
**block4** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_four_image_text_quadrant_module import StandardFourImageTextQuadrantModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardFourImageTextQuadrantModule from a JSON string
standard_four_image_text_quadrant_module_instance = StandardFourImageTextQuadrantModule.from_json(json)
# print the JSON string representation of the object
print(StandardFourImageTextQuadrantModule.to_json())

# convert the object into a dict
standard_four_image_text_quadrant_module_dict = standard_four_image_text_quadrant_module_instance.to_dict()
# create an instance of StandardFourImageTextQuadrantModule from a dict
standard_four_image_text_quadrant_module_from_dict = StandardFourImageTextQuadrantModule.from_dict(standard_four_image_text_quadrant_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


