# OrderIneligibilityReason

Represents one ineligibility reason for the order (there can be multiple reasons).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Code for the order ineligibility. | 
**description** | **str** | Description detailing the ineligibility reason of the order. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.order_ineligibility_reason import OrderIneligibilityReason

# TODO update the JSON string below
json = "{}"
# create an instance of OrderIneligibilityReason from a JSON string
order_ineligibility_reason_instance = OrderIneligibilityReason.from_json(json)
# print the JSON string representation of the object
print(OrderIneligibilityReason.to_json())

# convert the object into a dict
order_ineligibility_reason_dict = order_ineligibility_reason_instance.to_dict()
# create an instance of OrderIneligibilityReason from a dict
order_ineligibility_reason_from_dict = OrderIneligibilityReason.from_dict(order_ineligibility_reason_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


