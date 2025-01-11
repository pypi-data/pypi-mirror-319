# MoneyType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**currency_code** | **str** | The currency code in ISO 4217 format. | [optional] 
**amount** | **float** | The monetary value. | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.money_type import MoneyType

# TODO update the JSON string below
json = "{}"
# create an instance of MoneyType from a JSON string
money_type_instance = MoneyType.from_json(json)
# print the JSON string representation of the object
print(MoneyType.to_json())

# convert the object into a dict
money_type_dict = money_type_instance.to_dict()
# create an instance of MoneyType from a dict
money_type_from_dict = MoneyType.from_dict(money_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


