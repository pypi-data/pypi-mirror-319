# CreateSupplySourceResponse

The result of creating a new supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supply_source_id** | **str** | An Amazon generated unique supply source ID. | 
**supply_source_code** | **str** | The seller-provided unique supply source code. | 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.create_supply_source_response import CreateSupplySourceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSupplySourceResponse from a JSON string
create_supply_source_response_instance = CreateSupplySourceResponse.from_json(json)
# print the JSON string representation of the object
print(CreateSupplySourceResponse.to_json())

# convert the object into a dict
create_supply_source_response_dict = create_supply_source_response_instance.to_dict()
# create an instance of CreateSupplySourceResponse from a dict
create_supply_source_response_from_dict = CreateSupplySourceResponse.from_dict(create_supply_source_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


