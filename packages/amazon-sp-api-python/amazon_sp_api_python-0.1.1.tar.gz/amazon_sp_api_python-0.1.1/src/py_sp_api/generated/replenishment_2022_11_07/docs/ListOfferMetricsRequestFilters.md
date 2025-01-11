# ListOfferMetricsRequestFilters

Use these parameters to filter results. Any result must match all provided parameters. For any parameter that is an array, the result must match at least one element in the provided array.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregation_frequency** | [**AggregationFrequency**](AggregationFrequency.md) |  | [optional] 
**time_interval** | [**TimeInterval**](TimeInterval.md) |  | 
**time_period_type** | [**TimePeriodType**](TimePeriodType.md) |  | 
**marketplace_id** | **str** | The marketplace identifier. The supported marketplaces for both sellers and vendors are US, CA, ES, UK, FR, IT, IN, DE and JP. The supported marketplaces for vendors only are BR, AU, MX, AE and NL. Refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) to find the identifier for the marketplace. | 
**program_types** | [**List[ProgramType]**](ProgramType.md) | A list of replenishment program types. | 
**asins** | **List[str]** | A list of Amazon Standard Identification Numbers (ASINs). | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offer_metrics_request_filters import ListOfferMetricsRequestFilters

# TODO update the JSON string below
json = "{}"
# create an instance of ListOfferMetricsRequestFilters from a JSON string
list_offer_metrics_request_filters_instance = ListOfferMetricsRequestFilters.from_json(json)
# print the JSON string representation of the object
print(ListOfferMetricsRequestFilters.to_json())

# convert the object into a dict
list_offer_metrics_request_filters_dict = list_offer_metrics_request_filters_instance.to_dict()
# create an instance of ListOfferMetricsRequestFilters from a dict
list_offer_metrics_request_filters_from_dict = ListOfferMetricsRequestFilters.from_dict(list_offer_metrics_request_filters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


