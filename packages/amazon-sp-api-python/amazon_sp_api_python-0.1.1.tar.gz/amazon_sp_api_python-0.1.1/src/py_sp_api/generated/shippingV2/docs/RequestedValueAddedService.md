# RequestedValueAddedService

A value-added service to be applied to a shipping service purchase.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The identifier of the selected value-added service. Must be among those returned in the response to the getRates operation. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.requested_value_added_service import RequestedValueAddedService

# TODO update the JSON string below
json = "{}"
# create an instance of RequestedValueAddedService from a JSON string
requested_value_added_service_instance = RequestedValueAddedService.from_json(json)
# print the JSON string representation of the object
print(RequestedValueAddedService.to_json())

# convert the object into a dict
requested_value_added_service_dict = requested_value_added_service_instance.to_dict()
# create an instance of RequestedValueAddedService from a dict
requested_value_added_service_from_dict = RequestedValueAddedService.from_dict(requested_value_added_service_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


