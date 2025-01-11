# TextItem

Rich positional text, usually presented as a collection of bullet points.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | **int** | The rank or index of this text item within the collection. Different items cannot occupy the same position within a single collection. | 
**text** | [**TextComponent**](TextComponent.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.text_item import TextItem

# TODO update the JSON string below
json = "{}"
# create an instance of TextItem from a JSON string
text_item_instance = TextItem.from_json(json)
# print the JSON string representation of the object
print(TextItem.to_json())

# convert the object into a dict
text_item_dict = text_item_instance.to_dict()
# create an instance of TextItem from a dict
text_item_from_dict = TextItem.from_dict(text_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


