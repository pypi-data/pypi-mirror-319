# CreateQueryResponse

The response for the `createQuery` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query_id** | **str** | The identifier for the query. This identifier is unique only in combination with a selling partner account ID. | 

## Example

```python
from py_sp_api.generated.dataKiosk_2023_11_15.models.create_query_response import CreateQueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateQueryResponse from a JSON string
create_query_response_instance = CreateQueryResponse.from_json(json)
# print the JSON string representation of the object
print(CreateQueryResponse.to_json())

# convert the object into a dict
create_query_response_dict = create_query_response_instance.to_dict()
# create an instance of CreateQueryResponse from a dict
create_query_response_from_dict = CreateQueryResponse.from_dict(create_query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


