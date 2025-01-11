# OrderItem

A single order item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The item&#39;s Amazon Standard Identification Number (ASIN). | 
**seller_sku** | **str** | The item&#39;s seller stock keeping unit (SKU). | [optional] 
**order_item_id** | **str** | An Amazon-defined order item identifier. | 
**associated_items** | [**List[AssociatedItem]**](AssociatedItem.md) | A list of associated items that a customer has purchased with a product. For example, a tire installation service purchased with tires. | [optional] 
**title** | **str** | The item&#39;s name. | [optional] 
**quantity_ordered** | **int** | The number of items in the order.  | 
**quantity_shipped** | **int** | The number of items shipped. | [optional] 
**product_info** | [**ProductInfoDetail**](ProductInfoDetail.md) |  | [optional] 
**points_granted** | [**PointsGrantedDetail**](PointsGrantedDetail.md) |  | [optional] 
**item_price** | [**Money**](Money.md) |  | [optional] 
**shipping_price** | [**Money**](Money.md) |  | [optional] 
**item_tax** | [**Money**](Money.md) |  | [optional] 
**shipping_tax** | [**Money**](Money.md) |  | [optional] 
**shipping_discount** | [**Money**](Money.md) |  | [optional] 
**shipping_discount_tax** | [**Money**](Money.md) |  | [optional] 
**promotion_discount** | [**Money**](Money.md) |  | [optional] 
**promotion_discount_tax** | [**Money**](Money.md) |  | [optional] 
**promotion_ids** | **List[str]** | A list of promotion identifiers provided by the seller when the promotions were created. | [optional] 
**cod_fee** | [**Money**](Money.md) |  | [optional] 
**cod_fee_discount** | [**Money**](Money.md) |  | [optional] 
**is_gift** | **str** | Indicates whether the item is a gift.  **Possible values**: &#x60;true&#x60; and &#x60;false&#x60;. | [optional] 
**condition_note** | **str** | The condition of the item, as described by the seller. | [optional] 
**condition_id** | **str** | The condition of the item.  **Possible values**: &#x60;New&#x60;, &#x60;Used&#x60;, &#x60;Collectible&#x60;, &#x60;Refurbished&#x60;, &#x60;Preorder&#x60;, and &#x60;Club&#x60;. | [optional] 
**condition_subtype_id** | **str** | The subcondition of the item.  **Possible values**: &#x60;New&#x60;, &#x60;Mint&#x60;, &#x60;Very Good&#x60;, &#x60;Good&#x60;, &#x60;Acceptable&#x60;, &#x60;Poor&#x60;, &#x60;Club&#x60;, &#x60;OEM&#x60;, &#x60;Warranty&#x60;, &#x60;Refurbished Warranty&#x60;, &#x60;Refurbished&#x60;, &#x60;Open Box&#x60;, &#x60;Any&#x60;, and &#x60;Other&#x60;. | [optional] 
**scheduled_delivery_start_date** | **str** | The start date of the scheduled delivery window in the time zone for the order destination. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date time format. | [optional] 
**scheduled_delivery_end_date** | **str** | The end date of the scheduled delivery window in the time zone for the order destination. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date time format. | [optional] 
**price_designation** | **str** | Indicates that the selling price is a special price that is only available for Amazon Business orders. For more information about the Amazon Business Seller Program, refer to the [Amazon Business website](https://www.amazon.com/b2b/info/amazon-business).   **Possible values**: &#x60;BusinessPrice&#x60; | [optional] 
**tax_collection** | [**TaxCollection**](TaxCollection.md) |  | [optional] 
**serial_number_required** | **bool** | When true, the product type for this item has a serial number.   Only returned for Amazon Easy Ship orders. | [optional] 
**is_transparency** | **bool** | When true, the ASIN is enrolled in Transparency. The Transparency serial number that you must submit is determined by:  **1D or 2D Barcode:** This has a **T** logo. Submit either the 29-character alpha-numeric identifier beginning with **AZ** or **ZA**, or the 38-character Serialized Global Trade Item Number (SGTIN). **2D Barcode SN:** Submit the 7- to 20-character serial number barcode, which likely has the prefix **SN**. The serial number is applied to the same side of the packaging as the GTIN (UPC/EAN/ISBN) barcode. **QR code SN:** Submit the URL that the QR code generates. | [optional] 
**ioss_number** | **str** | The IOSS number of the marketplace. Sellers shipping to the EU from outside the EU must provide this IOSS number to their carrier when Amazon has collected the VAT on the sale. | [optional] 
**store_chain_store_id** | **str** | The store chain store identifier. Linked to a specific store in a store chain. | [optional] 
**deemed_reseller_category** | **str** | The category of deemed reseller. This applies to selling partners that are not based in the EU and is used to help them meet the VAT Deemed Reseller tax laws in the EU and UK. | [optional] 
**buyer_info** | [**ItemBuyerInfo**](ItemBuyerInfo.md) |  | [optional] 
**buyer_requested_cancel** | [**BuyerRequestedCancel**](BuyerRequestedCancel.md) |  | [optional] 
**serial_numbers** | **List[str]** | A list of serial numbers for electronic products that are shipped to customers. Returned for FBA orders only. | [optional] 
**substitution_preferences** | [**SubstitutionPreferences**](SubstitutionPreferences.md) |  | [optional] 
**measurement** | [**Measurement**](Measurement.md) |  | [optional] 
**shipping_constraints** | [**ShippingConstraints**](ShippingConstraints.md) |  | [optional] 
**amazon_programs** | [**AmazonPrograms**](AmazonPrograms.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.order_item import OrderItem

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItem from a JSON string
order_item_instance = OrderItem.from_json(json)
# print the JSON string representation of the object
print(OrderItem.to_json())

# convert the object into a dict
order_item_dict = order_item_instance.to_dict()
# create an instance of OrderItem from a dict
order_item_from_dict = OrderItem.from_dict(order_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


