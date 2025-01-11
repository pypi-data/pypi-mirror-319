# ItemSummaryByMarketplace

Summary details of an Amazon catalog item for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**brand_name** | **str** | Name of the brand associated with an Amazon catalog item. | [optional] 
**browse_node** | **str** | Identifier of the browse node associated with an Amazon catalog item. | [optional] 
**color_name** | **str** | Name of the color associated with an Amazon catalog item. | [optional] 
**item_name** | **str** | Name, or title, associated with an Amazon catalog item. | [optional] 
**manufacturer** | **str** | Name of the manufacturer associated with an Amazon catalog item. | [optional] 
**model_number** | **str** | Model number associated with an Amazon catalog item. | [optional] 
**size_name** | **str** | Name of the size associated with an Amazon catalog item. | [optional] 
**style_name** | **str** | Name of the style associated with an Amazon catalog item. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2020_12_01.models.item_summary_by_marketplace import ItemSummaryByMarketplace

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


