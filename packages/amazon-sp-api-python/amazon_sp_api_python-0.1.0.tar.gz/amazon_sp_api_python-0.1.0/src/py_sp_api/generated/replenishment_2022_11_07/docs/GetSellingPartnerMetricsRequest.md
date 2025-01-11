# GetSellingPartnerMetricsRequest

The request body for the `getSellingPartnerMetrics` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregation_frequency** | [**AggregationFrequency**](AggregationFrequency.md) |  | [optional] 
**time_interval** | [**TimeInterval**](TimeInterval.md) |  | 
**metrics** | [**List[Metric]**](Metric.md) | The list of metrics requested. If no metric value is provided, data for all of the metrics will be returned. | [optional] 
**time_period_type** | [**TimePeriodType**](TimePeriodType.md) |  | 
**marketplace_id** | **str** | The marketplace identifier. The supported marketplaces for both sellers and vendors are US, CA, ES, UK, FR, IT, IN, DE and JP. The supported marketplaces for vendors only are BR, AU, MX, AE and NL. Refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) to find the identifier for the marketplace. | 
**program_types** | [**List[ProgramType]**](ProgramType.md) | A list of replenishment program types. | 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.get_selling_partner_metrics_request import GetSellingPartnerMetricsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetSellingPartnerMetricsRequest from a JSON string
get_selling_partner_metrics_request_instance = GetSellingPartnerMetricsRequest.from_json(json)
# print the JSON string representation of the object
print(GetSellingPartnerMetricsRequest.to_json())

# convert the object into a dict
get_selling_partner_metrics_request_dict = get_selling_partner_metrics_request_instance.to_dict()
# create an instance of GetSellingPartnerMetricsRequest from a dict
get_selling_partner_metrics_request_from_dict = GetSellingPartnerMetricsRequest.from_dict(get_selling_partner_metrics_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


