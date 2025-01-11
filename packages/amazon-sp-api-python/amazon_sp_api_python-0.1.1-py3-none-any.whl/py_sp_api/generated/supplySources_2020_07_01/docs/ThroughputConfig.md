# ThroughputConfig

The throughput configuration.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**throughput_cap** | [**ThroughputCap**](ThroughputCap.md) |  | [optional] 
**throughput_unit** | [**ThroughputUnit**](ThroughputUnit.md) |  | 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.throughput_config import ThroughputConfig

# TODO update the JSON string below
json = "{}"
# create an instance of ThroughputConfig from a JSON string
throughput_config_instance = ThroughputConfig.from_json(json)
# print the JSON string representation of the object
print(ThroughputConfig.to_json())

# convert the object into a dict
throughput_config_dict = throughput_config_instance.to_dict()
# create an instance of ThroughputConfig from a dict
throughput_config_from_dict = ThroughputConfig.from_dict(throughput_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


