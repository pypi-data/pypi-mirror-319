# AggregationSettings

A container that holds all of the necessary properties to configure the aggregation of notifications.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregation_time_period** | [**AggregationTimePeriod**](AggregationTimePeriod.md) |  | 

## Example

```python
from py_sp_api.generated.notifications.models.aggregation_settings import AggregationSettings

# TODO update the JSON string below
json = "{}"
# create an instance of AggregationSettings from a JSON string
aggregation_settings_instance = AggregationSettings.from_json(json)
# print the JSON string representation of the object
print(AggregationSettings.to_json())

# convert the object into a dict
aggregation_settings_dict = aggregation_settings_instance.to_dict()
# create an instance of AggregationSettings from a dict
aggregation_settings_from_dict = AggregationSettings.from_dict(aggregation_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


