# SupplySourceListInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **str** | The custom alias for this supply source | [optional] 
**supply_source_id** | **str** | An Amazon generated unique supply source ID. | [optional] 
**supply_source_code** | **str** | The seller-provided unique supply source code. | [optional] 
**address** | [**Address**](Address.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.supply_source_list_inner import SupplySourceListInner

# TODO update the JSON string below
json = "{}"
# create an instance of SupplySourceListInner from a JSON string
supply_source_list_inner_instance = SupplySourceListInner.from_json(json)
# print the JSON string representation of the object
print(SupplySourceListInner.to_json())

# convert the object into a dict
supply_source_list_inner_dict = supply_source_list_inner_instance.to_dict()
# create an instance of SupplySourceListInner from a dict
supply_source_list_inner_from_dict = SupplySourceListInner.from_dict(supply_source_list_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


