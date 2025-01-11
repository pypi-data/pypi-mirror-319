# PackageDetail

Properties of packages

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_reference_id** | **str** | A seller-supplied identifier that uniquely identifies a package within the scope of an order. Only positive numeric values are supported. | 
**carrier_code** | **str** | Identifies the carrier that will deliver the package. This field is required for all marketplaces. For more information, refer to the [&#x60;CarrierCode&#x60; announcement](https://developer-docs.amazon.com/sp-api/changelog/carriercode-value-required-in-shipment-confirmations-for-br-mx-ca-sg-au-in-jp-marketplaces). | 
**carrier_name** | **str** | Carrier Name that will deliver the package. Required when &#x60;carrierCode&#x60; is \&quot;Others\&quot;  | [optional] 
**shipping_method** | **str** | Ship method to be used for shipping the order. | [optional] 
**tracking_number** | **str** | The tracking number used to obtain tracking and delivery information. | 
**ship_date** | **datetime** | The shipping date for the package. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; date/time format. | 
**ship_from_supply_source_id** | **str** | The unique identifier for the supply source. | [optional] 
**order_items** | [**List[ConfirmShipmentOrderItem]**](ConfirmShipmentOrderItem.md) | A list of order items. | 

## Example

```python
from py_sp_api.generated.ordersV0.models.package_detail import PackageDetail

# TODO update the JSON string below
json = "{}"
# create an instance of PackageDetail from a JSON string
package_detail_instance = PackageDetail.from_json(json)
# print the JSON string representation of the object
print(PackageDetail.to_json())

# convert the object into a dict
package_detail_dict = package_detail_instance.to_dict()
# create an instance of PackageDetail from a dict
package_detail_from_dict = PackageDetail.from_dict(package_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


