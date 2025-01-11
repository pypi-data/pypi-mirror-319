# Constraint

A validation constraint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**validation_reg_ex** | **str** | A regular expression. | [optional] 
**validation_string** | **str** | A validation string. | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.constraint import Constraint

# TODO update the JSON string below
json = "{}"
# create an instance of Constraint from a JSON string
constraint_instance = Constraint.from_json(json)
# print the JSON string representation of the object
print(Constraint.to_json())

# convert the object into a dict
constraint_dict = constraint_instance.to_dict()
# create an instance of Constraint from a dict
constraint_from_dict = Constraint.from_dict(constraint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


