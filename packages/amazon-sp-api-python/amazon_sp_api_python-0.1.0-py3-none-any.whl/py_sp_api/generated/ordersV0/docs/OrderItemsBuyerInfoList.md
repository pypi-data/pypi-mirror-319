# OrderItemsBuyerInfoList

A single order item's buyer information list with the order ID.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_items** | [**List[OrderItemBuyerInfo]**](OrderItemBuyerInfo.md) | A single order item&#39;s buyer information list. | 
**next_token** | **str** | When present and not empty, pass this string token in the next request to return the next response page. | [optional] 
**amazon_order_id** | **str** | An Amazon-defined order identifier, in 3-7-7 format. | 

## Example

```python
from py_sp_api.generated.ordersV0.models.order_items_buyer_info_list import OrderItemsBuyerInfoList

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItemsBuyerInfoList from a JSON string
order_items_buyer_info_list_instance = OrderItemsBuyerInfoList.from_json(json)
# print the JSON string representation of the object
print(OrderItemsBuyerInfoList.to_json())

# convert the object into a dict
order_items_buyer_info_list_dict = order_items_buyer_info_list_instance.to_dict()
# create an instance of OrderItemsBuyerInfoList from a dict
order_items_buyer_info_list_from_dict = OrderItemsBuyerInfoList.from_dict(order_items_buyer_info_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


