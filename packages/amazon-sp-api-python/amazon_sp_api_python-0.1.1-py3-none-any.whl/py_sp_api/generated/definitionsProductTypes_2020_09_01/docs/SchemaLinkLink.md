# SchemaLinkLink

Link to retrieve the schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource** | **str** | URI resource for the link. | 
**verb** | **str** | HTTP method for the link operation. | 

## Example

```python
from py_sp_api.generated.definitionsProductTypes_2020_09_01.models.schema_link_link import SchemaLinkLink

# TODO update the JSON string below
json = "{}"
# create an instance of SchemaLinkLink from a JSON string
schema_link_link_instance = SchemaLinkLink.from_json(json)
# print the JSON string representation of the object
print(SchemaLinkLink.to_json())

# convert the object into a dict
schema_link_link_dict = schema_link_link_instance.to_dict()
# create an instance of SchemaLinkLink from a dict
schema_link_link_from_dict = SchemaLinkLink.from_dict(schema_link_link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


