# ListOffersRequestSort

Use these parameters to sort the response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order** | [**SortOrder**](SortOrder.md) |  | 
**key** | [**ListOffersSortKey**](ListOffersSortKey.md) |  | 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offers_request_sort import ListOffersRequestSort

# TODO update the JSON string below
json = "{}"
# create an instance of ListOffersRequestSort from a JSON string
list_offers_request_sort_instance = ListOffersRequestSort.from_json(json)
# print the JSON string representation of the object
print(ListOffersRequestSort.to_json())

# convert the object into a dict
list_offers_request_sort_dict = list_offers_request_sort_instance.to_dict()
# create an instance of ListOffersRequestSort from a dict
list_offers_request_sort_from_dict = ListOffersRequestSort.from_dict(list_offers_request_sort_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


