# GenerateOrderScenarioRequest

The request body for the generateOrderScenarios operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**orders** | [**List[OrderScenarioRequest]**](OrderScenarioRequest.md) | The list of test orders requested as indicated by party identifiers. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.generate_order_scenario_request import GenerateOrderScenarioRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateOrderScenarioRequest from a JSON string
generate_order_scenario_request_instance = GenerateOrderScenarioRequest.from_json(json)
# print the JSON string representation of the object
print(GenerateOrderScenarioRequest.to_json())

# convert the object into a dict
generate_order_scenario_request_dict = generate_order_scenario_request_instance.to_dict()
# create an instance of GenerateOrderScenarioRequest from a dict
generate_order_scenario_request_from_dict = GenerateOrderScenarioRequest.from_dict(generate_order_scenario_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


