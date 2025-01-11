# OrderItemTaxDetails

Total tax details for the line item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_line_item** | [**List[TaxDetails]**](TaxDetails.md) | A list of tax line items. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.order_item_tax_details import OrderItemTaxDetails

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItemTaxDetails from a JSON string
order_item_tax_details_instance = OrderItemTaxDetails.from_json(json)
# print the JSON string representation of the object
print(OrderItemTaxDetails.to_json())

# convert the object into a dict
order_item_tax_details_dict = order_item_tax_details_instance.to_dict()
# create an instance of OrderItemTaxDetails from a dict
order_item_tax_details_from_dict = OrderItemTaxDetails.from_dict(order_item_tax_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


