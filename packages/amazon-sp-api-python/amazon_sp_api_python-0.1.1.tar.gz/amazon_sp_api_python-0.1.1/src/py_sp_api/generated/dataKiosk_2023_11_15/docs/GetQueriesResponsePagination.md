# GetQueriesResponsePagination

When a request has results that are not included in this response, pagination occurs. This means the results are divided into pages. To retrieve the next page, you must pass the `nextToken` as the `paginationToken` query parameter in the subsequent `getQueries` request. All other parameters must be provided with the same values that were provided with the request that generated this token, with the exception of `pageSize` which can be modified between calls to `getQueries`. When there are no more pages to fetch, the `nextToken` field will be absent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | A token that can be used to fetch the next page of results. | [optional] 

## Example

```python
from py_sp_api.generated.dataKiosk_2023_11_15.models.get_queries_response_pagination import GetQueriesResponsePagination

# TODO update the JSON string below
json = "{}"
# create an instance of GetQueriesResponsePagination from a JSON string
get_queries_response_pagination_instance = GetQueriesResponsePagination.from_json(json)
# print the JSON string representation of the object
print(GetQueriesResponsePagination.to_json())

# convert the object into a dict
get_queries_response_pagination_dict = get_queries_response_pagination_instance.to_dict()
# create an instance of GetQueriesResponsePagination from a dict
get_queries_response_pagination_from_dict = GetQueriesResponsePagination.from_dict(get_queries_response_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


