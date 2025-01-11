# IssueEnforcementAction

The enforcement action taken by Amazon that affect the publishing or status of a listing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | The enforcement action name.   Possible values:   * &#x60;LISTING_SUPPRESSED&#x60; - This enforcement takes down the current listing item&#39;s buyability.   * &#x60;ATTRIBUTE_SUPPRESSED&#x60; - An attribute&#39;s value on the listing item is invalid, which causes it to be rejected by Amazon.   * &#x60;CATALOG_ITEM_REMOVED&#x60; - This catalog item is inactive on Amazon, and all offers against it in the applicable marketplace are non-buyable.   * &#x60;SEARCH_SUPPRESSED&#x60; - This value indicates that the catalog item is hidden from search results. | 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.issue_enforcement_action import IssueEnforcementAction

# TODO update the JSON string below
json = "{}"
# create an instance of IssueEnforcementAction from a JSON string
issue_enforcement_action_instance = IssueEnforcementAction.from_json(json)
# print the JSON string representation of the object
print(IssueEnforcementAction.to_json())

# convert the object into a dict
issue_enforcement_action_dict = issue_enforcement_action_instance.to_dict()
# create an instance of IssueEnforcementAction from a dict
issue_enforcement_action_from_dict = IssueEnforcementAction.from_dict(issue_enforcement_action_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


