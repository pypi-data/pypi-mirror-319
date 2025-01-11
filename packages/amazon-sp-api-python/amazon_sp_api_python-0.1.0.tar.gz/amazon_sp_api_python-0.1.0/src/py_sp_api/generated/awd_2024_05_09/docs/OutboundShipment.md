# OutboundShipment

Represents an AWD outbound shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | Timestamp when the shipment was created. | [optional] 
**destination_address** | [**Address**](Address.md) |  | 
**order_id** | **str** | Outbound order ID this outbound shipment belongs to. | 
**origin_address** | [**Address**](Address.md) |  | 
**shipment_package_quantities** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | Specific distribution packages that are included in the context of this shipment. | [optional] 
**shipment_id** | **str** | Unique shipment ID. | 
**shipment_product_quantities** | [**List[ProductQuantity]**](ProductQuantity.md) | Specific product units that are included in the context of this shipment. | [optional] 
**shipment_status** | [**OutboundShipmentStatus**](OutboundShipmentStatus.md) |  | 
**updated_at** | **datetime** | Timestamp when the shipment was updated. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.outbound_shipment import OutboundShipment

# TODO update the JSON string below
json = "{}"
# create an instance of OutboundShipment from a JSON string
outbound_shipment_instance = OutboundShipment.from_json(json)
# print the JSON string representation of the object
print(OutboundShipment.to_json())

# convert the object into a dict
outbound_shipment_dict = outbound_shipment_instance.to_dict()
# create an instance of OutboundShipment from a dict
outbound_shipment_from_dict = OutboundShipment.from_dict(outbound_shipment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


