# TestOrder

Error response returned when the request is unsuccessful.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | An error code that identifies the type of error that occurred. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.test_order import TestOrder

# TODO update the JSON string below
json = "{}"
# create an instance of TestOrder from a JSON string
test_order_instance = TestOrder.from_json(json)
# print the JSON string representation of the object
print(TestOrder.to_json())

# convert the object into a dict
test_order_dict = test_order_instance.to_dict()
# create an instance of TestOrder from a dict
test_order_from_dict = TestOrder.from_dict(test_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


