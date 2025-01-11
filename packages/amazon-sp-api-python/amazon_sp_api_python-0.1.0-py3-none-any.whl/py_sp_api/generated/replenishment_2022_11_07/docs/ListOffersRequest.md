# ListOffersRequest

The request body for the `listOffers` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**ListOffersRequestPagination**](ListOffersRequestPagination.md) |  | 
**filters** | [**ListOffersRequestFilters**](ListOffersRequestFilters.md) |  | 
**sort** | [**ListOffersRequestSort**](ListOffersRequestSort.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offers_request import ListOffersRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListOffersRequest from a JSON string
list_offers_request_instance = ListOffersRequest.from_json(json)
# print the JSON string representation of the object
print(ListOffersRequest.to_json())

# convert the object into a dict
list_offers_request_dict = list_offers_request_instance.to_dict()
# create an instance of ListOffersRequest from a dict
list_offers_request_from_dict = ListOffersRequest.from_dict(list_offers_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


