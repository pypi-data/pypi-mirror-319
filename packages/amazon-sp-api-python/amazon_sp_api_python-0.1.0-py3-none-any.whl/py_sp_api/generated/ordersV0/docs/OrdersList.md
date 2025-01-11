# OrdersList

A list of orders along with additional information to make subsequent API calls.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**orders** | [**List[Order]**](Order.md) | A list of orders. | 
**next_token** | **str** | When present and not empty, pass this string token in the next request to return the next response page. | [optional] 
**last_updated_before** | **str** | Use this date to select orders that were last updated before (or at) a specified time. An update is defined as any change in order status, including the creation of a new order. Includes updates made by Amazon and by the seller. All dates must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. | [optional] 
**created_before** | **str** | Use this date to select orders created before (or at) a specified time. Only orders placed before the specified time are returned. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.orders_list import OrdersList

# TODO update the JSON string below
json = "{}"
# create an instance of OrdersList from a JSON string
orders_list_instance = OrdersList.from_json(json)
# print the JSON string representation of the object
print(OrdersList.to_json())

# convert the object into a dict
orders_list_dict = orders_list_instance.to_dict()
# create an instance of OrdersList from a dict
orders_list_from_dict = OrdersList.from_dict(orders_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


