# ListOffersResponse

The response schema for the `listOffers` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**offers** | [**List[ListOffersResponseOffer]**](ListOffersResponseOffer.md) | A list of offers. | [optional] 
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offers_response import ListOffersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListOffersResponse from a JSON string
list_offers_response_instance = ListOffersResponse.from_json(json)
# print the JSON string representation of the object
print(ListOffersResponse.to_json())

# convert the object into a dict
list_offers_response_dict = list_offers_response_instance.to_dict()
# create an instance of ListOffersResponse from a dict
list_offers_response_from_dict = ListOffersResponse.from_dict(list_offers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


