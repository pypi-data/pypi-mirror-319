# ItemSummaryByMarketplace

Summary details of a listings item for an Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. Identifies the Amazon marketplace for the listings item. | 
**asin** | **str** | Amazon Standard Identification Number (ASIN) of the listings item. | [optional] 
**product_type** | **str** | The Amazon product type of the listings item. | 
**condition_type** | **str** | Identifies the condition of the listings item. | [optional] 
**status** | **List[str]** | Statuses that apply to the listings item. | 
**fn_sku** | **str** | The fulfillment network stock keeping unit is an identifier used by Amazon fulfillment centers to identify each unique item. | [optional] 
**item_name** | **str** | The name or title associated with an Amazon catalog item. | [optional] 
**created_date** | **datetime** | The date the listings item was created in ISO 8601 format. | 
**last_updated_date** | **datetime** | The date the listings item was last updated in ISO 8601 format. | 
**main_image** | [**ItemImage**](ItemImage.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.item_summary_by_marketplace import ItemSummaryByMarketplace

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


