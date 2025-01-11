# TestCaseData

The set of test case data returned in response to the test data request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scenarios** | [**List[Scenario]**](Scenario.md) | Set of use cases that describes the possible test scenarios. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.test_case_data import TestCaseData

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseData from a JSON string
test_case_data_instance = TestCaseData.from_json(json)
# print the JSON string representation of the object
print(TestCaseData.to_json())

# convert the object into a dict
test_case_data_dict = test_case_data_instance.to_dict()
# create an instance of TestCaseData from a dict
test_case_data_from_dict = TestCaseData.from_dict(test_case_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


