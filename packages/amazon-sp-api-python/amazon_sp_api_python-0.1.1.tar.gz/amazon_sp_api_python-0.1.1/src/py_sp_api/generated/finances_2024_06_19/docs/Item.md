# Item

Additional information about the items in a transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | A description of the items in a transaction. | [optional] 
**related_identifiers** | [**List[ItemRelatedIdentifier]**](ItemRelatedIdentifier.md) | Related business identifiers of the item in the transaction. | [optional] 
**total_amount** | [**Currency**](Currency.md) |  | [optional] 
**breakdowns** | [**List[Breakdown]**](Breakdown.md) | A list of breakdowns that provide details on how the total amount is calculated for the transaction. | [optional] 
**contexts** | [**List[Context]**](Context.md) | A list of additional information about the item. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.item import Item

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


