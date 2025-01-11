# PartneredSmallParcelDataOutput

Information returned by Amazon about a Small Parcel shipment by an Amazon-partnered carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_list** | [**List[PartneredSmallParcelPackageOutput]**](PartneredSmallParcelPackageOutput.md) | A list of packages, including shipping information from the Amazon-partnered carrier. | 
**partnered_estimate** | [**PartneredEstimate**](PartneredEstimate.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.partnered_small_parcel_data_output import PartneredSmallParcelDataOutput

# TODO update the JSON string below
json = "{}"
# create an instance of PartneredSmallParcelDataOutput from a JSON string
partnered_small_parcel_data_output_instance = PartneredSmallParcelDataOutput.from_json(json)
# print the JSON string representation of the object
print(PartneredSmallParcelDataOutput.to_json())

# convert the object into a dict
partnered_small_parcel_data_output_dict = partnered_small_parcel_data_output_instance.to_dict()
# create an instance of PartneredSmallParcelDataOutput from a dict
partnered_small_parcel_data_output_from_dict = PartneredSmallParcelDataOutput.from_dict(partnered_small_parcel_data_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


