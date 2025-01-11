# PlainTextItem

Plain positional text, used in collections of brief labels and descriptors.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | **int** | The rank or index of this text item within the collection. Different items cannot occupy the same position within a single collection. | 
**value** | **str** | The actual plain text. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.plain_text_item import PlainTextItem

# TODO update the JSON string below
json = "{}"
# create an instance of PlainTextItem from a JSON string
plain_text_item_instance = PlainTextItem.from_json(json)
# print the JSON string representation of the object
print(PlainTextItem.to_json())

# convert the object into a dict
plain_text_item_dict = plain_text_item_instance.to_dict()
# create an instance of PlainTextItem from a dict
plain_text_item_from_dict = PlainTextItem.from_dict(plain_text_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


