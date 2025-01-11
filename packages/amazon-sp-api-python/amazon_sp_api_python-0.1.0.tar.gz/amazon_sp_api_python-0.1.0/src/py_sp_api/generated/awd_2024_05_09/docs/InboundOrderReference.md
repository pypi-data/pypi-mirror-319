# InboundOrderReference

A response that contains the reference identifiers for the newly created or updated inbound order. Consists of an order ID and version.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | Order ID of the inbound order. | 
**order_version** | **str** | Order version of the inbound order. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inbound_order_reference import InboundOrderReference

# TODO update the JSON string below
json = "{}"
# create an instance of InboundOrderReference from a JSON string
inbound_order_reference_instance = InboundOrderReference.from_json(json)
# print the JSON string representation of the object
print(InboundOrderReference.to_json())

# convert the object into a dict
inbound_order_reference_dict = inbound_order_reference_instance.to_dict()
# create an instance of InboundOrderReference from a dict
inbound_order_reference_from_dict = InboundOrderReference.from_dict(inbound_order_reference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


