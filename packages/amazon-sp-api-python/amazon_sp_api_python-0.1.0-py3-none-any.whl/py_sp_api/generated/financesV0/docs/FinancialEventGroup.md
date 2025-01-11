# FinancialEventGroup

Information related to a financial event group.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**financial_event_group_id** | **str** | A unique identifier for the financial event group. | [optional] 
**processing_status** | **str** | The processing status of the financial event group indicates whether the balance of the financial event group is settled.  Possible values:  * Open  * Closed | [optional] 
**fund_transfer_status** | **str** | The status of the fund transfer. | [optional] 
**original_total** | [**Currency**](Currency.md) |  | [optional] 
**converted_total** | [**Currency**](Currency.md) |  | [optional] 
**fund_transfer_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**trace_id** | **str** | The trace identifier used by sellers to look up transactions externally. | [optional] 
**account_tail** | **str** | The account tail of the payment instrument. | [optional] 
**beginning_balance** | [**Currency**](Currency.md) |  | [optional] 
**financial_event_group_start** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**financial_event_group_end** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.financial_event_group import FinancialEventGroup

# TODO update the JSON string below
json = "{}"
# create an instance of FinancialEventGroup from a JSON string
financial_event_group_instance = FinancialEventGroup.from_json(json)
# print the JSON string representation of the object
print(FinancialEventGroup.to_json())

# convert the object into a dict
financial_event_group_dict = financial_event_group_instance.to_dict()
# create an instance of FinancialEventGroup from a dict
financial_event_group_from_dict = FinancialEventGroup.from_dict(financial_event_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


