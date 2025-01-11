# StandardComparisonProductBlock

The A+ Content standard comparison product block.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | **int** | The rank or index of this comparison product block within the module. Different blocks cannot occupy the same position within a single module. | 
**image** | [**ImageComponent**](ImageComponent.md) |  | [optional] 
**title** | **str** | The comparison product title. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN). | [optional] 
**highlight** | **bool** | Determines whether this block of content is visually highlighted. | [optional] 
**metrics** | [**List[PlainTextItem]**](PlainTextItem.md) | Comparison metrics for the product. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_comparison_product_block import StandardComparisonProductBlock

# TODO update the JSON string below
json = "{}"
# create an instance of StandardComparisonProductBlock from a JSON string
standard_comparison_product_block_instance = StandardComparisonProductBlock.from_json(json)
# print the JSON string representation of the object
print(StandardComparisonProductBlock.to_json())

# convert the object into a dict
standard_comparison_product_block_dict = standard_comparison_product_block_instance.to_dict()
# create an instance of StandardComparisonProductBlock from a dict
standard_comparison_product_block_from_dict = StandardComparisonProductBlock.from_dict(standard_comparison_product_block_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


