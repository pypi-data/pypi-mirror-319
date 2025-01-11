# GetQueriesResponse

The response for the `getQueries` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queries** | [**List[Query]**](Query.md) | A list of queries. | 
**pagination** | [**GetQueriesResponsePagination**](GetQueriesResponsePagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.dataKiosk_2023_11_15.models.get_queries_response import GetQueriesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetQueriesResponse from a JSON string
get_queries_response_instance = GetQueriesResponse.from_json(json)
# print the JSON string representation of the object
print(GetQueriesResponse.to_json())

# convert the object into a dict
get_queries_response_dict = get_queries_response_instance.to_dict()
# create an instance of GetQueriesResponse from a dict
get_queries_response_from_dict = GetQueriesResponse.from_dict(get_queries_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


