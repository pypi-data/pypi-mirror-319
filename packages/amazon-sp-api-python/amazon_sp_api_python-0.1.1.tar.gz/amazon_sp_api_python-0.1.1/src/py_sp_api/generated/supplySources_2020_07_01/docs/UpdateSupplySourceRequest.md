# UpdateSupplySourceRequest

A request to update the configuration and capabilities of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **str** | The custom alias for this supply source | [optional] 
**configuration** | [**SupplySourceConfiguration**](SupplySourceConfiguration.md) |  | [optional] 
**capabilities** | [**SupplySourceCapabilities**](SupplySourceCapabilities.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.update_supply_source_request import UpdateSupplySourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSupplySourceRequest from a JSON string
update_supply_source_request_instance = UpdateSupplySourceRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateSupplySourceRequest.to_json())

# convert the object into a dict
update_supply_source_request_dict = update_supply_source_request_instance.to_dict()
# create an instance of UpdateSupplySourceRequest from a dict
update_supply_source_request_from_dict = UpdateSupplySourceRequest.from_dict(update_supply_source_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


