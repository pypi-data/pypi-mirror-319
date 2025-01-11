# GetRatesResult

The payload for the getRates operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_token** | **str** | A unique token generated to identify a getRates operation. | 
**rates** | [**List[Rate]**](Rate.md) | A list of eligible shipping service offerings. | 
**ineligible_rates** | [**List[IneligibleRate]**](IneligibleRate.md) | A list of ineligible shipping service offerings. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_rates_result import GetRatesResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetRatesResult from a JSON string
get_rates_result_instance = GetRatesResult.from_json(json)
# print the JSON string representation of the object
print(GetRatesResult.to_json())

# convert the object into a dict
get_rates_result_dict = get_rates_result_instance.to_dict()
# create an instance of GetRatesResult from a dict
get_rates_result_from_dict = GetRatesResult.from_dict(get_rates_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


