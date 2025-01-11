# ListOfferMetricsRequest

The request body for the `listOfferMetrics` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**ListOfferMetricsRequestPagination**](ListOfferMetricsRequestPagination.md) |  | 
**sort** | [**ListOfferMetricsRequestSort**](ListOfferMetricsRequestSort.md) |  | [optional] 
**filters** | [**ListOfferMetricsRequestFilters**](ListOfferMetricsRequestFilters.md) |  | 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offer_metrics_request import ListOfferMetricsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListOfferMetricsRequest from a JSON string
list_offer_metrics_request_instance = ListOfferMetricsRequest.from_json(json)
# print the JSON string representation of the object
print(ListOfferMetricsRequest.to_json())

# convert the object into a dict
list_offer_metrics_request_dict = list_offer_metrics_request_instance.to_dict()
# create an instance of ListOfferMetricsRequest from a dict
list_offer_metrics_request_from_dict = ListOfferMetricsRequest.from_dict(list_offer_metrics_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


