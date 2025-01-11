# ListFinancialEventsResponse

The response schema for the listFinancialEvents operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ListFinancialEventsPayload**](ListFinancialEventsPayload.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.list_financial_events_response import ListFinancialEventsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListFinancialEventsResponse from a JSON string
list_financial_events_response_instance = ListFinancialEventsResponse.from_json(json)
# print the JSON string representation of the object
print(ListFinancialEventsResponse.to_json())

# convert the object into a dict
list_financial_events_response_dict = list_financial_events_response_instance.to_dict()
# create an instance of ListFinancialEventsResponse from a dict
list_financial_events_response_from_dict = ListFinancialEventsResponse.from_dict(list_financial_events_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


