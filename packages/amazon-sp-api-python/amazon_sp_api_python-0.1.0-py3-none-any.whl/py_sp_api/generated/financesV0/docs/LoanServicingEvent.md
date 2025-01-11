# LoanServicingEvent

A loan advance, loan payment, or loan refund.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loan_amount** | [**Currency**](Currency.md) |  | [optional] 
**source_business_event_type** | **str** | The type of event.  Possible values:  * LoanAdvance  * LoanPayment  * LoanRefund | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.loan_servicing_event import LoanServicingEvent

# TODO update the JSON string below
json = "{}"
# create an instance of LoanServicingEvent from a JSON string
loan_servicing_event_instance = LoanServicingEvent.from_json(json)
# print the JSON string representation of the object
print(LoanServicingEvent.to_json())

# convert the object into a dict
loan_servicing_event_dict = loan_servicing_event_instance.to_dict()
# create an instance of LoanServicingEvent from a dict
loan_servicing_event_from_dict = LoanServicingEvent.from_dict(loan_servicing_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


