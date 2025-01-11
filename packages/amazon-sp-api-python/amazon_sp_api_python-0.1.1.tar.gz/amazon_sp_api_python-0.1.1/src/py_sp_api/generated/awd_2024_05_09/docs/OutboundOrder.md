# OutboundOrder

Represents an AWD outbound order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**confirmed_on** | **datetime** | Date on which this outbound order was confirmed. | [optional] 
**created_at** | **datetime** | Date on which this outbound order was created. | [optional] 
**eligible_packages_to_outbound** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | List of packages that are eligible for outbound. | [optional] 
**eligible_products_to_outbound** | [**List[ProductQuantity]**](ProductQuantity.md) | List of product units that are eligible for outbound. | [optional] 
**execution_errors** | [**List[OutboundExecutionError]**](OutboundExecutionError.md) | Execution errors associated with the outbound order. This field will be populated if the order failed validation. | [optional] 
**order_id** | **str** | Order ID for the outbound order. | 
**order_preferences** | [**List[OrderAttribute]**](OrderAttribute.md) | Order preferences for this outbound order. | [optional] 
**order_status** | [**OutboundStatus**](OutboundStatus.md) |  | 
**outbound_shipments** | [**List[OutboundShipment]**](OutboundShipment.md) | List of outbound shipments that are part of this order. | 
**packages_to_outbound** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | List of packages to be outbound. | [optional] 
**products_to_outbound** | [**List[ProductQuantity]**](ProductQuantity.md) | List of product units to be outbound. | [optional] 
**shipped_outbound_packages** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | Outbound packages that are shipped after the execution has completed post confirmation. | [optional] 
**shipped_outbound_products** | [**List[ProductQuantity]**](ProductQuantity.md) | Outbound product units that are shipped after the execution has completed post confirmation. | [optional] 
**updated_at** | **datetime** | Date on which this outbound order was last updated. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.outbound_order import OutboundOrder

# TODO update the JSON string below
json = "{}"
# create an instance of OutboundOrder from a JSON string
outbound_order_instance = OutboundOrder.from_json(json)
# print the JSON string representation of the object
print(OutboundOrder.to_json())

# convert the object into a dict
outbound_order_dict = outbound_order_instance.to_dict()
# create an instance of OutboundOrder from a dict
outbound_order_from_dict = OutboundOrder.from_dict(outbound_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


