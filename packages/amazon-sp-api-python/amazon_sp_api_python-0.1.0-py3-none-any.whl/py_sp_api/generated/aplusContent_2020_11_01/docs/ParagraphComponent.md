# ParagraphComponent

A list of rich text content, usually presented in a text box.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text_list** | [**List[TextComponent]**](TextComponent.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.paragraph_component import ParagraphComponent

# TODO update the JSON string below
json = "{}"
# create an instance of ParagraphComponent from a JSON string
paragraph_component_instance = ParagraphComponent.from_json(json)
# print the JSON string representation of the object
print(ParagraphComponent.to_json())

# convert the object into a dict
paragraph_component_dict = paragraph_component_instance.to_dict()
# create an instance of ParagraphComponent from a dict
paragraph_component_from_dict = ParagraphComponent.from_dict(paragraph_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


