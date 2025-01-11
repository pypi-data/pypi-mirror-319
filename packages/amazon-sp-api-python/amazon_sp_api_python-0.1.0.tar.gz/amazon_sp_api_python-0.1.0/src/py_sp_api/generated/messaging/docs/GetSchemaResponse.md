# GetSchemaResponse

The `GET` request schema response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**links** | [**GetSchemaResponseLinks**](GetSchemaResponseLinks.md) |  | [optional] 
**payload** | **Dict[str, object]** | A JSON schema document describing the expected payload of the action. This object can be validated against &lt;a href&#x3D;http://json-schema.org/draft-04/schema&gt;http://json-schema.org/draft-04/schema&lt;/a&gt;. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.get_schema_response import GetSchemaResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSchemaResponse from a JSON string
get_schema_response_instance = GetSchemaResponse.from_json(json)
# print the JSON string representation of the object
print(GetSchemaResponse.to_json())

# convert the object into a dict
get_schema_response_dict = get_schema_response_instance.to_dict()
# create an instance of GetSchemaResponse from a dict
get_schema_response_from_dict = GetSchemaResponse.from_dict(get_schema_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


