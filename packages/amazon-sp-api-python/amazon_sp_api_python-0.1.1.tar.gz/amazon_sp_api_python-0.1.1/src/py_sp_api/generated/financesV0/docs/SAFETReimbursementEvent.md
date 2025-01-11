# SAFETReimbursementEvent

A SAFE-T claim reimbursement on the seller's account.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**safet_claim_id** | **str** | A SAFE-T claim identifier. | [optional] 
**reimbursed_amount** | [**Currency**](Currency.md) |  | [optional] 
**reason_code** | **str** | Indicates why the seller was reimbursed. | [optional] 
**safet_reimbursement_item_list** | [**List[SAFETReimbursementItem]**](SAFETReimbursementItem.md) | A list of SAFETReimbursementItems. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.safet_reimbursement_event import SAFETReimbursementEvent

# TODO update the JSON string below
json = "{}"
# create an instance of SAFETReimbursementEvent from a JSON string
safet_reimbursement_event_instance = SAFETReimbursementEvent.from_json(json)
# print the JSON string representation of the object
print(SAFETReimbursementEvent.to_json())

# convert the object into a dict
safet_reimbursement_event_dict = safet_reimbursement_event_instance.to_dict()
# create an instance of SAFETReimbursementEvent from a dict
safet_reimbursement_event_from_dict = SAFETReimbursementEvent.from_dict(safet_reimbursement_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


