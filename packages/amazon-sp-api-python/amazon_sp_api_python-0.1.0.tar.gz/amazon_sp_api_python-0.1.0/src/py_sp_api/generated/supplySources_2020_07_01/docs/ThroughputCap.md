# ThroughputCap

The throughput capacity

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **int** | An unsigned integer that can be only positive or zero. | [optional] 
**time_unit** | [**TimeUnit**](TimeUnit.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.throughput_cap import ThroughputCap

# TODO update the JSON string below
json = "{}"
# create an instance of ThroughputCap from a JSON string
throughput_cap_instance = ThroughputCap.from_json(json)
# print the JSON string representation of the object
print(ThroughputCap.to_json())

# convert the object into a dict
throughput_cap_dict = throughput_cap_instance.to_dict()
# create an instance of ThroughputCap from a dict
throughput_cap_from_dict = ThroughputCap.from_dict(throughput_cap_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


