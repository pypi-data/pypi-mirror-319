# StandardComparisonTableModule

The standard product comparison table.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_columns** | [**List[StandardComparisonProductBlock]**](StandardComparisonProductBlock.md) |  | [optional] 
**metric_row_labels** | [**List[PlainTextItem]**](PlainTextItem.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_comparison_table_module import StandardComparisonTableModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardComparisonTableModule from a JSON string
standard_comparison_table_module_instance = StandardComparisonTableModule.from_json(json)
# print the JSON string representation of the object
print(StandardComparisonTableModule.to_json())

# convert the object into a dict
standard_comparison_table_module_dict = standard_comparison_table_module_instance.to_dict()
# create an instance of StandardComparisonTableModule from a dict
standard_comparison_table_module_from_dict = StandardComparisonTableModule.from_dict(standard_comparison_table_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


