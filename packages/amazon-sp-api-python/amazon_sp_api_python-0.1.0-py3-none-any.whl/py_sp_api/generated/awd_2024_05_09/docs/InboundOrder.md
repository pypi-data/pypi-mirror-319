# InboundOrder

Represents an AWD inbound order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel_placed_inbound_shipments** | [**List[InboundShipment]**](InboundShipment.md) | List of inbound shipments part of this order. | 
**created_at** | **datetime** | Date when this order was created. | 
**external_reference_id** | **str** | Reference ID that can be used to correlate the order with partner resources. | [optional] 
**order_id** | **str** | Inbound order ID. | 
**order_status** | [**InboundStatus**](InboundStatus.md) |  | 
**order_version** | **str** | Inbound order version. | 
**origin_address** | [**Address**](Address.md) |  | 
**packages_to_inbound** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | List of packages to be inbounded. | 
**preferences** | [**InboundPreferences**](InboundPreferences.md) |  | [optional] 
**ship_by** | **datetime** | Date by which this order will be shipped. | [optional] 
**updated_at** | **datetime** | Date when this order was last updated. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inbound_order import InboundOrder

# TODO update the JSON string below
json = "{}"
# create an instance of InboundOrder from a JSON string
inbound_order_instance = InboundOrder.from_json(json)
# print the JSON string representation of the object
print(InboundOrder.to_json())

# convert the object into a dict
inbound_order_dict = inbound_order_instance.to_dict()
# create an instance of InboundOrder from a dict
inbound_order_from_dict = InboundOrder.from_dict(inbound_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


