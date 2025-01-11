# NonPartneredSmallParcelPackageOutput

Carrier, tracking number, and status information for the package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **str** | The carrier that you are using for the inbound shipment. | 
**tracking_id** | **str** | The tracking number of the package, provided by the carrier. | 
**package_status** | [**PackageStatus**](PackageStatus.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.non_partnered_small_parcel_package_output import NonPartneredSmallParcelPackageOutput

# TODO update the JSON string below
json = "{}"
# create an instance of NonPartneredSmallParcelPackageOutput from a JSON string
non_partnered_small_parcel_package_output_instance = NonPartneredSmallParcelPackageOutput.from_json(json)
# print the JSON string representation of the object
print(NonPartneredSmallParcelPackageOutput.to_json())

# convert the object into a dict
non_partnered_small_parcel_package_output_dict = non_partnered_small_parcel_package_output_instance.to_dict()
# create an instance of NonPartneredSmallParcelPackageOutput from a dict
non_partnered_small_parcel_package_output_from_dict = NonPartneredSmallParcelPackageOutput.from_dict(non_partnered_small_parcel_package_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


