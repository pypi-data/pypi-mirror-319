# CreateSupplySourceRequest

A request to create a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supply_source_code** | **str** | The seller-provided unique supply source code. | 
**alias** | **str** | The custom alias for this supply source | 
**address** | [**Address**](Address.md) |  | 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.create_supply_source_request import CreateSupplySourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSupplySourceRequest from a JSON string
create_supply_source_request_instance = CreateSupplySourceRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSupplySourceRequest.to_json())

# convert the object into a dict
create_supply_source_request_dict = create_supply_source_request_instance.to_dict()
# create an instance of CreateSupplySourceRequest from a dict
create_supply_source_request_from_dict = CreateSupplySourceRequest.from_dict(create_supply_source_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


