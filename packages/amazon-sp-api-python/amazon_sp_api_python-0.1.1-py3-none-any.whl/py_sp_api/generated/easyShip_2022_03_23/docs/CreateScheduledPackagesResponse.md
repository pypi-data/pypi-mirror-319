# CreateScheduledPackagesResponse

The response schema for the bulk scheduling API. It returns by the bulk scheduling API containing an array of the scheduled packtages, an optional list of orders we couldn't schedule with the reason, and a pre-signed URL for a ZIP file containing the associated shipping labels plus the documents enabled for your marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scheduled_packages** | [**List[Package]**](Package.md) | A list of packages. Refer to the &#x60;Package&#x60; object. | [optional] 
**rejected_orders** | [**List[RejectedOrder]**](RejectedOrder.md) | A list of orders we couldn&#39;t scheduled on your behalf. Each element contains the reason and details on the error. | [optional] 
**printable_documents_url** | **str** | A pre-signed URL for the zip document containing the shipping labels and the documents enabled for your marketplace. | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.create_scheduled_packages_response import CreateScheduledPackagesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateScheduledPackagesResponse from a JSON string
create_scheduled_packages_response_instance = CreateScheduledPackagesResponse.from_json(json)
# print the JSON string representation of the object
print(CreateScheduledPackagesResponse.to_json())

# convert the object into a dict
create_scheduled_packages_response_dict = create_scheduled_packages_response_instance.to_dict()
# create an instance of CreateScheduledPackagesResponse from a dict
create_scheduled_packages_response_from_dict = CreateScheduledPackagesResponse.from_dict(create_scheduled_packages_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


