# StandardTextBlock

The A+ Content standard text box block, comprised of a paragraph with a headline.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**body** | [**ParagraphComponent**](ParagraphComponent.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_text_block import StandardTextBlock

# TODO update the JSON string below
json = "{}"
# create an instance of StandardTextBlock from a JSON string
standard_text_block_instance = StandardTextBlock.from_json(json)
# print the JSON string representation of the object
print(StandardTextBlock.to_json())

# convert the object into a dict
standard_text_block_dict = standard_text_block_instance.to_dict()
# create an instance of StandardTextBlock from a dict
standard_text_block_from_dict = StandardTextBlock.from_dict(standard_text_block_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


