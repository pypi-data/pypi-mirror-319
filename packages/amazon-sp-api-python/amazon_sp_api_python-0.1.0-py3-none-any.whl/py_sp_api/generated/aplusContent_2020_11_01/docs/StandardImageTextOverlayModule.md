# StandardImageTextOverlayModule

A standard background image with a floating text box.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**overlay_color_type** | [**ColorType**](ColorType.md) |  | 
**block** | [**StandardImageTextBlock**](StandardImageTextBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_image_text_overlay_module import StandardImageTextOverlayModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardImageTextOverlayModule from a JSON string
standard_image_text_overlay_module_instance = StandardImageTextOverlayModule.from_json(json)
# print the JSON string representation of the object
print(StandardImageTextOverlayModule.to_json())

# convert the object into a dict
standard_image_text_overlay_module_dict = standard_image_text_overlay_module_instance.to_dict()
# create an instance of StandardImageTextOverlayModule from a dict
standard_image_text_overlay_module_from_dict = StandardImageTextOverlayModule.from_dict(standard_image_text_overlay_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


