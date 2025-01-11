# GetPricingResponse

The response schema for the `getPricing` and `getCompetitivePricing` operations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[Price]**](Price.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.get_pricing_response import GetPricingResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPricingResponse from a JSON string
get_pricing_response_instance = GetPricingResponse.from_json(json)
# print the JSON string representation of the object
print(GetPricingResponse.to_json())

# convert the object into a dict
get_pricing_response_dict = get_pricing_response_instance.to_dict()
# create an instance of GetPricingResponse from a dict
get_pricing_response_from_dict = GetPricingResponse.from_dict(get_pricing_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


