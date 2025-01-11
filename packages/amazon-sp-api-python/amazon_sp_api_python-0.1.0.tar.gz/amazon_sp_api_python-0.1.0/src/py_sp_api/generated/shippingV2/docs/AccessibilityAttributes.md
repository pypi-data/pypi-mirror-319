# AccessibilityAttributes

Defines the accessibility details of the access point.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**distance** | **str** | The approximate distance of access point from input postalCode&#39;s centroid. | [optional] 
**drive_time** | **int** | The approximate (static) drive time from input postal code&#39;s centroid. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.accessibility_attributes import AccessibilityAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of AccessibilityAttributes from a JSON string
accessibility_attributes_instance = AccessibilityAttributes.from_json(json)
# print the JSON string representation of the object
print(AccessibilityAttributes.to_json())

# convert the object into a dict
accessibility_attributes_dict = accessibility_attributes_instance.to_dict()
# create an instance of AccessibilityAttributes from a dict
accessibility_attributes_from_dict = AccessibilityAttributes.from_dict(accessibility_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


