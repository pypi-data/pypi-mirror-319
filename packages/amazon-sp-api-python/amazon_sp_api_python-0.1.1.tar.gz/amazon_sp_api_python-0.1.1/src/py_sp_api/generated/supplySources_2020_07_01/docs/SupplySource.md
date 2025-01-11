# SupplySource

The supply source details, including configurations and capabilities.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supply_source_id** | **str** | An Amazon generated unique supply source ID. | [optional] 
**supply_source_code** | **str** | The seller-provided unique supply source code. | [optional] 
**alias** | **str** | The custom alias for this supply source | [optional] 
**status** | [**SupplySourceStatusReadOnly**](SupplySourceStatusReadOnly.md) |  | [optional] 
**address** | [**Address**](Address.md) |  | [optional] 
**configuration** | [**SupplySourceConfiguration**](SupplySourceConfiguration.md) |  | [optional] 
**capabilities** | [**SupplySourceCapabilities**](SupplySourceCapabilities.md) |  | [optional] 
**created_at** | **str** | A date and time in the rfc3339 format. | [optional] 
**updated_at** | **str** | A date and time in the rfc3339 format. | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.supply_source import SupplySource

# TODO update the JSON string below
json = "{}"
# create an instance of SupplySource from a JSON string
supply_source_instance = SupplySource.from_json(json)
# print the JSON string representation of the object
print(SupplySource.to_json())

# convert the object into a dict
supply_source_dict = supply_source_instance.to_dict()
# create an instance of SupplySource from a dict
supply_source_from_dict = SupplySource.from_dict(supply_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


