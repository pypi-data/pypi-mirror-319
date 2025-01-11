# UpdateFulfillmentOrderItem

Item information for updating a fulfillment order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | [optional] 
**seller_fulfillment_order_item_id** | **str** | Identifies the fulfillment order item to update. Created with a previous call to the &#x60;createFulfillmentOrder&#x60; operation. | 
**quantity** | **int** | The item quantity. | 
**gift_message** | **str** | A message to the gift recipient, if applicable. | [optional] 
**displayable_comment** | **str** | Item-specific text that displays in recipient-facing materials such as the outbound shipment packing slip. | [optional] 
**fulfillment_network_sku** | **str** | Amazon&#39;s fulfillment network SKU of the item. | [optional] 
**order_item_disposition** | **str** | Indicates whether the item is sellable or unsellable. | [optional] 
**per_unit_declared_value** | [**Money**](Money.md) |  | [optional] 
**per_unit_price** | [**Money**](Money.md) |  | [optional] 
**per_unit_tax** | [**Money**](Money.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.update_fulfillment_order_item import UpdateFulfillmentOrderItem

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateFulfillmentOrderItem from a JSON string
update_fulfillment_order_item_instance = UpdateFulfillmentOrderItem.from_json(json)
# print the JSON string representation of the object
print(UpdateFulfillmentOrderItem.to_json())

# convert the object into a dict
update_fulfillment_order_item_dict = update_fulfillment_order_item_instance.to_dict()
# create an instance of UpdateFulfillmentOrderItem from a dict
update_fulfillment_order_item_from_dict = UpdateFulfillmentOrderItem.from_dict(update_fulfillment_order_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


