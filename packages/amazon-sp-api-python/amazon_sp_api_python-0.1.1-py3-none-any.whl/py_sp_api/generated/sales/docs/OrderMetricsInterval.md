# OrderMetricsInterval

Contains order metrics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**interval** | **str** | The interval of time based on requested granularity (ex. Hour, Day, etc.) If this is the first or the last interval from the list, it might contain incomplete data if the requested interval doesn&#39;t align with the requested granularity (ex. request interval 2018-09-01T02:00:00Z--2018-09-04T19:00:00Z and granularity day will result in Sept 1st UTC day and Sept 4th UTC days having partial data). | 
**unit_count** | **int** | The number of units in orders based on the specified filters. | 
**order_item_count** | **int** | The number of order items based on the specified filters. | 
**order_count** | **int** | The number of orders based on the specified filters. | 
**average_unit_price** | [**Money**](Money.md) |  | 
**total_sales** | [**Money**](Money.md) |  | 

## Example

```python
from py_sp_api.generated.sales.models.order_metrics_interval import OrderMetricsInterval

# TODO update the JSON string below
json = "{}"
# create an instance of OrderMetricsInterval from a JSON string
order_metrics_interval_instance = OrderMetricsInterval.from_json(json)
# print the JSON string representation of the object
print(OrderMetricsInterval.to_json())

# convert the object into a dict
order_metrics_interval_dict = order_metrics_interval_instance.to_dict()
# create an instance of OrderMetricsInterval from a dict
order_metrics_interval_from_dict = OrderMetricsInterval.from_dict(order_metrics_interval_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


