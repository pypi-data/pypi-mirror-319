# ListFinancialEventsPayload

The payload for the listFinancialEvents operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | When present and not empty, pass this string token in the next request to return the next response page. | [optional] 
**financial_events** | [**FinancialEvents**](FinancialEvents.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.list_financial_events_payload import ListFinancialEventsPayload

# TODO update the JSON string below
json = "{}"
# create an instance of ListFinancialEventsPayload from a JSON string
list_financial_events_payload_instance = ListFinancialEventsPayload.from_json(json)
# print the JSON string representation of the object
print(ListFinancialEventsPayload.to_json())

# convert the object into a dict
list_financial_events_payload_dict = list_financial_events_payload_instance.to_dict()
# create an instance of ListFinancialEventsPayload from a dict
list_financial_events_payload_from_dict = ListFinancialEventsPayload.from_dict(list_financial_events_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


