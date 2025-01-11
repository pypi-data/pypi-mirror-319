# AffordabilityExpenseEvent

An expense related to an affordability promotion.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined identifier for an order. | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**marketplace_id** | **str** | An encrypted, Amazon-defined marketplace identifier. | [optional] 
**transaction_type** | **str** | Indicates the type of transaction.   Possible values:  * Charge - For an affordability promotion expense.  * Refund - For an affordability promotion expense reversal. | [optional] 
**base_expense** | [**Currency**](Currency.md) |  | [optional] 
**tax_type_cgst** | [**Currency**](Currency.md) |  | 
**tax_type_sgst** | [**Currency**](Currency.md) |  | 
**tax_type_igst** | [**Currency**](Currency.md) |  | 
**total_expense** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.affordability_expense_event import AffordabilityExpenseEvent

# TODO update the JSON string below
json = "{}"
# create an instance of AffordabilityExpenseEvent from a JSON string
affordability_expense_event_instance = AffordabilityExpenseEvent.from_json(json)
# print the JSON string representation of the object
print(AffordabilityExpenseEvent.to_json())

# convert the object into a dict
affordability_expense_event_dict = affordability_expense_event_instance.to_dict()
# create an instance of AffordabilityExpenseEvent from a dict
affordability_expense_event_from_dict = AffordabilityExpenseEvent.from_dict(affordability_expense_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


