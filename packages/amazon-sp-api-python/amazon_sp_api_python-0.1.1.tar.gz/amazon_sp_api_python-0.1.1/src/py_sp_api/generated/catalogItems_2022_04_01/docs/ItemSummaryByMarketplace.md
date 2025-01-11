# ItemSummaryByMarketplace

Summary details of an Amazon catalog item for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**adult_product** | **bool** | Identifies an Amazon catalog item is intended for an adult audience or is sexual in nature. | [optional] 
**autographed** | **bool** | Identifies an Amazon catalog item is autographed by a player or celebrity. | [optional] 
**brand** | **str** | Name of the brand associated with an Amazon catalog item. | [optional] 
**browse_classification** | [**ItemBrowseClassification**](ItemBrowseClassification.md) |  | [optional] 
**color** | **str** | Name of the color associated with an Amazon catalog item. | [optional] 
**contributors** | [**List[ItemContributor]**](ItemContributor.md) | Individual contributors to the creation of an item, such as the authors or actors. | [optional] 
**item_classification** | **str** | Classification type associated with the Amazon catalog item. | [optional] 
**item_name** | **str** | Name, or title, associated with an Amazon catalog item. | [optional] 
**manufacturer** | **str** | Name of the manufacturer associated with an Amazon catalog item. | [optional] 
**memorabilia** | **bool** | Identifies an Amazon catalog item is memorabilia valued for its connection with historical events, culture, or entertainment. | [optional] 
**model_number** | **str** | Model number associated with an Amazon catalog item. | [optional] 
**package_quantity** | **int** | Quantity of an Amazon catalog item in one package. | [optional] 
**part_number** | **str** | Part number associated with an Amazon catalog item. | [optional] 
**release_date** | **date** | First date on which an Amazon catalog item is shippable to customers. | [optional] 
**size** | **str** | Name of the size associated with an Amazon catalog item. | [optional] 
**style** | **str** | Name of the style associated with an Amazon catalog item. | [optional] 
**trade_in_eligible** | **bool** | Identifies an Amazon catalog item is eligible for trade-in. | [optional] 
**website_display_group** | **str** | Identifier of the website display group associated with an Amazon catalog item. | [optional] 
**website_display_group_name** | **str** | Display name of the website display group associated with an Amazon catalog item. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_summary_by_marketplace import ItemSummaryByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemSummaryByMarketplace from a JSON string
item_summary_by_marketplace_instance = ItemSummaryByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemSummaryByMarketplace.to_json())

# convert the object into a dict
item_summary_by_marketplace_dict = item_summary_by_marketplace_instance.to_dict()
# create an instance of ItemSummaryByMarketplace from a dict
item_summary_by_marketplace_from_dict = ItemSummaryByMarketplace.from_dict(item_summary_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


