# RentalTransactionEvent

An event related to a rental transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined identifier for an order. | [optional] 
**rental_event_type** | **str** | The type of rental event.  Possible values:  * RentalCustomerPayment-Buyout - Transaction type that represents when the customer wants to buy out a rented item.  * RentalCustomerPayment-Extension - Transaction type that represents when the customer wants to extend the rental period.  * RentalCustomerRefund-Buyout - Transaction type that represents when the customer requests a refund for the buyout of the rented item.  * RentalCustomerRefund-Extension - Transaction type that represents when the customer requests a refund over the extension on the rented item.  * RentalHandlingFee - Transaction type that represents the fee that Amazon charges sellers who rent through Amazon.  * RentalChargeFailureReimbursement - Transaction type that represents when Amazon sends money to the seller to compensate for a failed charge.  * RentalLostItemReimbursement - Transaction type that represents when Amazon sends money to the seller to compensate for a lost item. | [optional] 
**extension_length** | **int** | The number of days that the buyer extended an already rented item. This value is only returned for RentalCustomerPayment-Extension and RentalCustomerRefund-Extension events. | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**rental_charge_list** | [**List[ChargeComponent]**](ChargeComponent.md) | A list of charge information on the seller&#39;s account. | [optional] 
**rental_fee_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**marketplace_name** | **str** | The name of the marketplace. | [optional] 
**rental_initial_value** | [**Currency**](Currency.md) |  | [optional] 
**rental_reimbursement** | [**Currency**](Currency.md) |  | [optional] 
**rental_tax_withheld_list** | [**List[TaxWithheldComponent]**](TaxWithheldComponent.md) | A list of information about taxes withheld. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.rental_transaction_event import RentalTransactionEvent

# TODO update the JSON string below
json = "{}"
# create an instance of RentalTransactionEvent from a JSON string
rental_transaction_event_instance = RentalTransactionEvent.from_json(json)
# print the JSON string representation of the object
print(RentalTransactionEvent.to_json())

# convert the object into a dict
rental_transaction_event_dict = rental_transaction_event_instance.to_dict()
# create an instance of RentalTransactionEvent from a dict
rental_transaction_event_from_dict = RentalTransactionEvent.from_dict(rental_transaction_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


