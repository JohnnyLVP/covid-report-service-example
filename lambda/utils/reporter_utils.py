import pandas as pd
from s3 import S3Manager

class ReporterServicesUtils:

    response_columns = ['confirmed','deaths','recovered']

    def __init__(self):
        pass
    
    @classmethod
    def filtering_df_data(self,df,filter_country,filter_date):
        
        filter_df = df[(df.country == filter_country) & (df.date == filter_date)][self.response_columns]
        return filter_df.to_json(orient = 'index')
    
    @classmethod
    def report_filter(self,s3_bucket,s3_key,country,date):

        s3_manager = S3Manager()
        try:
            file_object = s3_manager.get_file_object(s3_bucket, s3_key)
            df_report = pd.read_csv(file_object) 
            json_file = self.filtering_df_data(df_report, country, date)

            return json_file

        except Exception as e:
            print(f"Exception has ocurred: {e}")
