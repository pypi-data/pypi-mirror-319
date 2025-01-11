# ItemIdentifier

Identifier associated with the item in the Amazon catalog, such as a UPC or EAN identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier_type** | **str** | Type of identifier, such as UPC, EAN, or ISBN. | 
**identifier** | **str** | Identifier. | 

## Example

```python
from py_sp_api.generated.catalogItems_2020_12_01.models.item_identifier import ItemIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ItemIdentifier from a JSON string
item_identifier_instance = ItemIdentifier.from_json(json)
# print the JSON string representation of the object
print(ItemIdentifier.to_json())

# convert the object into a dict
item_identifier_dict = item_identifier_instance.to_dict()
# create an instance of ItemIdentifier from a dict
item_identifier_from_dict = ItemIdentifier.from_dict(item_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


