# GetOrderMetricsResponse

The response schema for the getOrderMetrics operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[OrderMetricsInterval]**](OrderMetricsInterval.md) | A set of order metrics, each scoped to a particular time interval. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.sales.models.get_order_metrics_response import GetOrderMetricsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrderMetricsResponse from a JSON string
get_order_metrics_response_instance = GetOrderMetricsResponse.from_json(json)
# print the JSON string representation of the object
print(GetOrderMetricsResponse.to_json())

# convert the object into a dict
get_order_metrics_response_dict = get_order_metrics_response_instance.to_dict()
# create an instance of GetOrderMetricsResponse from a dict
get_order_metrics_response_from_dict = GetOrderMetricsResponse.from_dict(get_order_metrics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


