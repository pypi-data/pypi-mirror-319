# Package

A package to be shipped through a shipping service offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**Dimensions**](Dimensions.md) |  | 
**weight** | [**Weight**](Weight.md) |  | 
**insured_value** | [**Currency**](Currency.md) |  | 
**is_hazmat** | **bool** | When true, the package contains hazardous materials. Defaults to false. | [optional] 
**seller_display_name** | **str** | The seller name displayed on the label. | [optional] 
**charges** | [**List[ChargeComponent]**](ChargeComponent.md) | A list of charges based on the shipping service charges applied on a package. | [optional] 
**package_client_reference_id** | **str** | A client provided unique identifier for a package being shipped. This value should be saved by the client to pass as a parameter to the getShipmentDocuments operation. | 
**items** | [**List[Item]**](Item.md) | A list of items. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.package import Package

# TODO update the JSON string below
json = "{}"
# create an instance of Package from a JSON string
package_instance = Package.from_json(json)
# print the JSON string representation of the object
print(Package.to_json())

# convert the object into a dict
package_dict = package_instance.to_dict()
# create an instance of Package from a dict
package_from_dict = Package.from_dict(package_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


