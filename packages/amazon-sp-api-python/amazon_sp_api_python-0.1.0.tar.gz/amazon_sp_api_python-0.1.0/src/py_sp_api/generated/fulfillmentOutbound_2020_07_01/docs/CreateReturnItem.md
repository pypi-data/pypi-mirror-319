# CreateReturnItem

An item that Amazon accepted for return.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_return_item_id** | **str** | An identifier assigned by the seller to the return item. | 
**seller_fulfillment_order_item_id** | **str** | The identifier assigned to the item by the seller when the fulfillment order was created. | 
**amazon_shipment_id** | **str** | The identifier for the shipment that is associated with the return item. | 
**return_reason_code** | **str** | The return reason code assigned to the return item by the seller. | 
**return_comment** | **str** | An optional comment about the return item. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.create_return_item import CreateReturnItem

# TODO update the JSON string below
json = "{}"
# create an instance of CreateReturnItem from a JSON string
create_return_item_instance = CreateReturnItem.from_json(json)
# print the JSON string representation of the object
print(CreateReturnItem.to_json())

# convert the object into a dict
create_return_item_dict = create_return_item_instance.to_dict()
# create an instance of CreateReturnItem from a dict
create_return_item_from_dict = CreateReturnItem.from_dict(create_return_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


