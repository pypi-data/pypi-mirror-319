# FinancialEvents

Contains all information related to a financial event.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_event_list** | [**List[ShipmentEvent]**](ShipmentEvent.md) | A list of shipment event information. | [optional] 
**shipment_settle_event_list** | [**List[ShipmentEvent]**](ShipmentEvent.md) | A list of &#x60;ShipmentEvent&#x60; items. | [optional] 
**refund_event_list** | [**List[ShipmentEvent]**](ShipmentEvent.md) | A list of shipment event information. | [optional] 
**guarantee_claim_event_list** | [**List[ShipmentEvent]**](ShipmentEvent.md) | A list of shipment event information. | [optional] 
**chargeback_event_list** | [**List[ShipmentEvent]**](ShipmentEvent.md) | A list of shipment event information. | [optional] 
**pay_with_amazon_event_list** | [**List[PayWithAmazonEvent]**](PayWithAmazonEvent.md) | A list of events related to the seller&#39;s Pay with Amazon account. | [optional] 
**service_provider_credit_event_list** | [**List[SolutionProviderCreditEvent]**](SolutionProviderCreditEvent.md) | A list of information about solution provider credits. | [optional] 
**retrocharge_event_list** | [**List[RetrochargeEvent]**](RetrochargeEvent.md) | A list of information about Retrocharge or RetrochargeReversal events. | [optional] 
**rental_transaction_event_list** | [**List[RentalTransactionEvent]**](RentalTransactionEvent.md) | A list of rental transaction event information. | [optional] 
**product_ads_payment_event_list** | [**List[ProductAdsPaymentEvent]**](ProductAdsPaymentEvent.md) | A list of sponsored products payment events. | [optional] 
**service_fee_event_list** | [**List[ServiceFeeEvent]**](ServiceFeeEvent.md) | A list of information about service fee events. | [optional] 
**seller_deal_payment_event_list** | [**List[SellerDealPaymentEvent]**](SellerDealPaymentEvent.md) | A list of payment events for deal-related fees. | [optional] 
**debt_recovery_event_list** | [**List[DebtRecoveryEvent]**](DebtRecoveryEvent.md) | A list of debt recovery event information. | [optional] 
**loan_servicing_event_list** | [**List[LoanServicingEvent]**](LoanServicingEvent.md) | A list of loan servicing events. | [optional] 
**adjustment_event_list** | [**List[AdjustmentEvent]**](AdjustmentEvent.md) | A list of adjustment event information for the seller&#39;s account. | [optional] 
**safet_reimbursement_event_list** | [**List[SAFETReimbursementEvent]**](SAFETReimbursementEvent.md) | A list of SAFETReimbursementEvents. | [optional] 
**seller_review_enrollment_payment_event_list** | [**List[SellerReviewEnrollmentPaymentEvent]**](SellerReviewEnrollmentPaymentEvent.md) | A list of information about fee events for the Early Reviewer Program. | [optional] 
**fba_liquidation_event_list** | [**List[FBALiquidationEvent]**](FBALiquidationEvent.md) | A list of FBA inventory liquidation payment events. | [optional] 
**coupon_payment_event_list** | [**List[CouponPaymentEvent]**](CouponPaymentEvent.md) | A list of coupon payment event information. | [optional] 
**imaging_services_fee_event_list** | [**List[ImagingServicesFeeEvent]**](ImagingServicesFeeEvent.md) | A list of fee events related to Amazon Imaging services. | [optional] 
**network_commingling_transaction_event_list** | [**List[NetworkComminglingTransactionEvent]**](NetworkComminglingTransactionEvent.md) | A list of network commingling transaction events. | [optional] 
**affordability_expense_event_list** | [**List[AffordabilityExpenseEvent]**](AffordabilityExpenseEvent.md) | A list of expense information related to an affordability promotion. | [optional] 
**affordability_expense_reversal_event_list** | [**List[AffordabilityExpenseEvent]**](AffordabilityExpenseEvent.md) | A list of expense information related to an affordability promotion. | [optional] 
**removal_shipment_event_list** | [**List[RemovalShipmentEvent]**](RemovalShipmentEvent.md) | A list of removal shipment event information. | [optional] 
**removal_shipment_adjustment_event_list** | [**List[RemovalShipmentAdjustmentEvent]**](RemovalShipmentAdjustmentEvent.md) | A comma-delimited list of Removal shipmentAdjustment details for FBA inventory. | [optional] 
**trial_shipment_event_list** | [**List[TrialShipmentEvent]**](TrialShipmentEvent.md) | A list of information about trial shipment financial events. | [optional] 
**tds_reimbursement_event_list** | [**List[TDSReimbursementEvent]**](TDSReimbursementEvent.md) | A list of &#x60;TDSReimbursementEvent&#x60; items. | [optional] 
**adhoc_disbursement_event_list** | [**List[AdhocDisbursementEvent]**](AdhocDisbursementEvent.md) | A list of &#x60;AdhocDisbursement&#x60; events. | [optional] 
**tax_withholding_event_list** | [**List[TaxWithholdingEvent]**](TaxWithholdingEvent.md) | A list of &#x60;TaxWithholding&#x60; events. | [optional] 
**charge_refund_event_list** | [**List[ChargeRefundEvent]**](ChargeRefundEvent.md) | A list of charge refund events. | [optional] 
**failed_adhoc_disbursement_event_list** | [**List[FailedAdhocDisbursementEvent]**](FailedAdhocDisbursementEvent.md) | A list of &#x60;FailedAdhocDisbursementEvent&#x60;s. | [optional] 
**value_added_service_charge_event_list** | [**List[ValueAddedServiceChargeEvent]**](ValueAddedServiceChargeEvent.md) | A list of &#x60;ValueAddedServiceCharge&#x60; events. | [optional] 
**capacity_reservation_billing_event_list** | [**List[CapacityReservationBillingEvent]**](CapacityReservationBillingEvent.md) | A list of &#x60;CapacityReservationBillingEvent&#x60; events. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.financial_events import FinancialEvents

# TODO update the JSON string below
json = "{}"
# create an instance of FinancialEvents from a JSON string
financial_events_instance = FinancialEvents.from_json(json)
# print the JSON string representation of the object
print(FinancialEvents.to_json())

# convert the object into a dict
financial_events_dict = financial_events_instance.to_dict()
# create an instance of FinancialEvents from a dict
financial_events_from_dict = FinancialEvents.from_dict(financial_events_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


