# AcceptedRate

The specific rate purchased for the shipment, or null if unpurchased.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_charge** | [**Currency**](Currency.md) |  | [optional] 
**billed_weight** | [**Weight**](Weight.md) |  | [optional] 
**service_type** | [**ServiceType**](ServiceType.md) |  | [optional] 
**promise** | [**ShippingPromiseSet**](ShippingPromiseSet.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.accepted_rate import AcceptedRate

# TODO update the JSON string below
json = "{}"
# create an instance of AcceptedRate from a JSON string
accepted_rate_instance = AcceptedRate.from_json(json)
# print the JSON string representation of the object
print(AcceptedRate.to_json())

# convert the object into a dict
accepted_rate_dict = accepted_rate_instance.to_dict()
# create an instance of AcceptedRate from a dict
accepted_rate_from_dict = AcceptedRate.from_dict(accepted_rate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


