# InboundOrderCreationData

Payload for creating an inbound order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**external_reference_id** | **str** | Reference ID that can be used to correlate the order with partner resources. | [optional] 
**origin_address** | [**Address**](Address.md) |  | 
**packages_to_inbound** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | List of packages to be inbounded. | 
**preferences** | [**InboundPreferences**](InboundPreferences.md) |  | [optional] 
**ship_by** | **datetime** | Estimated date by when goods have to be picked up. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inbound_order_creation_data import InboundOrderCreationData

# TODO update the JSON string below
json = "{}"
# create an instance of InboundOrderCreationData from a JSON string
inbound_order_creation_data_instance = InboundOrderCreationData.from_json(json)
# print the JSON string representation of the object
print(InboundOrderCreationData.to_json())

# convert the object into a dict
inbound_order_creation_data_dict = inbound_order_creation_data_instance.to_dict()
# create an instance of InboundOrderCreationData from a dict
inbound_order_creation_data_from_dict = InboundOrderCreationData.from_dict(inbound_order_creation_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


