# OrderAddress

The shipping address for the order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier, in 3-7-7 format. | 
**buyer_company_name** | **str** | The company name of the contact buyer. For IBA orders, the buyer company must be Amazon entities. | [optional] 
**shipping_address** | [**Address**](Address.md) |  | [optional] 
**delivery_preferences** | [**DeliveryPreferences**](DeliveryPreferences.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.order_address import OrderAddress

# TODO update the JSON string below
json = "{}"
# create an instance of OrderAddress from a JSON string
order_address_instance = OrderAddress.from_json(json)
# print the JSON string representation of the object
print(OrderAddress.to_json())

# convert the object into a dict
order_address_dict = order_address_instance.to_dict()
# create an instance of OrderAddress from a dict
order_address_from_dict = OrderAddress.from_dict(order_address_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


