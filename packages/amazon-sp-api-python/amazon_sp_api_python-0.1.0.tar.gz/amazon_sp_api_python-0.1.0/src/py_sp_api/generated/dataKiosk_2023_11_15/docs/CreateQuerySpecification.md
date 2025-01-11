# CreateQuerySpecification

Information required to create the query.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query** | **str** | The GraphQL query to submit. A query must be at most 8000 characters after unnecessary whitespace is removed. | 
**pagination_token** | **str** | A token to fetch a certain page of query results when there are multiple pages of query results available. The value of this token must be fetched from the &#x60;pagination.nextToken&#x60; field of the &#x60;Query&#x60; object, and the &#x60;query&#x60; field for this object must also be set to the &#x60;query&#x60; field of the same &#x60;Query&#x60; object. A &#x60;Query&#x60; object can be retrieved from either the &#x60;getQueries&#x60; or &#x60;getQuery&#x60; operation. In the absence of this token value, the first page of query results will be requested. | [optional] 

## Example

```python
from py_sp_api.generated.dataKiosk_2023_11_15.models.create_query_specification import CreateQuerySpecification

# TODO update the JSON string below
json = "{}"
# create an instance of CreateQuerySpecification from a JSON string
create_query_specification_instance = CreateQuerySpecification.from_json(json)
# print the JSON string representation of the object
print(CreateQuerySpecification.to_json())

# convert the object into a dict
create_query_specification_dict = create_query_specification_instance.to_dict()
# create an instance of CreateQuerySpecification from a dict
create_query_specification_from_dict = CreateQuerySpecification.from_dict(create_query_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


