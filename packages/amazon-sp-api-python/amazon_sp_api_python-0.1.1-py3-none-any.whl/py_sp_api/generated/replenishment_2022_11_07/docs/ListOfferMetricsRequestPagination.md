# ListOfferMetricsRequestPagination

Use these parameters to paginate through the response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**limit** | **int** | The maximum number of results to return in the response. | 
**offset** | **int** | The offset from which to retrieve the number of results specified by the &#x60;limit&#x60; value. The first result is at offset 0. | 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offer_metrics_request_pagination import ListOfferMetricsRequestPagination

# TODO update the JSON string below
json = "{}"
# create an instance of ListOfferMetricsRequestPagination from a JSON string
list_offer_metrics_request_pagination_instance = ListOfferMetricsRequestPagination.from_json(json)
# print the JSON string representation of the object
print(ListOfferMetricsRequestPagination.to_json())

# convert the object into a dict
list_offer_metrics_request_pagination_dict = list_offer_metrics_request_pagination_instance.to_dict()
# create an instance of ListOfferMetricsRequestPagination from a dict
list_offer_metrics_request_pagination_from_dict = ListOfferMetricsRequestPagination.from_dict(list_offer_metrics_request_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


