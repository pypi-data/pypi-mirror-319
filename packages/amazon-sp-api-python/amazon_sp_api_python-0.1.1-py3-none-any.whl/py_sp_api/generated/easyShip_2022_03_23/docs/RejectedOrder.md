# RejectedOrder

A order which we couldn't schedule on your behalf. It contains its id, and information on the error.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier. Identifies the order that the seller wants to deliver using Amazon Easy Ship. | 
**error** | [**Error**](Error.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.rejected_order import RejectedOrder

# TODO update the JSON string below
json = "{}"
# create an instance of RejectedOrder from a JSON string
rejected_order_instance = RejectedOrder.from_json(json)
# print the JSON string representation of the object
print(RejectedOrder.to_json())

# convert the object into a dict
rejected_order_dict = rejected_order_instance.to_dict()
# create an instance of RejectedOrder from a dict
rejected_order_from_dict = RejectedOrder.from_dict(rejected_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


