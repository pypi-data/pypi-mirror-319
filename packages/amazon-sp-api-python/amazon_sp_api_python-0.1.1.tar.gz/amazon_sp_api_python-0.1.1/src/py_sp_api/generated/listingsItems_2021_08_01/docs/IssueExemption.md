# IssueExemption

Conveying the status of the listed enforcement actions and, if applicable, provides information about the exemption's expiry date.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | This field indicates the current exemption status for the listed enforcement actions. It can take values such as &#x60;EXEMPT&#x60;, signifying permanent exemption, &#x60;EXEMPT_UNTIL_EXPIRY_DATE&#x60; indicating temporary exemption until a specified date, or &#x60;NOT_EXEMPT&#x60; signifying no exemptions, and enforcement actions were already applied. | 
**expiry_date** | **datetime** | This field represents the timestamp, following the ISO 8601 format, which specifies the date when temporary exemptions, if applicable, will expire, and Amazon will begin enforcing the listed actions. | [optional] 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.issue_exemption import IssueExemption

# TODO update the JSON string below
json = "{}"
# create an instance of IssueExemption from a JSON string
issue_exemption_instance = IssueExemption.from_json(json)
# print the JSON string representation of the object
print(IssueExemption.to_json())

# convert the object into a dict
issue_exemption_dict = issue_exemption_instance.to_dict()
# create an instance of IssueExemption from a dict
issue_exemption_from_dict = IssueExemption.from_dict(issue_exemption_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


