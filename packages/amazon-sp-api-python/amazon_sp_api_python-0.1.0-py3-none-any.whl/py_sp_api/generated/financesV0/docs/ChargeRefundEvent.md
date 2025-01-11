# ChargeRefundEvent

An event related to charge refund.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**reason_code** | **str** | The reason given for a charge refund.  Example: &#x60;SubscriptionFeeCorrection&#x60; | [optional] 
**reason_code_description** | **str** | A description of the Reason Code.   Example: &#x60;SubscriptionFeeCorrection&#x60; | [optional] 
**charge_refund_transactions** | [**List[ChargeRefundTransaction]**](ChargeRefundTransaction.md) | A list of &#x60;ChargeRefund&#x60; transactions | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.charge_refund_event import ChargeRefundEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ChargeRefundEvent from a JSON string
charge_refund_event_instance = ChargeRefundEvent.from_json(json)
# print the JSON string representation of the object
print(ChargeRefundEvent.to_json())

# convert the object into a dict
charge_refund_event_dict = charge_refund_event_instance.to_dict()
# create an instance of ChargeRefundEvent from a dict
charge_refund_event_from_dict = ChargeRefundEvent.from_dict(charge_refund_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


