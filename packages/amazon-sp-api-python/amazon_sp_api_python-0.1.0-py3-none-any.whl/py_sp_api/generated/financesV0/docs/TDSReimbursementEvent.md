# TDSReimbursementEvent

An event related to a Tax-Deducted-at-Source (TDS) reimbursement.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**tds_order_id** | **str** | The Tax-Deducted-at-Source (TDS) identifier. | [optional] 
**reimbursed_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.tds_reimbursement_event import TDSReimbursementEvent

# TODO update the JSON string below
json = "{}"
# create an instance of TDSReimbursementEvent from a JSON string
tds_reimbursement_event_instance = TDSReimbursementEvent.from_json(json)
# print the JSON string representation of the object
print(TDSReimbursementEvent.to_json())

# convert the object into a dict
tds_reimbursement_event_dict = tds_reimbursement_event_instance.to_dict()
# create an instance of TDSReimbursementEvent from a dict
tds_reimbursement_event_from_dict = TDSReimbursementEvent.from_dict(tds_reimbursement_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


