# TimeRangeContext

Additional information that is related to the time range of the transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **datetime** | A date in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**end_time** | **datetime** | A date in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.time_range_context import TimeRangeContext

# TODO update the JSON string below
json = "{}"
# create an instance of TimeRangeContext from a JSON string
time_range_context_instance = TimeRangeContext.from_json(json)
# print the JSON string representation of the object
print(TimeRangeContext.to_json())

# convert the object into a dict
time_range_context_dict = time_range_context_instance.to_dict()
# create an instance of TimeRangeContext from a dict
time_range_context_from_dict = TimeRangeContext.from_dict(time_range_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


