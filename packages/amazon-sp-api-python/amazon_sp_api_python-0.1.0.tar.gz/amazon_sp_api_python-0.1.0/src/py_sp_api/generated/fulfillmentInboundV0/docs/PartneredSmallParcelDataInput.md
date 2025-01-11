# PartneredSmallParcelDataInput

Information that is required by an Amazon-partnered carrier to ship a Small Parcel inbound shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_list** | [**List[PartneredSmallParcelPackageInput]**](PartneredSmallParcelPackageInput.md) | A list of dimensions and weight information for packages. | [optional] 
**carrier_name** | **str** | The Amazon-partnered carrier to use for the inbound shipment. **&#x60;CarrierName&#x60;** values in France (FR), Italy (IT), Spain (ES), the United Kingdom (UK), and the United States (US): &#x60;UNITED_PARCEL_SERVICE_INC&#x60;. &lt;br&gt; **&#x60;CarrierName&#x60;** values in Germany (DE): &#x60;DHL_STANDARD&#x60;,&#x60;UNITED_PARCEL_SERVICE_INC&#x60;. &lt;br&gt;Default: &#x60;UNITED_PARCEL_SERVICE_INC&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.partnered_small_parcel_data_input import PartneredSmallParcelDataInput

# TODO update the JSON string below
json = "{}"
# create an instance of PartneredSmallParcelDataInput from a JSON string
partnered_small_parcel_data_input_instance = PartneredSmallParcelDataInput.from_json(json)
# print the JSON string representation of the object
print(PartneredSmallParcelDataInput.to_json())

# convert the object into a dict
partnered_small_parcel_data_input_dict = partnered_small_parcel_data_input_instance.to_dict()
# create an instance of PartneredSmallParcelDataInput from a dict
partnered_small_parcel_data_input_from_dict = PartneredSmallParcelDataInput.from_dict(partnered_small_parcel_data_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


