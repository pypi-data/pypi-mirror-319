# GetRatesResult

The payload schema for the getRates operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_rates** | [**List[ServiceRate]**](ServiceRate.md) | A list of service rates. | 

## Example

```python
from py_sp_api.generated.shipping.models.get_rates_result import GetRatesResult

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


