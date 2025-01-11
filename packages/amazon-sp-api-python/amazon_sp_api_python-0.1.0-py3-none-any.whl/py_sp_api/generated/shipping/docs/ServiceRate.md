# ServiceRate

The specific rate for a shipping service, or null if no service available.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_charge** | [**Currency**](Currency.md) |  | 
**billable_weight** | [**Weight**](Weight.md) |  | 
**service_type** | [**ServiceType**](ServiceType.md) |  | 
**promise** | [**ShippingPromiseSet**](ShippingPromiseSet.md) |  | 

## Example

```python
from py_sp_api.generated.shipping.models.service_rate import ServiceRate

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceRate from a JSON string
service_rate_instance = ServiceRate.from_json(json)
# print the JSON string representation of the object
print(ServiceRate.to_json())

# convert the object into a dict
service_rate_dict = service_rate_instance.to_dict()
# create an instance of ServiceRate from a dict
service_rate_from_dict = ServiceRate.from_dict(service_rate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


