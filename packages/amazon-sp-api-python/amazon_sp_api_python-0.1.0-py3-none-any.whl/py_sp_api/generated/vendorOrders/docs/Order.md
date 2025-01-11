# Order

Represents an order placed by Amazon, including the purchase order number, current state, and order details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | The purchase order number for this order. Formatting Notes: 8-character alpha-numeric code. | 
**purchase_order_state** | **str** | This field will contain the current state of the purchase order. | 
**order_details** | [**OrderDetails**](OrderDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order import Order

# TODO update the JSON string below
json = "{}"
# create an instance of Order from a JSON string
order_instance = Order.from_json(json)
# print the JSON string representation of the object
print(Order.to_json())

# convert the object into a dict
order_dict = order_instance.to_dict()
# create an instance of Order from a dict
order_from_dict = Order.from_dict(order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


