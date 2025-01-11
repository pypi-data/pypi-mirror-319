# GetRatesRequest

The request schema for the getRates operation. When the channelType is Amazon, the shipTo address is not required and will be ignored.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_to** | [**Address**](Address.md) |  | [optional] 
**ship_from** | [**Address**](Address.md) |  | 
**return_to** | [**Address**](Address.md) |  | [optional] 
**ship_date** | **datetime** | The ship date and time (the requested pickup). This defaults to the current date and time. | [optional] 
**shipper_instruction** | [**ShipperInstruction**](ShipperInstruction.md) |  | [optional] 
**packages** | [**List[Package]**](Package.md) | A list of packages to be shipped through a shipping service offering. | 
**value_added_services** | [**ValueAddedServiceDetails**](ValueAddedServiceDetails.md) |  | [optional] 
**tax_details** | [**List[TaxDetail]**](TaxDetail.md) | A list of tax detail information. | [optional] 
**channel_details** | [**ChannelDetails**](ChannelDetails.md) |  | 
**client_reference_details** | [**List[ClientReferenceDetail]**](ClientReferenceDetail.md) | Object to pass additional information about the MCI Integrator shipperType: List of ClientReferenceDetail | [optional] 
**shipment_type** | [**ShipmentType**](ShipmentType.md) |  | [optional] 
**destination_access_point_details** | [**AccessPointDetails**](AccessPointDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_rates_request import GetRatesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetRatesRequest from a JSON string
get_rates_request_instance = GetRatesRequest.from_json(json)
# print the JSON string representation of the object
print(GetRatesRequest.to_json())

# convert the object into a dict
get_rates_request_dict = get_rates_request_instance.to_dict()
# create an instance of GetRatesRequest from a dict
get_rates_request_from_dict = GetRatesRequest.from_dict(get_rates_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


