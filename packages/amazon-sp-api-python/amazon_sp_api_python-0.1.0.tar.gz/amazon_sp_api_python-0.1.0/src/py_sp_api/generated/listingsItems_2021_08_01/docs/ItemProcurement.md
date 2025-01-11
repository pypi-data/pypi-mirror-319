# ItemProcurement

The vendor procurement information for the listings item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cost_price** | [**Money**](Money.md) |  | 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.item_procurement import ItemProcurement

# TODO update the JSON string below
json = "{}"
# create an instance of ItemProcurement from a JSON string
item_procurement_instance = ItemProcurement.from_json(json)
# print the JSON string representation of the object
print(ItemProcurement.to_json())

# convert the object into a dict
item_procurement_dict = item_procurement_instance.to_dict()
# create an instance of ItemProcurement from a dict
item_procurement_from_dict = ItemProcurement.from_dict(item_procurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


