# SchemaLink


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**link** | [**SchemaLinkLink**](SchemaLinkLink.md) |  | 
**checksum** | **str** | Checksum hash of the schema (Base64 MD5). Can be used to verify schema contents, identify changes between schema versions, and for caching. | 

## Example

```python
from py_sp_api.generated.definitionsProductTypes_2020_09_01.models.schema_link import SchemaLink

# TODO update the JSON string below
json = "{}"
# create an instance of SchemaLink from a JSON string
schema_link_instance = SchemaLink.from_json(json)
# print the JSON string representation of the object
print(SchemaLink.to_json())

# convert the object into a dict
schema_link_dict = schema_link_instance.to_dict()
# create an instance of SchemaLink from a dict
schema_link_from_dict = SchemaLink.from_dict(schema_link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


