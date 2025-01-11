# GetSellingPartnerMetricsResponse

The response schema for the `getSellingPartnerMetrics` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metrics** | [**List[GetSellingPartnerMetricsResponseMetric]**](GetSellingPartnerMetricsResponseMetric.md) | A list of metrics data for the selling partner. | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.get_selling_partner_metrics_response import GetSellingPartnerMetricsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSellingPartnerMetricsResponse from a JSON string
get_selling_partner_metrics_response_instance = GetSellingPartnerMetricsResponse.from_json(json)
# print the JSON string representation of the object
print(GetSellingPartnerMetricsResponse.to_json())

# convert the object into a dict
get_selling_partner_metrics_response_dict = get_selling_partner_metrics_response_instance.to_dict()
# create an instance of GetSellingPartnerMetricsResponse from a dict
get_selling_partner_metrics_response_from_dict = GetSellingPartnerMetricsResponse.from_dict(get_selling_partner_metrics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


