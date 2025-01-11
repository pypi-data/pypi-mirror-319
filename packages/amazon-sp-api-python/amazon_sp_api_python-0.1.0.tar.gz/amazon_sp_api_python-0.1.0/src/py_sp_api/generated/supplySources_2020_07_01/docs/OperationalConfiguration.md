# OperationalConfiguration

The operational configuration of `supplySources`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contact_details** | [**ContactDetails**](ContactDetails.md) |  | [optional] 
**throughput_config** | [**ThroughputConfig**](ThroughputConfig.md) |  | [optional] 
**operating_hours_by_day** | [**OperatingHoursByDay**](OperatingHoursByDay.md) |  | [optional] 
**handling_time** | [**Duration**](Duration.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.operational_configuration import OperationalConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of OperationalConfiguration from a JSON string
operational_configuration_instance = OperationalConfiguration.from_json(json)
# print the JSON string representation of the object
print(OperationalConfiguration.to_json())

# convert the object into a dict
operational_configuration_dict = operational_configuration_instance.to_dict()
# create an instance of OperationalConfiguration from a dict
operational_configuration_from_dict = OperationalConfiguration.from_dict(operational_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


