# SupplySourceCapabilities

The capabilities of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**outbound** | [**OutboundCapability**](OutboundCapability.md) |  | [optional] 
**services** | [**ServicesCapability**](ServicesCapability.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.supply_source_capabilities import SupplySourceCapabilities

# TODO update the JSON string below
json = "{}"
# create an instance of SupplySourceCapabilities from a JSON string
supply_source_capabilities_instance = SupplySourceCapabilities.from_json(json)
# print the JSON string representation of the object
print(SupplySourceCapabilities.to_json())

# convert the object into a dict
supply_source_capabilities_dict = supply_source_capabilities_instance.to_dict()
# create an instance of SupplySourceCapabilities from a dict
supply_source_capabilities_from_dict = SupplySourceCapabilities.from_dict(supply_source_capabilities_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


