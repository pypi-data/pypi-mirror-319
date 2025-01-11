# ItemProductTypeByMarketplace

Product type associated with the Amazon catalog item for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | [optional] 
**product_type** | **str** | Name of the product type associated with the Amazon catalog item. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_product_type_by_marketplace import ItemProductTypeByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemProductTypeByMarketplace from a JSON string
item_product_type_by_marketplace_instance = ItemProductTypeByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemProductTypeByMarketplace.to_json())

# convert the object into a dict
item_product_type_by_marketplace_dict = item_product_type_by_marketplace_instance.to_dict()
# create an instance of ItemProductTypeByMarketplace from a dict
item_product_type_by_marketplace_from_dict = ItemProductTypeByMarketplace.from_dict(item_product_type_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


