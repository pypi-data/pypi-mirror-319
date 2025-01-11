# ItemImagesByMarketplace

Images for an item in the Amazon catalog for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**images** | [**List[ItemImage]**](ItemImage.md) | Images for an item in the Amazon catalog for the indicated Amazon marketplace. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_images_by_marketplace import ItemImagesByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemImagesByMarketplace from a JSON string
item_images_by_marketplace_instance = ItemImagesByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemImagesByMarketplace.to_json())

# convert the object into a dict
item_images_by_marketplace_dict = item_images_by_marketplace_instance.to_dict()
# create an instance of ItemImagesByMarketplace from a dict
item_images_by_marketplace_from_dict = ItemImagesByMarketplace.from_dict(item_images_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


