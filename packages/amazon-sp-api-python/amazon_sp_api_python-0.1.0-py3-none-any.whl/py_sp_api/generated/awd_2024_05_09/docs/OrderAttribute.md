# OrderAttribute

Consists of the order preference and corresponding preference value.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_preference** | [**OrderPreference**](OrderPreference.md) |  | 
**order_preference_value** | [**OrderPreferenceValue**](OrderPreferenceValue.md) |  | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.order_attribute import OrderAttribute

# TODO update the JSON string below
json = "{}"
# create an instance of OrderAttribute from a JSON string
order_attribute_instance = OrderAttribute.from_json(json)
# print the JSON string representation of the object
print(OrderAttribute.to_json())

# convert the object into a dict
order_attribute_dict = order_attribute_instance.to_dict()
# create an instance of OrderAttribute from a dict
order_attribute_from_dict = OrderAttribute.from_dict(order_attribute_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


