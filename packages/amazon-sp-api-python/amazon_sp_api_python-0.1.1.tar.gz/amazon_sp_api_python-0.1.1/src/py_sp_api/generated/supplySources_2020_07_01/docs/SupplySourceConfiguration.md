# SupplySourceConfiguration

Includes configuration and timezone of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operational_configuration** | [**OperationalConfiguration**](OperationalConfiguration.md) |  | [optional] 
**timezone** | **str** | Please see RFC 6557, should be a canonical time zone ID as listed here: https://www.joda.org/joda-time/timezones.html. | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.supply_source_configuration import SupplySourceConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of SupplySourceConfiguration from a JSON string
supply_source_configuration_instance = SupplySourceConfiguration.from_json(json)
# print the JSON string representation of the object
print(SupplySourceConfiguration.to_json())

# convert the object into a dict
supply_source_configuration_dict = supply_source_configuration_instance.to_dict()
# create an instance of SupplySourceConfiguration from a dict
supply_source_configuration_from_dict = SupplySourceConfiguration.from_dict(supply_source_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


