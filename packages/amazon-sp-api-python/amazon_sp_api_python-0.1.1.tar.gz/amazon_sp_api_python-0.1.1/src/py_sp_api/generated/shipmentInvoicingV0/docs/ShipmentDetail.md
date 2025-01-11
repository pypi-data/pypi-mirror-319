# ShipmentDetail

The information required by a selling partner to issue a shipment invoice.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warehouse_id** | **str** | The Amazon-defined identifier for the warehouse. | [optional] 
**amazon_order_id** | **str** | The Amazon-defined identifier for the order. | [optional] 
**amazon_shipment_id** | **str** | The Amazon-defined identifier for the shipment. | [optional] 
**purchase_date** | **datetime** | The date and time when the order was created. | [optional] 
**shipping_address** | [**Address**](Address.md) |  | [optional] 
**payment_method_details** | **List[str]** | The list of payment method details. | [optional] 
**marketplace_id** | **str** | The identifier for the marketplace where the order was placed. | [optional] 
**seller_id** | **str** | The seller identifier. | [optional] 
**buyer_name** | **str** | The name of the buyer. | [optional] 
**buyer_county** | **str** | The county of the buyer. | [optional] 
**buyer_tax_info** | [**BuyerTaxInfo**](BuyerTaxInfo.md) |  | [optional] 
**marketplace_tax_info** | [**MarketplaceTaxInfo**](MarketplaceTaxInfo.md) |  | [optional] 
**seller_display_name** | **str** | The seller’s friendly name registered in the marketplace. | [optional] 
**shipment_items** | [**List[ShipmentItem]**](ShipmentItem.md) | A list of shipment items. | [optional] 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.shipment_detail import ShipmentDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentDetail from a JSON string
shipment_detail_instance = ShipmentDetail.from_json(json)
# print the JSON string representation of the object
print(ShipmentDetail.to_json())

# convert the object into a dict
shipment_detail_dict = shipment_detail_instance.to_dict()
# create an instance of ShipmentDetail from a dict
shipment_detail_from_dict = ShipmentDetail.from_dict(shipment_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


