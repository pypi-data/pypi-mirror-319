# ProductAdsPaymentEvent

A Sponsored Products payment event.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**transaction_type** | **str** | Indicates if the transaction is for a charge or a refund.  Possible values:  * charge - Charge  * refund - Refund | [optional] 
**invoice_id** | **str** | Identifier for the invoice that the transaction appears in. | [optional] 
**base_value** | [**Currency**](Currency.md) |  | [optional] 
**tax_value** | [**Currency**](Currency.md) |  | [optional] 
**transaction_value** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.product_ads_payment_event import ProductAdsPaymentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ProductAdsPaymentEvent from a JSON string
product_ads_payment_event_instance = ProductAdsPaymentEvent.from_json(json)
# print the JSON string representation of the object
print(ProductAdsPaymentEvent.to_json())

# convert the object into a dict
product_ads_payment_event_dict = product_ads_payment_event_instance.to_dict()
# create an instance of ProductAdsPaymentEvent from a dict
product_ads_payment_event_from_dict = ProductAdsPaymentEvent.from_dict(product_ads_payment_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


