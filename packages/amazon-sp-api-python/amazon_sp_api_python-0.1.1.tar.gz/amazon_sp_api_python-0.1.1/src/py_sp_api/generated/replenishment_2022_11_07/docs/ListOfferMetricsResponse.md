# ListOfferMetricsResponse

The response schema for the `listOfferMetrics` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**offers** | [**List[ListOfferMetricsResponseOffer]**](ListOfferMetricsResponseOffer.md) | A list of offers and associated metrics. | [optional] 
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offer_metrics_response import ListOfferMetricsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListOfferMetricsResponse from a JSON string
list_offer_metrics_response_instance = ListOfferMetricsResponse.from_json(json)
# print the JSON string representation of the object
print(ListOfferMetricsResponse.to_json())

# convert the object into a dict
list_offer_metrics_response_dict = list_offer_metrics_response_instance.to_dict()
# create an instance of ListOfferMetricsResponse from a dict
list_offer_metrics_response_from_dict = ListOfferMetricsResponse.from_dict(list_offer_metrics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


