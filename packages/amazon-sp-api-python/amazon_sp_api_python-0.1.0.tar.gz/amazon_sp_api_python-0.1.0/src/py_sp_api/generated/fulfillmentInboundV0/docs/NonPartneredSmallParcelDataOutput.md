# NonPartneredSmallParcelDataOutput

Information returned by Amazon about a Small Parcel shipment by a carrier that has not partnered with Amazon.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_list** | [**List[NonPartneredSmallParcelPackageOutput]**](NonPartneredSmallParcelPackageOutput.md) | A list of packages, including carrier, tracking number, and status information for each package. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.non_partnered_small_parcel_data_output import NonPartneredSmallParcelDataOutput

# TODO update the JSON string below
json = "{}"
# create an instance of NonPartneredSmallParcelDataOutput from a JSON string
non_partnered_small_parcel_data_output_instance = NonPartneredSmallParcelDataOutput.from_json(json)
# print the JSON string representation of the object
print(NonPartneredSmallParcelDataOutput.to_json())

# convert the object into a dict
non_partnered_small_parcel_data_output_dict = non_partnered_small_parcel_data_output_instance.to_dict()
# create an instance of NonPartneredSmallParcelDataOutput from a dict
non_partnered_small_parcel_data_output_from_dict = NonPartneredSmallParcelDataOutput.from_dict(non_partnered_small_parcel_data_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


