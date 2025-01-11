# DebtRecoveryEvent

A debt payment or debt adjustment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**debt_recovery_type** | **str** | The debt recovery type.  Possible values:  * DebtPayment  * DebtPaymentFailure  * DebtAdjustment | [optional] 
**recovery_amount** | [**Currency**](Currency.md) |  | [optional] 
**over_payment_credit** | [**Currency**](Currency.md) |  | [optional] 
**debt_recovery_item_list** | [**List[DebtRecoveryItem]**](DebtRecoveryItem.md) | A list of debt recovery item information. | [optional] 
**charge_instrument_list** | [**List[ChargeInstrument]**](ChargeInstrument.md) | A list of payment instruments. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.debt_recovery_event import DebtRecoveryEvent

# TODO update the JSON string below
json = "{}"
# create an instance of DebtRecoveryEvent from a JSON string
debt_recovery_event_instance = DebtRecoveryEvent.from_json(json)
# print the JSON string representation of the object
print(DebtRecoveryEvent.to_json())

# convert the object into a dict
debt_recovery_event_dict = debt_recovery_event_instance.to_dict()
# create an instance of DebtRecoveryEvent from a dict
debt_recovery_event_from_dict = DebtRecoveryEvent.from_dict(debt_recovery_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


