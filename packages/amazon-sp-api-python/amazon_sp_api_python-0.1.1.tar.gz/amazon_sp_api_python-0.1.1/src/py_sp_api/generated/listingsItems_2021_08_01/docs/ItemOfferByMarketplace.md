# ItemOfferByMarketplace

Offer details of a listings item for an Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The Amazon marketplace identifier. | 
**offer_type** | **str** | Type of offer for the listings item. | 
**price** | [**Money**](Money.md) |  | 
**points** | [**Points**](Points.md) |  | [optional] 
**audience** | [**Audience**](Audience.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.item_offer_by_marketplace import ItemOfferByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemOfferByMarketplace from a JSON string
item_offer_by_marketplace_instance = ItemOfferByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemOfferByMarketplace.to_json())

# convert the object into a dict
item_offer_by_marketplace_dict = item_offer_by_marketplace_instance.to_dict()
# create an instance of ItemOfferByMarketplace from a dict
item_offer_by_marketplace_from_dict = ItemOfferByMarketplace.from_dict(item_offer_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


