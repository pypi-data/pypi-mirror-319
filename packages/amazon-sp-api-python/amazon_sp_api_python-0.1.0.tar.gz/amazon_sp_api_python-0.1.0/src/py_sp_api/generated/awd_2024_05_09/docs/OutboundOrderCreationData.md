# OutboundOrderCreationData

Payload for creating an outbound order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_preferences** | [**List[OrderAttribute]**](OrderAttribute.md) | Order preferences for the outbound order. | [optional] 
**packages_to_outbound** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | List of packages to be outbound. | [optional] 
**products_to_outbound** | [**List[ProductQuantity]**](ProductQuantity.md) | List of product units to be outbound. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.outbound_order_creation_data import OutboundOrderCreationData

# TODO update the JSON string below
json = "{}"
# create an instance of OutboundOrderCreationData from a JSON string
outbound_order_creation_data_instance = OutboundOrderCreationData.from_json(json)
# print the JSON string representation of the object
print(OutboundOrderCreationData.to_json())

# convert the object into a dict
outbound_order_creation_data_dict = outbound_order_creation_data_instance.to_dict()
# create an instance of OutboundOrderCreationData from a dict
outbound_order_creation_data_from_dict = OutboundOrderCreationData.from_dict(outbound_order_creation_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


