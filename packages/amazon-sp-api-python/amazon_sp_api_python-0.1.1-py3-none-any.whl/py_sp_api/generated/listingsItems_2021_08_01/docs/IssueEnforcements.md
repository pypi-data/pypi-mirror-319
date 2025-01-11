# IssueEnforcements

This field provides information about the enforcement actions taken by Amazon that affect the publishing or status of a listing. It also includes details about any associated exemptions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**actions** | [**List[IssueEnforcementAction]**](IssueEnforcementAction.md) | List of enforcement actions taken by Amazon that affect the publishing or status of a listing. | 
**exemption** | [**IssueExemption**](IssueExemption.md) |  | 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.issue_enforcements import IssueEnforcements

# TODO update the JSON string below
json = "{}"
# create an instance of IssueEnforcements from a JSON string
issue_enforcements_instance = IssueEnforcements.from_json(json)
# print the JSON string representation of the object
print(IssueEnforcements.to_json())

# convert the object into a dict
issue_enforcements_dict = issue_enforcements_instance.to_dict()
# create an instance of IssueEnforcements from a dict
issue_enforcements_from_dict = IssueEnforcements.from_dict(issue_enforcements_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


