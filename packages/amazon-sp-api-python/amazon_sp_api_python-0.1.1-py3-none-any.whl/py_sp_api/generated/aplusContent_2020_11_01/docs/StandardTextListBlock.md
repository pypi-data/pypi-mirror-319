# StandardTextListBlock

The A+ Content standard fixed length list of text, usually presented as bullet points.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text_list** | [**List[TextItem]**](TextItem.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_text_list_block import StandardTextListBlock

# TODO update the JSON string below
json = "{}"
# create an instance of StandardTextListBlock from a JSON string
standard_text_list_block_instance = StandardTextListBlock.from_json(json)
# print the JSON string representation of the object
print(StandardTextListBlock.to_json())

# convert the object into a dict
standard_text_list_block_dict = standard_text_list_block_instance.to_dict()
# create an instance of StandardTextListBlock from a dict
standard_text_list_block_from_dict = StandardTextListBlock.from_dict(standard_text_list_block_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


