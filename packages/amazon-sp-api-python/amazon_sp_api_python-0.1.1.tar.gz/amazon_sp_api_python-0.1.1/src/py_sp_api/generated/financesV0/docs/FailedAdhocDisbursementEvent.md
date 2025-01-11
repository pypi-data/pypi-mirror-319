# FailedAdhocDisbursementEvent

Failed ad hoc disbursement event list.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**funds_transfers_type** | **str** | The type of fund transfer.   Example \&quot;Refund\&quot; | [optional] 
**transfer_id** | **str** | The transfer identifier. | [optional] 
**disbursement_id** | **str** | The disbursement identifier. | [optional] 
**payment_disbursement_type** | **str** | The type of payment for disbursement.   Example &#x60;CREDIT_CARD&#x60; | [optional] 
**status** | **str** | The status of the failed &#x60;AdhocDisbursement&#x60;.   Example &#x60;HARD_DECLINED&#x60; | [optional] 
**transfer_amount** | [**Currency**](Currency.md) |  | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.failed_adhoc_disbursement_event import FailedAdhocDisbursementEvent

# TODO update the JSON string below
json = "{}"
# create an instance of FailedAdhocDisbursementEvent from a JSON string
failed_adhoc_disbursement_event_instance = FailedAdhocDisbursementEvent.from_json(json)
# print the JSON string representation of the object
print(FailedAdhocDisbursementEvent.to_json())

# convert the object into a dict
failed_adhoc_disbursement_event_dict = failed_adhoc_disbursement_event_instance.to_dict()
# create an instance of FailedAdhocDisbursementEvent from a dict
failed_adhoc_disbursement_event_from_dict = FailedAdhocDisbursementEvent.from_dict(failed_adhoc_disbursement_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


