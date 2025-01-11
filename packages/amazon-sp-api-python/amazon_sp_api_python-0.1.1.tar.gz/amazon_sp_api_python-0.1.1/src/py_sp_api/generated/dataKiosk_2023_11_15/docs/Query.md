# Query

Detailed information about the query.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query_id** | **str** | The query identifier. This identifier is unique only in combination with a selling partner account ID. | 
**query** | **str** | The submitted query. | 
**created_time** | **datetime** | The date and time when the query was created, in ISO 8601 date time format. | 
**processing_status** | **str** | The processing status of the query. | 
**processing_start_time** | **datetime** | The date and time when the query processing started, in ISO 8601 date time format. | [optional] 
**processing_end_time** | **datetime** | The date and time when the query processing completed, in ISO 8601 date time format. | [optional] 
**data_document_id** | **str** | The data document identifier. This identifier is only present when there is data available as a result of the query. This identifier is unique only in combination with a selling partner account ID. Pass this identifier into the &#x60;getDocument&#x60; operation to get the information required to retrieve the data document&#39;s contents. | [optional] 
**error_document_id** | **str** | The error document identifier. This identifier is only present when an error occurs during query processing. This identifier is unique only in combination with a selling partner account ID. Pass this identifier into the &#x60;getDocument&#x60; operation to get the information required to retrieve the error document&#39;s contents. | [optional] 
**pagination** | [**QueryPagination**](QueryPagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.dataKiosk_2023_11_15.models.query import Query

# TODO update the JSON string below
json = "{}"
# create an instance of Query from a JSON string
query_instance = Query.from_json(json)
# print the JSON string representation of the object
print(Query.to_json())

# convert the object into a dict
query_dict = query_instance.to_dict()
# create an instance of Query from a dict
query_from_dict = Query.from_dict(query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


