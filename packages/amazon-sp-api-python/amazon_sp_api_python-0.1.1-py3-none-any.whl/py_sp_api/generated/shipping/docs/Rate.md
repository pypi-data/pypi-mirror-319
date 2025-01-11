# Rate

The available rate that can be used to send the shipment

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rate_id** | **str** | An identifier for the rate. | [optional] 
**total_charge** | [**Currency**](Currency.md) |  | [optional] 
**billed_weight** | [**Weight**](Weight.md) |  | [optional] 
**expiration_time** | **datetime** | The time after which the offering will expire. | [optional] 
**service_type** | [**ServiceType**](ServiceType.md) |  | [optional] 
**promise** | [**ShippingPromiseSet**](ShippingPromiseSet.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.rate import Rate

# TODO update the JSON string below
json = "{}"
# create an instance of Rate from a JSON string
rate_instance = Rate.from_json(json)
# print the JSON string representation of the object
print(Rate.to_json())

# convert the object into a dict
rate_dict = rate_instance.to_dict()
# create an instance of Rate from a dict
rate_from_dict = Rate.from_dict(rate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


