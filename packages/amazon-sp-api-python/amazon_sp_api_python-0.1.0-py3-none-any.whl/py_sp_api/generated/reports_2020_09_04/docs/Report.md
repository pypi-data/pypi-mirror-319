# Report


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_ids** | **List[str]** | A list of marketplace identifiers for the report. | [optional] 
**report_id** | **str** | The identifier for the report. This identifier is unique only in combination with a seller ID. | 
**report_type** | **str** | The report type. | 
**data_start_time** | **datetime** | The start of a date and time range used for selecting the data to report. | [optional] 
**data_end_time** | **datetime** | The end of a date and time range used for selecting the data to report. | [optional] 
**report_schedule_id** | **str** | The identifier of the report schedule that created this report (if any). This identifier is unique only in combination with a seller ID. | [optional] 
**created_time** | **datetime** | The date and time when the report was created. | 
**processing_status** | **str** | The processing status of the report. | 
**processing_start_time** | **datetime** | The date and time when the report processing started, in ISO 8601 date time format. | [optional] 
**processing_end_time** | **datetime** | The date and time when the report processing completed, in ISO 8601 date time format. | [optional] 
**report_document_id** | **str** | The identifier for the report document. Pass this into the getReportDocument operation to get the information you will need to retrieve and decrypt the report document&#39;s contents. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.report import Report

# TODO update the JSON string below
json = "{}"
# create an instance of Report from a JSON string
report_instance = Report.from_json(json)
# print the JSON string representation of the object
print(Report.to_json())

# convert the object into a dict
report_dict = report_instance.to_dict()
# create an instance of Report from a dict
report_from_dict = Report.from_dict(report_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


