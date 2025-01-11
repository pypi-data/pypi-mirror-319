# OrderScenarioRequest

The party identifiers required to generate the test data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.order_scenario_request import OrderScenarioRequest

# TODO update the JSON string below
json = "{}"
# create an instance of OrderScenarioRequest from a JSON string
order_scenario_request_instance = OrderScenarioRequest.from_json(json)
# print the JSON string representation of the object
print(OrderScenarioRequest.to_json())

# convert the object into a dict
order_scenario_request_dict = order_scenario_request_instance.to_dict()
# create an instance of OrderScenarioRequest from a dict
order_scenario_request_from_dict = OrderScenarioRequest.from_dict(order_scenario_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


