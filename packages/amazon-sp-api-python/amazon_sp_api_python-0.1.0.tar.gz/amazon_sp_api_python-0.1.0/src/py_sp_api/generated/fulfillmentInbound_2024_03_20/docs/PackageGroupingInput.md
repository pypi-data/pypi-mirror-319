# PackageGroupingInput

Packing information for the inbound plan.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**boxes** | [**List[BoxInput]**](BoxInput.md) | Box level information being provided. | 
**packing_group_id** | **str** | The ID of the &#x60;packingGroup&#x60; that packages are grouped according to. The &#x60;PackingGroupId&#x60; can only be provided before placement confirmation, and it must belong to the confirmed &#x60;PackingOption&#x60;. One of &#x60;ShipmentId&#x60; or &#x60;PackingGroupId&#x60; must be provided with every request. | [optional] 
**shipment_id** | **str** | The ID of the shipment that packages are grouped according to. The &#x60;ShipmentId&#x60; can only be provided after placement confirmation, and the shipment must belong to the confirmed placement option. One of &#x60;ShipmentId&#x60; or &#x60;PackingGroupId&#x60; must be provided with every request. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.package_grouping_input import PackageGroupingInput

# TODO update the JSON string below
json = "{}"
# create an instance of PackageGroupingInput from a JSON string
package_grouping_input_instance = PackageGroupingInput.from_json(json)
# print the JSON string representation of the object
print(PackageGroupingInput.to_json())

# convert the object into a dict
package_grouping_input_dict = package_grouping_input_instance.to_dict()
# create an instance of PackageGroupingInput from a dict
package_grouping_input_from_dict = PackageGroupingInput.from_dict(package_grouping_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


