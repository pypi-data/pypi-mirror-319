# CreateFulfillmentOrderItem

Item information for creating a fulfillment order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**seller_fulfillment_order_item_id** | **str** | A fulfillment order item identifier that the seller creates to track fulfillment order items. Used to disambiguate multiple fulfillment items that have the same &#x60;SellerSKU&#x60;. For example, the seller might assign different &#x60;SellerFulfillmentOrderItemId&#x60; values to two items in a fulfillment order that share the same &#x60;SellerSKU&#x60; but have different &#x60;GiftMessage&#x60; values. | 
**quantity** | **int** | The item quantity. | 
**gift_message** | **str** | A message to the gift recipient, if applicable. | [optional] 
**displayable_comment** | **str** | Item-specific text that displays in recipient-facing materials such as the outbound shipment packing slip. | [optional] 
**fulfillment_network_sku** | **str** | Amazon&#39;s fulfillment network SKU of the item. | [optional] 
**per_unit_declared_value** | [**Money**](Money.md) |  | [optional] 
**per_unit_price** | [**Money**](Money.md) |  | [optional] 
**per_unit_tax** | [**Money**](Money.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.create_fulfillment_order_item import CreateFulfillmentOrderItem

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFulfillmentOrderItem from a JSON string
create_fulfillment_order_item_instance = CreateFulfillmentOrderItem.from_json(json)
# print the JSON string representation of the object
print(CreateFulfillmentOrderItem.to_json())

# convert the object into a dict
create_fulfillment_order_item_dict = create_fulfillment_order_item_instance.to_dict()
# create an instance of CreateFulfillmentOrderItem from a dict
create_fulfillment_order_item_from_dict = CreateFulfillmentOrderItem.from_dict(create_fulfillment_order_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


