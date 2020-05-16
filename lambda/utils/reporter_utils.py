import pandas as pd
import io
from utils.s3 import S3Manager

class ReporterServicesUtils:

    response_columns = ['confirmed','deaths','recovered']

    def __init__(self):
        pass
    
    @classmethod
    def filtering_df_data(self,df,filter_country,filter_date):
        
        filter_df = df[(df.country == filter_country) & (df.date == filter_date)][self.response_columns]
        
        return filter_df.to_json(orient = 'records')
    
    @classmethod
    def report_filter(self,s3_bucket,s3_key,filter_country,filter_date):

        s3_manager = S3Manager()
        try:
            file_object = s3_manager.get_file_object(s3_bucket, s3_key)
            
            df_report = pd.read_csv(io.BytesIO(file_object)) 
            json_file = self.filtering_df_data(df_report, filter_country, filter_date)
            
            return json_file

        except Exception as e:
            print("Exception has ocurred: {}".format(e))
