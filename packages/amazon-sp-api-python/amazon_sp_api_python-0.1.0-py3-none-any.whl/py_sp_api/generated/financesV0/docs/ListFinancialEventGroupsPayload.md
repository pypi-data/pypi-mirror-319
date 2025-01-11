# ListFinancialEventGroupsPayload

The payload for the listFinancialEventGroups operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | When present and not empty, pass this string token in the next request to return the next response page. | [optional] 
**financial_event_group_list** | [**List[FinancialEventGroup]**](FinancialEventGroup.md) | A list of financial event group information. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.list_financial_event_groups_payload import ListFinancialEventGroupsPayload

# TODO update the JSON string below
json = "{}"
# create an instance of ListFinancialEventGroupsPayload from a JSON string
list_financial_event_groups_payload_instance = ListFinancialEventGroupsPayload.from_json(json)
# print the JSON string representation of the object
print(ListFinancialEventGroupsPayload.to_json())

# convert the object into a dict
list_financial_event_groups_payload_dict = list_financial_event_groups_payload_instance.to_dict()
# create an instance of ListFinancialEventGroupsPayload from a dict
list_financial_event_groups_payload_from_dict = ListFinancialEventGroupsPayload.from_dict(list_financial_event_groups_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


