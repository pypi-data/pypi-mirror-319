# CurrencyAmount

Currency type and amount.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**currency_code** | **str** | Three-digit currency code in ISO 4217 format. | 
**amount** | **float** | The currency amount. | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.currency_amount import CurrencyAmount

# TODO update the JSON string below
json = "{}"
# create an instance of CurrencyAmount from a JSON string
currency_amount_instance = CurrencyAmount.from_json(json)
# print the JSON string representation of the object
print(CurrencyAmount.to_json())

# convert the object into a dict
currency_amount_dict = currency_amount_instance.to_dict()
# create an instance of CurrencyAmount from a dict
currency_amount_from_dict = CurrencyAmount.from_dict(currency_amount_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


