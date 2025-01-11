# StandardTextPairBlock

The A+ Content standard label and description block, comprised of a pair of text components.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | [**TextComponent**](TextComponent.md) |  | [optional] 
**description** | [**TextComponent**](TextComponent.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_text_pair_block import StandardTextPairBlock

# TODO update the JSON string below
json = "{}"
# create an instance of StandardTextPairBlock from a JSON string
standard_text_pair_block_instance = StandardTextPairBlock.from_json(json)
# print the JSON string representation of the object
print(StandardTextPairBlock.to_json())

# convert the object into a dict
standard_text_pair_block_dict = standard_text_pair_block_instance.to_dict()
# create an instance of StandardTextPairBlock from a dict
standard_text_pair_block_from_dict = StandardTextPairBlock.from_dict(standard_text_pair_block_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


