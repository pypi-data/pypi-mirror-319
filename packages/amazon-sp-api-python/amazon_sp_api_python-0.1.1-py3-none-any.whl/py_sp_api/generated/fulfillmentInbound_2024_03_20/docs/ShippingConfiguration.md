# ShippingConfiguration

The shipping configurations supported for the packing option. Available modes are ground small parcel, freight less-than-truckload (LTL), freight full-truckload (FTL) palletized, freight FTL non-palletized, ocean less-than-container-load (LCL), ocean full-container load (FCL), air small parcel, and air small parcel express.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_mode** | **str** | Mode of shipment transportation that this option will provide.  Possible values: &#x60;GROUND_SMALL_PARCEL&#x60;, &#x60;FREIGHT_LTL&#x60;, &#x60;FREIGHT_FTL_PALLET&#x60;, &#x60;FREIGHT_FTL_NONPALLET&#x60;, &#x60;OCEAN_LCL&#x60;, &#x60;OCEAN_FCL&#x60;, &#x60;AIR_SMALL_PARCEL&#x60;, &#x60;AIR_SMALL_PARCEL_EXPRESS&#x60;. | [optional] 
**shipping_solution** | **str** | Shipping program for the option. Possible values: &#x60;AMAZON_PARTNERED_CARRIER&#x60;, &#x60;USE_YOUR_OWN_CARRIER&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.shipping_configuration import ShippingConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingConfiguration from a JSON string
shipping_configuration_instance = ShippingConfiguration.from_json(json)
# print the JSON string representation of the object
print(ShippingConfiguration.to_json())

# convert the object into a dict
shipping_configuration_dict = shipping_configuration_instance.to_dict()
# create an instance of ShippingConfiguration from a dict
shipping_configuration_from_dict = ShippingConfiguration.from_dict(shipping_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


