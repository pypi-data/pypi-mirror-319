# SearchContentPublishRecordsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 
**next_page_token** | **str** | A page token that is returned when the results of the call exceed the page size. To get another page of results, call the operation again, passing in this value with the pageToken parameter. | [optional] 
**publish_record_list** | [**List[PublishRecord]**](PublishRecord.md) | A list of A+ Content publishing records. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.search_content_publish_records_response import SearchContentPublishRecordsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SearchContentPublishRecordsResponse from a JSON string
search_content_publish_records_response_instance = SearchContentPublishRecordsResponse.from_json(json)
# print the JSON string representation of the object
print(SearchContentPublishRecordsResponse.to_json())

# convert the object into a dict
search_content_publish_records_response_dict = search_content_publish_records_response_instance.to_dict()
# create an instance of SearchContentPublishRecordsResponse from a dict
search_content_publish_records_response_from_dict = SearchContentPublishRecordsResponse.from_dict(search_content_publish_records_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


