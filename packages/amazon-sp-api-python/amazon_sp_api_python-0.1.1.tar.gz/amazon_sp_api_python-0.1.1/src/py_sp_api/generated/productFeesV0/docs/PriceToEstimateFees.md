# PriceToEstimateFees

Price information for an item, used to estimate fees.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**listing_price** | [**MoneyType**](MoneyType.md) |  | 
**shipping** | [**MoneyType**](MoneyType.md) |  | [optional] 
**points** | [**Points**](Points.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.price_to_estimate_fees import PriceToEstimateFees

# TODO update the JSON string below
json = "{}"
# create an instance of PriceToEstimateFees from a JSON string
price_to_estimate_fees_instance = PriceToEstimateFees.from_json(json)
# print the JSON string representation of the object
print(PriceToEstimateFees.to_json())

# convert the object into a dict
price_to_estimate_fees_dict = price_to_estimate_fees_instance.to_dict()
# create an instance of PriceToEstimateFees from a dict
price_to_estimate_fees_from_dict = PriceToEstimateFees.from_dict(price_to_estimate_fees_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


