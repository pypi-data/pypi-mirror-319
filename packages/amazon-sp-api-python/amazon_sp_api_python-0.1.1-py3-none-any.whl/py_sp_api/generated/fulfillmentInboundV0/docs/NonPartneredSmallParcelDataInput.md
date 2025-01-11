# NonPartneredSmallParcelDataInput

Information that you provide to Amazon about a Small Parcel shipment shipped by a carrier that has not partnered with Amazon.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **str** | The carrier that you are using for the inbound shipment. | 
**package_list** | [**List[NonPartneredSmallParcelPackageInput]**](NonPartneredSmallParcelPackageInput.md) | A list of package tracking information. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.non_partnered_small_parcel_data_input import NonPartneredSmallParcelDataInput

# TODO update the JSON string below
json = "{}"
# create an instance of NonPartneredSmallParcelDataInput from a JSON string
non_partnered_small_parcel_data_input_instance = NonPartneredSmallParcelDataInput.from_json(json)
# print the JSON string representation of the object
print(NonPartneredSmallParcelDataInput.to_json())

# convert the object into a dict
non_partnered_small_parcel_data_input_dict = non_partnered_small_parcel_data_input_instance.to_dict()
# create an instance of NonPartneredSmallParcelDataInput from a dict
non_partnered_small_parcel_data_input_from_dict = NonPartneredSmallParcelDataInput.from_dict(non_partnered_small_parcel_data_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


