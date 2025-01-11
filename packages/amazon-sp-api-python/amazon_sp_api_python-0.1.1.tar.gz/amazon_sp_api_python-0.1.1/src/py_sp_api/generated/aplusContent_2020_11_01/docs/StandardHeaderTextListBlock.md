# StandardHeaderTextListBlock

The A+ standard fixed-length list of text, with a related headline.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**block** | [**StandardTextListBlock**](StandardTextListBlock.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_header_text_list_block import StandardHeaderTextListBlock

# TODO update the JSON string below
json = "{}"
# create an instance of StandardHeaderTextListBlock from a JSON string
standard_header_text_list_block_instance = StandardHeaderTextListBlock.from_json(json)
# print the JSON string representation of the object
print(StandardHeaderTextListBlock.to_json())

# convert the object into a dict
standard_header_text_list_block_dict = standard_header_text_list_block_instance.to_dict()
# create an instance of StandardHeaderTextListBlock from a dict
standard_header_text_list_block_from_dict = StandardHeaderTextListBlock.from_dict(standard_header_text_list_block_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


