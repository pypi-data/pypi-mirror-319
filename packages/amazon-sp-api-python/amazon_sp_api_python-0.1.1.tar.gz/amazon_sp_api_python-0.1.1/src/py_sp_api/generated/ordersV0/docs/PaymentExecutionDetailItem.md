# PaymentExecutionDetailItem

Information about a sub-payment method used to pay for a COD order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment** | [**Money**](Money.md) |  | 
**payment_method** | **str** | A sub-payment method for a COD order.  **Possible values**: * &#x60;COD&#x60;: Cash on delivery  * &#x60;GC&#x60;: Gift card  * &#x60;PointsAccount&#x60;: Amazon Points * &#x60;Invoice&#x60;: Invoice | 

## Example

```python
from py_sp_api.generated.ordersV0.models.payment_execution_detail_item import PaymentExecutionDetailItem

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentExecutionDetailItem from a JSON string
payment_execution_detail_item_instance = PaymentExecutionDetailItem.from_json(json)
# print the JSON string representation of the object
print(PaymentExecutionDetailItem.to_json())

# convert the object into a dict
payment_execution_detail_item_dict = payment_execution_detail_item_instance.to_dict()
# create an instance of PaymentExecutionDetailItem from a dict
payment_execution_detail_item_from_dict = PaymentExecutionDetailItem.from_dict(payment_execution_detail_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


