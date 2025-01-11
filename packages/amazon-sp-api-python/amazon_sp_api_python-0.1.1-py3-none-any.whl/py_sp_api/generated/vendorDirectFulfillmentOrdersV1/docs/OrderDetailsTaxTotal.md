# OrderDetailsTaxTotal

The total Tax object within shipment that relates to the order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_line_item** | [**List[TaxDetails]**](TaxDetails.md) | A list of tax line items. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.order_details_tax_total import OrderDetailsTaxTotal

# TODO update the JSON string below
json = "{}"
# create an instance of OrderDetailsTaxTotal from a JSON string
order_details_tax_total_instance = OrderDetailsTaxTotal.from_json(json)
# print the JSON string representation of the object
print(OrderDetailsTaxTotal.to_json())

# convert the object into a dict
order_details_tax_total_dict = order_details_tax_total_instance.to_dict()
# create an instance of OrderDetailsTaxTotal from a dict
order_details_tax_total_from_dict = OrderDetailsTaxTotal.from_dict(order_details_tax_total_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


