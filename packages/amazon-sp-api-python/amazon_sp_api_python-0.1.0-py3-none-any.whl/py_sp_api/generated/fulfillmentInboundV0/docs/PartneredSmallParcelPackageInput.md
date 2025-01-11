# PartneredSmallParcelPackageInput

Dimension and weight information for the package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**Dimensions**](Dimensions.md) |  | 
**weight** | [**Weight**](Weight.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.partnered_small_parcel_package_input import PartneredSmallParcelPackageInput

# TODO update the JSON string below
json = "{}"
# create an instance of PartneredSmallParcelPackageInput from a JSON string
partnered_small_parcel_package_input_instance = PartneredSmallParcelPackageInput.from_json(json)
# print the JSON string representation of the object
print(PartneredSmallParcelPackageInput.to_json())

# convert the object into a dict
partnered_small_parcel_package_input_dict = partnered_small_parcel_package_input_instance.to_dict()
# create an instance of PartneredSmallParcelPackageInput from a dict
partnered_small_parcel_package_input_from_dict = PartneredSmallParcelPackageInput.from_dict(partnered_small_parcel_package_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


