# GetRatesResponse

The response schema for the getRates operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetRatesResult**](GetRatesResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.get_rates_response import GetRatesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetRatesResponse from a JSON string
get_rates_response_instance = GetRatesResponse.from_json(json)
# print the JSON string representation of the object
print(GetRatesResponse.to_json())

# convert the object into a dict
get_rates_response_dict = get_rates_response_instance.to_dict()
# create an instance of GetRatesResponse from a dict
get_rates_response_from_dict = GetRatesResponse.from_dict(get_rates_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


