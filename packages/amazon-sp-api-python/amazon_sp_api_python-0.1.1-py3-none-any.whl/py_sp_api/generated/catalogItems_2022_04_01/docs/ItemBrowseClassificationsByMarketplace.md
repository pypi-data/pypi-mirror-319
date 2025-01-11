# ItemBrowseClassificationsByMarketplace

Classifications (browse nodes) associated with the item in the Amazon catalog for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**classifications** | [**List[ItemBrowseClassification]**](ItemBrowseClassification.md) | Classifications (browse nodes) associated with the item in the Amazon catalog for the indicated Amazon marketplace. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_browse_classifications_by_marketplace import ItemBrowseClassificationsByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemBrowseClassificationsByMarketplace from a JSON string
item_browse_classifications_by_marketplace_instance = ItemBrowseClassificationsByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemBrowseClassificationsByMarketplace.to_json())

# convert the object into a dict
item_browse_classifications_by_marketplace_dict = item_browse_classifications_by_marketplace_instance.to_dict()
# create an instance of ItemBrowseClassificationsByMarketplace from a dict
item_browse_classifications_by_marketplace_from_dict = ItemBrowseClassificationsByMarketplace.from_dict(item_browse_classifications_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


