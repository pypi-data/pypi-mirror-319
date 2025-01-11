# DebtRecoveryItem

An item of a debt payment or debt adjustment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recovery_amount** | [**Currency**](Currency.md) |  | [optional] 
**original_amount** | [**Currency**](Currency.md) |  | [optional] 
**group_begin_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**group_end_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.debt_recovery_item import DebtRecoveryItem

# TODO update the JSON string below
json = "{}"
# create an instance of DebtRecoveryItem from a JSON string
debt_recovery_item_instance = DebtRecoveryItem.from_json(json)
# print the JSON string representation of the object
print(DebtRecoveryItem.to_json())

# convert the object into a dict
debt_recovery_item_dict = debt_recovery_item_instance.to_dict()
# create an instance of DebtRecoveryItem from a dict
debt_recovery_item_from_dict = DebtRecoveryItem.from_dict(debt_recovery_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


