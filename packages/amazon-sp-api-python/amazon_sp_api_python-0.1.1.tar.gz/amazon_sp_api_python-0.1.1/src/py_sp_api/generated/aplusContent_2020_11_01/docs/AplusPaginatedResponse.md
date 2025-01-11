# AplusPaginatedResponse

The base response data for paginated A+ Content operations. Individual operations may extend this with additional data. If nextPageToken is not returned, there are no more pages to return.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 
**next_page_token** | **str** | A page token that is returned when the results of the call exceed the page size. To get another page of results, call the operation again, passing in this value with the pageToken parameter. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.aplus_paginated_response import AplusPaginatedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AplusPaginatedResponse from a JSON string
aplus_paginated_response_instance = AplusPaginatedResponse.from_json(json)
# print the JSON string representation of the object
print(AplusPaginatedResponse.to_json())

# convert the object into a dict
aplus_paginated_response_dict = aplus_paginated_response_instance.to_dict()
# create an instance of AplusPaginatedResponse from a dict
aplus_paginated_response_from_dict = AplusPaginatedResponse.from_dict(aplus_paginated_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


