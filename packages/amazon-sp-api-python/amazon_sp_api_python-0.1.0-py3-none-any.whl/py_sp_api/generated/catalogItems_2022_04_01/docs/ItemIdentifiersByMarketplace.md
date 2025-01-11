# ItemIdentifiersByMarketplace

Identifiers associated with the item in the Amazon catalog for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**identifiers** | [**List[ItemIdentifier]**](ItemIdentifier.md) | Identifiers associated with the item in the Amazon catalog for the indicated Amazon marketplace. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_identifiers_by_marketplace import ItemIdentifiersByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemIdentifiersByMarketplace from a JSON string
item_identifiers_by_marketplace_instance = ItemIdentifiersByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemIdentifiersByMarketplace.to_json())

# convert the object into a dict
item_identifiers_by_marketplace_dict = item_identifiers_by_marketplace_instance.to_dict()
# create an instance of ItemIdentifiersByMarketplace from a dict
item_identifiers_by_marketplace_from_dict = ItemIdentifiersByMarketplace.from_dict(item_identifiers_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


