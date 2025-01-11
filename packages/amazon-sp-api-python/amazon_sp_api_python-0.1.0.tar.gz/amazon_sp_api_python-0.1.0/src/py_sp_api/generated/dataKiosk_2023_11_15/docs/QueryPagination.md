# QueryPagination

When a query produces results that are not included in the data document, pagination occurs. This means the results are divided into pages. To retrieve the next page, you must pass a `CreateQuerySpecification` object with `paginationToken` set to this object's `nextToken` and with `query` set to this object's `query` in the subsequent `createQuery` request. When there are no more pages to fetch, the `nextToken` field will be absent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | A token that can be used to fetch the next page of results. | [optional] 

## Example

```python
from py_sp_api.generated.dataKiosk_2023_11_15.models.query_pagination import QueryPagination

# TODO update the JSON string below
json = "{}"
# create an instance of QueryPagination from a JSON string
query_pagination_instance = QueryPagination.from_json(json)
# print the JSON string representation of the object
print(QueryPagination.to_json())

# convert the object into a dict
query_pagination_dict = query_pagination_instance.to_dict()
# create an instance of QueryPagination from a dict
query_pagination_from_dict = QueryPagination.from_dict(query_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


