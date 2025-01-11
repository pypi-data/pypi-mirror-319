# InboundPreferences

Preferences that can be passed in context of an inbound order

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**destination_region** | **str** | Pass a preferred region so that the inbound order can be shipped to an AWD warehouse located in that region. This doesn&#39;t guarantee the order to be assigned in the specified destination region as it depends on warehouse capacity availability. AWD currently supports following region IDs: [us-west, us-east] | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inbound_preferences import InboundPreferences

# TODO update the JSON string below
json = "{}"
# create an instance of InboundPreferences from a JSON string
inbound_preferences_instance = InboundPreferences.from_json(json)
# print the JSON string representation of the object
print(InboundPreferences.to_json())

# convert the object into a dict
inbound_preferences_dict = inbound_preferences_instance.to_dict()
# create an instance of InboundPreferences from a dict
inbound_preferences_from_dict = InboundPreferences.from_dict(inbound_preferences_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


