# TemporarilyUnavailableCarrier

A carrier who is temporarily unavailable, most likely due to a service outage experienced by the carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **str** | The name of the carrier. | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.temporarily_unavailable_carrier import TemporarilyUnavailableCarrier

# TODO update the JSON string below
json = "{}"
# create an instance of TemporarilyUnavailableCarrier from a JSON string
temporarily_unavailable_carrier_instance = TemporarilyUnavailableCarrier.from_json(json)
# print the JSON string representation of the object
print(TemporarilyUnavailableCarrier.to_json())

# convert the object into a dict
temporarily_unavailable_carrier_dict = temporarily_unavailable_carrier_instance.to_dict()
# create an instance of TemporarilyUnavailableCarrier from a dict
temporarily_unavailable_carrier_from_dict = TemporarilyUnavailableCarrier.from_dict(temporarily_unavailable_carrier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


