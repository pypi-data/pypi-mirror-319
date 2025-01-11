# ListOfferMetricsRequestSort

Use these parameters to sort the response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order** | [**SortOrder**](SortOrder.md) |  | 
**key** | [**ListOfferMetricsSortKey**](ListOfferMetricsSortKey.md) |  | 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offer_metrics_request_sort import ListOfferMetricsRequestSort

# TODO update the JSON string below
json = "{}"
# create an instance of ListOfferMetricsRequestSort from a JSON string
list_offer_metrics_request_sort_instance = ListOfferMetricsRequestSort.from_json(json)
# print the JSON string representation of the object
print(ListOfferMetricsRequestSort.to_json())

# convert the object into a dict
list_offer_metrics_request_sort_dict = list_offer_metrics_request_sort_instance.to_dict()
# create an instance of ListOfferMetricsRequestSort from a dict
list_offer_metrics_request_sort_from_dict = ListOfferMetricsRequestSort.from_dict(list_offer_metrics_request_sort_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


