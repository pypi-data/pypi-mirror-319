# PartneredLtlDataInput

Information that is required by an Amazon-partnered carrier to ship a Less Than Truckload/Full Truckload (LTL/FTL) inbound shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contact** | [**Contact**](Contact.md) |  | [optional] 
**box_count** | **int** | Contains an unsigned integer | [optional] 
**seller_freight_class** | [**SellerFreightClass**](SellerFreightClass.md) |  | [optional] 
**freight_ready_date** | **date** | Type containing date in string format | [optional] 
**pallet_list** | [**List[Pallet]**](Pallet.md) | A list of pallet information. | [optional] 
**total_weight** | [**Weight**](Weight.md) |  | [optional] 
**seller_declared_value** | [**Amount**](Amount.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.partnered_ltl_data_input import PartneredLtlDataInput

# TODO update the JSON string below
json = "{}"
# create an instance of PartneredLtlDataInput from a JSON string
partnered_ltl_data_input_instance = PartneredLtlDataInput.from_json(json)
# print the JSON string representation of the object
print(PartneredLtlDataInput.to_json())

# convert the object into a dict
partnered_ltl_data_input_dict = partnered_ltl_data_input_instance.to_dict()
# create an instance of PartneredLtlDataInput from a dict
partnered_ltl_data_input_from_dict = PartneredLtlDataInput.from_dict(partnered_ltl_data_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


