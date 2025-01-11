# PartneredLtlDataOutput

Information returned by Amazon about a Less Than Truckload/Full Truckload (LTL/FTL) shipment by an Amazon-partnered carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contact** | [**Contact**](Contact.md) |  | 
**box_count** | **int** | Contains an unsigned integer | 
**seller_freight_class** | [**SellerFreightClass**](SellerFreightClass.md) |  | [optional] 
**freight_ready_date** | **date** | Type containing date in string format | 
**pallet_list** | [**List[Pallet]**](Pallet.md) | A list of pallet information. | 
**total_weight** | [**Weight**](Weight.md) |  | 
**seller_declared_value** | [**Amount**](Amount.md) |  | [optional] 
**amazon_calculated_value** | [**Amount**](Amount.md) |  | [optional] 
**preview_pickup_date** | **date** | Type containing date in string format | 
**preview_delivery_date** | **date** | Type containing date in string format | 
**preview_freight_class** | [**SellerFreightClass**](SellerFreightClass.md) |  | 
**amazon_reference_id** | **str** | A unique identifier created by Amazon that identifies this Amazon-partnered, Less Than Truckload/Full Truckload (LTL/FTL) shipment. | 
**is_bill_of_lading_available** | **bool** | Indicates whether the bill of lading for the shipment is available. | 
**partnered_estimate** | [**PartneredEstimate**](PartneredEstimate.md) |  | [optional] 
**carrier_name** | **str** | The carrier for the inbound shipment. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.partnered_ltl_data_output import PartneredLtlDataOutput

# TODO update the JSON string below
json = "{}"
# create an instance of PartneredLtlDataOutput from a JSON string
partnered_ltl_data_output_instance = PartneredLtlDataOutput.from_json(json)
# print the JSON string representation of the object
print(PartneredLtlDataOutput.to_json())

# convert the object into a dict
partnered_ltl_data_output_dict = partnered_ltl_data_output_instance.to_dict()
# create an instance of PartneredLtlDataOutput from a dict
partnered_ltl_data_output_from_dict = PartneredLtlDataOutput.from_dict(partnered_ltl_data_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


