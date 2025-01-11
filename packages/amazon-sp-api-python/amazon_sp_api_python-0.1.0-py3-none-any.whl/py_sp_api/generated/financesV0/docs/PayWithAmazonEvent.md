# PayWithAmazonEvent

An event related to the seller's Pay with Amazon account.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_order_id** | **str** | An order identifier that is specified by the seller. | [optional] 
**transaction_posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**business_object_type** | **str** | The type of business object. | [optional] 
**sales_channel** | **str** | The sales channel for the transaction. | [optional] 
**charge** | [**ChargeComponent**](ChargeComponent.md) |  | [optional] 
**fee_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**payment_amount_type** | **str** | The type of payment.  Possible values:  * Sales | [optional] 
**amount_description** | **str** | A short description of this payment event. | [optional] 
**fulfillment_channel** | **str** | The fulfillment channel.  Possible values:  * AFN - Amazon Fulfillment Network (Fulfillment by Amazon)  * MFN - Merchant Fulfillment Network (self-fulfilled) | [optional] 
**store_name** | **str** | The store name where the event occurred. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.pay_with_amazon_event import PayWithAmazonEvent

# TODO update the JSON string below
json = "{}"
# create an instance of PayWithAmazonEvent from a JSON string
pay_with_amazon_event_instance = PayWithAmazonEvent.from_json(json)
# print the JSON string representation of the object
print(PayWithAmazonEvent.to_json())

# convert the object into a dict
pay_with_amazon_event_dict = pay_with_amazon_event_instance.to_dict()
# create an instance of PayWithAmazonEvent from a dict
pay_with_amazon_event_from_dict = PayWithAmazonEvent.from_dict(pay_with_amazon_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


