# StandardTechSpecsModule

The standard table of technical feature names and definitions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**specification_list** | [**List[StandardTextPairBlock]**](StandardTextPairBlock.md) | The specification list. | 
**table_count** | **int** | The number of tables to present. Features are evenly divided between the tables. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_tech_specs_module import StandardTechSpecsModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardTechSpecsModule from a JSON string
standard_tech_specs_module_instance = StandardTechSpecsModule.from_json(json)
# print the JSON string representation of the object
print(StandardTechSpecsModule.to_json())

# convert the object into a dict
standard_tech_specs_module_dict = standard_tech_specs_module_instance.to_dict()
# create an instance of StandardTechSpecsModule from a dict
standard_tech_specs_module_from_dict = StandardTechSpecsModule.from_dict(standard_tech_specs_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


