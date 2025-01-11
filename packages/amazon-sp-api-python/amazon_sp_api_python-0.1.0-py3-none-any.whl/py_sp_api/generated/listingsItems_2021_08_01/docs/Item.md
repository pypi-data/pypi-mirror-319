# Item

A listings item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sku** | **str** | A selling partner provided identifier for an Amazon listing. | 
**summaries** | [**List[ItemSummaryByMarketplace]**](ItemSummaryByMarketplace.md) | Summary details of a listings item. | [optional] 
**attributes** | **Dict[str, object]** | A JSON object containing structured listings item attribute data keyed by attribute name. | [optional] 
**issues** | [**List[Issue]**](Issue.md) | The issues associated with the listings item. | [optional] 
**offers** | [**List[ItemOfferByMarketplace]**](ItemOfferByMarketplace.md) | Offer details for the listings item. | [optional] 
**fulfillment_availability** | [**List[FulfillmentAvailability]**](FulfillmentAvailability.md) | The fulfillment availability for the listings item. | [optional] 
**procurement** | [**List[ItemProcurement]**](ItemProcurement.md) | The vendor procurement information for the listings item. | [optional] 
**relationships** | [**List[ItemRelationshipsByMarketplace]**](ItemRelationshipsByMarketplace.md) | Relationships for a listing item, by marketplace (for example, variations). | [optional] 
**product_types** | [**List[ItemProductTypeByMarketplace]**](ItemProductTypeByMarketplace.md) | Product types for a listing item, by marketplace. | [optional] 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.item import Item

# TODO update the JSON string below
json = "{}"
# create an instance of Item from a JSON string
item_instance = Item.from_json(json)
# print the JSON string representation of the object
print(Item.to_json())

# convert the object into a dict
item_dict = item_instance.to_dict()
# create an instance of Item from a dict
item_from_dict = Item.from_dict(item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


