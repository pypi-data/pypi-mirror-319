# AdhocDisbursementEvent

An event related to an Adhoc Disbursement.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_type** | **str** | Indicates the type of transaction.  Example: \&quot;Disbursed to Amazon Gift Card balance\&quot; | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**transaction_id** | **str** | The identifier for the transaction. | [optional] 
**transaction_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.adhoc_disbursement_event import AdhocDisbursementEvent

# TODO update the JSON string below
json = "{}"
# create an instance of AdhocDisbursementEvent from a JSON string
adhoc_disbursement_event_instance = AdhocDisbursementEvent.from_json(json)
# print the JSON string representation of the object
print(AdhocDisbursementEvent.to_json())

# convert the object into a dict
adhoc_disbursement_event_dict = adhoc_disbursement_event_instance.to_dict()
# create an instance of AdhocDisbursementEvent from a dict
adhoc_disbursement_event_from_dict = AdhocDisbursementEvent.from_dict(adhoc_disbursement_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


