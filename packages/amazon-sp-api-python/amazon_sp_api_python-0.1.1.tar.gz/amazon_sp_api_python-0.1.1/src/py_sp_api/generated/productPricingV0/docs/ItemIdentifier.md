# ItemIdentifier

Information that identifies an item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace from which prices are returned. | 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**seller_sku** | **str** | The seller stock keeping unit (SKU) of the item. | [optional] 
**item_condition** | [**ConditionType**](ConditionType.md) |  | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.item_identifier import ItemIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ItemIdentifier from a JSON string
item_identifier_instance = ItemIdentifier.from_json(json)
# print the JSON string representation of the object
print(ItemIdentifier.to_json())

# convert the object into a dict
item_identifier_dict = item_identifier_instance.to_dict()
# create an instance of ItemIdentifier from a dict
item_identifier_from_dict = ItemIdentifier.from_dict(item_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


