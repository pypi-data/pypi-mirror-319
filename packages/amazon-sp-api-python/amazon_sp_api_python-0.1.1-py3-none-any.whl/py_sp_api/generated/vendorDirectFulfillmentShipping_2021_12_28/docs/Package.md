# Package

The package that is associated with the container.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_tracking_number** | **str** | The tracking number on the label of shipment package, that you can fetch from the &#x60;shippingLabels&#x60; response. You can also scan the bar code on the shipping label to get the tracking number. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.package import Package

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


