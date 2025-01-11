# PaymentsContext

Additional information related to payments-related transactions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_type** | **str** | The type of payment. | [optional] 
**payment_method** | **str** | The method of payment. | [optional] 
**payment_reference** | **str** | The reference number of the payment. | [optional] 
**payment_date** | **datetime** | A date in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.payments_context import PaymentsContext

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentsContext from a JSON string
payments_context_instance = PaymentsContext.from_json(json)
# print the JSON string representation of the object
print(PaymentsContext.to_json())

# convert the object into a dict
payments_context_dict = payments_context_instance.to_dict()
# create an instance of PaymentsContext from a dict
payments_context_from_dict = PaymentsContext.from_dict(payments_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


