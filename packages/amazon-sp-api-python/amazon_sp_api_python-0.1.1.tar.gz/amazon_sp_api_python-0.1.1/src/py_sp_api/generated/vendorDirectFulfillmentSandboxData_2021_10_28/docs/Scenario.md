# Scenario

A scenario test case response returned when the request is successful.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scenario_id** | **str** | An identifier that identifies the type of scenario that user can use for testing. | 
**orders** | [**List[TestOrder]**](TestOrder.md) | A list of orders that can be used by the caller to test each life cycle or scenario. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.scenario import Scenario

# TODO update the JSON string below
json = "{}"
# create an instance of Scenario from a JSON string
scenario_instance = Scenario.from_json(json)
# print the JSON string representation of the object
print(Scenario.to_json())

# convert the object into a dict
scenario_dict = scenario_instance.to_dict()
# create an instance of Scenario from a dict
scenario_from_dict = Scenario.from_dict(scenario_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


