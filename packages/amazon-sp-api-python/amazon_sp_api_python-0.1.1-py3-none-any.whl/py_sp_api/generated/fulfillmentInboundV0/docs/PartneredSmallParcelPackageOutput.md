# PartneredSmallParcelPackageOutput

Dimension, weight, and shipping information for the package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**Dimensions**](Dimensions.md) |  | 
**weight** | [**Weight**](Weight.md) |  | 
**carrier_name** | **str** | The carrier specified with a previous call to putTransportDetails. | 
**tracking_id** | **str** | The tracking number of the package, provided by the carrier. | 
**package_status** | [**PackageStatus**](PackageStatus.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.partnered_small_parcel_package_output import PartneredSmallParcelPackageOutput

# TODO update the JSON string below
json = "{}"
# create an instance of PartneredSmallParcelPackageOutput from a JSON string
partnered_small_parcel_package_output_instance = PartneredSmallParcelPackageOutput.from_json(json)
# print the JSON string representation of the object
print(PartneredSmallParcelPackageOutput.to_json())

# convert the object into a dict
partnered_small_parcel_package_output_dict = partnered_small_parcel_package_output_instance.to_dict()
# create an instance of PartneredSmallParcelPackageOutput from a dict
partnered_small_parcel_package_output_from_dict = PartneredSmallParcelPackageOutput.from_dict(partnered_small_parcel_package_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


