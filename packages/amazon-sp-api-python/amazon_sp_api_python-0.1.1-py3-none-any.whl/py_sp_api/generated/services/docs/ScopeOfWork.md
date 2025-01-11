# ScopeOfWork

The scope of work for the order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the service job. | [optional] 
**title** | **str** | The title of the service job. | [optional] 
**quantity** | **int** | The number of service jobs. | [optional] 
**required_skills** | **List[str]** | A list of skills required to perform the job. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.scope_of_work import ScopeOfWork

# TODO update the JSON string below
json = "{}"
# create an instance of ScopeOfWork from a JSON string
scope_of_work_instance = ScopeOfWork.from_json(json)
# print the JSON string representation of the object
print(ScopeOfWork.to_json())

# convert the object into a dict
scope_of_work_dict = scope_of_work_instance.to_dict()
# create an instance of ScopeOfWork from a dict
scope_of_work_from_dict = ScopeOfWork.from_dict(scope_of_work_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


