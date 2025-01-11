# TextComponent

Rich text content.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The actual plain text. | 
**decorator_set** | [**List[Decorator]**](Decorator.md) | A set of content decorators. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.text_component import TextComponent

# TODO update the JSON string below
json = "{}"
# create an instance of TextComponent from a JSON string
text_component_instance = TextComponent.from_json(json)
# print the JSON string representation of the object
print(TextComponent.to_json())

# convert the object into a dict
text_component_dict = text_component_instance.to_dict()
# create an instance of TextComponent from a dict
text_component_from_dict = TextComponent.from_dict(text_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


