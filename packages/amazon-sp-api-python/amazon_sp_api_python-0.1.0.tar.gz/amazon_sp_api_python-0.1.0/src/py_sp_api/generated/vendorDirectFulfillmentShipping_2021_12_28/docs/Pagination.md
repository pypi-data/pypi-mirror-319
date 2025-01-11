# Pagination

The pagination elements required to retrieve the remaining data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | Pagination occurs when a request produces a response that exceeds the &#x60;pageSize&#x60;. This means that the response is divided into individual pages. To retrieve the next page or the previous page, you must pass the &#x60;nextToken&#x60; value or the &#x60;previousToken&#x60; value as the &#x60;pageToken&#x60; parameter in the next request. There is no &#x60;nextToken&#x60; in the pagination object on the last page. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.pagination import Pagination

# TODO update the JSON string below
json = "{}"
# create an instance of Pagination from a JSON string
pagination_instance = Pagination.from_json(json)
# print the JSON string representation of the object
print(Pagination.to_json())

# convert the object into a dict
pagination_dict = pagination_instance.to_dict()
# create an instance of Pagination from a dict
pagination_from_dict = Pagination.from_dict(pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


