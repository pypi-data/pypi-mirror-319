# NonPartneredSmallParcelPackageInput

The tracking number of the package, provided by the carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tracking_id** | **str** | The tracking number of the package, provided by the carrier. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.non_partnered_small_parcel_package_input import NonPartneredSmallParcelPackageInput

# TODO update the JSON string below
json = "{}"
# create an instance of NonPartneredSmallParcelPackageInput from a JSON string
non_partnered_small_parcel_package_input_instance = NonPartneredSmallParcelPackageInput.from_json(json)
# print the JSON string representation of the object
print(NonPartneredSmallParcelPackageInput.to_json())

# convert the object into a dict
non_partnered_small_parcel_package_input_dict = non_partnered_small_parcel_package_input_instance.to_dict()
# create an instance of NonPartneredSmallParcelPackageInput from a dict
non_partnered_small_parcel_package_input_from_dict = NonPartneredSmallParcelPackageInput.from_dict(non_partnered_small_parcel_package_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


