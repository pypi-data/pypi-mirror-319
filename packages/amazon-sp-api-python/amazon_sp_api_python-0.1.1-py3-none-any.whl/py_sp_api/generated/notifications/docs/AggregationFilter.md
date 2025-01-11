# AggregationFilter

A filter used to select the aggregation time period at which to send notifications (for example: limit to one notification every five minutes for high frequency notifications).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregation_settings** | [**AggregationSettings**](AggregationSettings.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.aggregation_filter import AggregationFilter

# TODO update the JSON string below
json = "{}"
# create an instance of AggregationFilter from a JSON string
aggregation_filter_instance = AggregationFilter.from_json(json)
# print the JSON string representation of the object
print(AggregationFilter.to_json())

# convert the object into a dict
aggregation_filter_dict = aggregation_filter_instance.to_dict()
# create an instance of AggregationFilter from a dict
aggregation_filter_from_dict = AggregationFilter.from_dict(aggregation_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


