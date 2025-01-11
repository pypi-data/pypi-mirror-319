# JobListing

The payload for the `getServiceJobs` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_result_size** | **int** | Total result size of the query result. | [optional] 
**next_page_token** | **str** | A generated string used to pass information to your next request. If &#x60;nextPageToken&#x60; is returned, pass the value of &#x60;nextPageToken&#x60; to the &#x60;pageToken&#x60; to get next results. | [optional] 
**previous_page_token** | **str** | A generated string used to pass information to your next request. If &#x60;previousPageToken&#x60; is returned, pass the value of &#x60;previousPageToken&#x60; to the &#x60;pageToken&#x60; to get previous page results. | [optional] 
**jobs** | [**List[ServiceJob]**](ServiceJob.md) | List of job details for the given input. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.job_listing import JobListing

# TODO update the JSON string below
json = "{}"
# create an instance of JobListing from a JSON string
job_listing_instance = JobListing.from_json(json)
# print the JSON string representation of the object
print(JobListing.to_json())

# convert the object into a dict
job_listing_dict = job_listing_instance.to_dict()
# create an instance of JobListing from a dict
job_listing_from_dict = JobListing.from_dict(job_listing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


