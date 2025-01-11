# ItemRelatedIdentifier

Related business identifiers of the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_related_identifier_name** | **str** | Enumerated set of related item identifier names for the item. | [optional] 
**item_related_identifier_value** | **str** | Corresponding value to &#x60;ItemRelatedIdentifierName&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.item_related_identifier import ItemRelatedIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ItemRelatedIdentifier from a JSON string
item_related_identifier_instance = ItemRelatedIdentifier.from_json(json)
# print the JSON string representation of the object
print(ItemRelatedIdentifier.to_json())

# convert the object into a dict
item_related_identifier_dict = item_related_identifier_instance.to_dict()
# create an instance of ItemRelatedIdentifier from a dict
item_related_identifier_from_dict = ItemRelatedIdentifier.from_dict(item_related_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


