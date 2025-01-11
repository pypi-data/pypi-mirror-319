# RegulatedInformation

The regulated information collected during purchase and used to verify the order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fields** | [**List[RegulatedInformationField]**](RegulatedInformationField.md) | A list of regulated information fields as collected from the regulatory form. | 

## Example

```python
from py_sp_api.generated.ordersV0.models.regulated_information import RegulatedInformation

# TODO update the JSON string below
json = "{}"
# create an instance of RegulatedInformation from a JSON string
regulated_information_instance = RegulatedInformation.from_json(json)
# print the JSON string representation of the object
print(RegulatedInformation.to_json())

# convert the object into a dict
regulated_information_dict = regulated_information_instance.to_dict()
# create an instance of RegulatedInformation from a dict
regulated_information_from_dict = RegulatedInformation.from_dict(regulated_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


