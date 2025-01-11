# ListFinancialEventGroupsResponse

The response schema for the listFinancialEventGroups operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ListFinancialEventGroupsPayload**](ListFinancialEventGroupsPayload.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.list_financial_event_groups_response import ListFinancialEventGroupsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListFinancialEventGroupsResponse from a JSON string
list_financial_event_groups_response_instance = ListFinancialEventGroupsResponse.from_json(json)
# print the JSON string representation of the object
print(ListFinancialEventGroupsResponse.to_json())

# convert the object into a dict
list_financial_event_groups_response_dict = list_financial_event_groups_response_instance.to_dict()
# create an instance of ListFinancialEventGroupsResponse from a dict
list_financial_event_groups_response_from_dict = ListFinancialEventGroupsResponse.from_dict(list_financial_event_groups_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


