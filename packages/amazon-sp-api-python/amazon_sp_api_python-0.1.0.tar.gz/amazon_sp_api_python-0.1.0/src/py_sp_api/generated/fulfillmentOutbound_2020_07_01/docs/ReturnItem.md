# ReturnItem

An item that Amazon accepted for return.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_return_item_id** | **str** | An identifier assigned by the seller to the return item. | 
**seller_fulfillment_order_item_id** | **str** | The identifier assigned to the item by the seller when the fulfillment order was created. | 
**amazon_shipment_id** | **str** | The identifier for the shipment that is associated with the return item. | 
**seller_return_reason_code** | **str** | The return reason code assigned to the return item by the seller. | 
**return_comment** | **str** | An optional comment about the return item. | [optional] 
**amazon_return_reason_code** | **str** | The return reason code that the Amazon fulfillment center assigned to the return item. | [optional] 
**status** | [**FulfillmentReturnItemStatus**](FulfillmentReturnItemStatus.md) |  | 
**status_changed_date** | **datetime** | Date timestamp | 
**return_authorization_id** | **str** | Identifies the return authorization used to return this item. Refer to &#x60;ReturnAuthorization&#x60;. | [optional] 
**return_received_condition** | [**ReturnItemDisposition**](ReturnItemDisposition.md) |  | [optional] 
**fulfillment_center_id** | **str** | The identifier for the Amazon fulfillment center that processed the return item. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.return_item import ReturnItem

# TODO update the JSON string below
json = "{}"
# create an instance of ReturnItem from a JSON string
return_item_instance = ReturnItem.from_json(json)
# print the JSON string representation of the object
print(ReturnItem.to_json())

# convert the object into a dict
return_item_dict = return_item_instance.to_dict()
# create an instance of ReturnItem from a dict
return_item_from_dict = ReturnItem.from_dict(return_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


