# OutboundOrderReference

A response that contains the reference identifier for the newly created or updated outbound order. This includes an order ID.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | outbound order ID. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.outbound_order_reference import OutboundOrderReference

# TODO update the JSON string below
json = "{}"
# create an instance of OutboundOrderReference from a JSON string
outbound_order_reference_instance = OutboundOrderReference.from_json(json)
# print the JSON string representation of the object
print(OutboundOrderReference.to_json())

# convert the object into a dict
outbound_order_reference_dict = outbound_order_reference_instance.to_dict()
# create an instance of OutboundOrderReference from a dict
outbound_order_reference_from_dict = OutboundOrderReference.from_dict(outbound_order_reference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


