import json
import pandas
import os

from utils.reporter_utils import ReporterServicesUtils

def lambda_handler(event,context):

    print(json.dumps(event))

    body = event['body']
    request_report = process_post_request(body)

    return get_response_hash(request_report)

def process_post_request(body):

    country = body['country']
    date_report = body['date_report']

    request_report = ReporterServicesUtils.report_filter(
        s3_bucket = os.environ['S3_BUCKET'],
        s3_key = os.environ['S3_FILE_KEY'],
        country = country,
        date = date_report
    )

    return request_report

def get_response_hash(report=None, comment = None, status_code=200):
    """
    this function returns a json string containing the status code and success reason.
    :param comment: error message or None
    :param status_code: error status code
    :return: dictionary containing response body.
    """
    resp_hash = {}
    report_dict = json.loads(report)["0"]
    if report:
        resp_hash["confirmed"] = report_dict["confirmed"]
        resp_hash["deaths"] = report_dict["deaths"]
        resp_hash["recovered"] = report_dict["recovered"]
    if comment:
        resp_hash["reason"] = "{}".format(comment)

    resp_hash['success'] = (status_code == 200)
    return {
        'statusCode': status_code,
        'body': json.dumps(resp_hash)
    }