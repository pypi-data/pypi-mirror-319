# ServiceSelection

Service Selection Criteria.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_id** | **List[str]** | A list of ServiceId. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.service_selection import ServiceSelection

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceSelection from a JSON string
service_selection_instance = ServiceSelection.from_json(json)
# print the JSON string representation of the object
print(ServiceSelection.to_json())

# convert the object into a dict
service_selection_dict = service_selection_instance.to_dict()
# create an instance of ServiceSelection from a dict
service_selection_from_dict = ServiceSelection.from_dict(service_selection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


