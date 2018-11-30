from sceptre.hooks import Hook
from sceptre.resolvers.stack_output import StackOutput
import boto3
import os


class S3UploadFile(Hook):
    NAME = 's3_upload_file'
    def __init__(self, *args, **kwargs):
        super(S3UploadFile, self).__init__(*args, **kwargs)

    def run(self):
        """
        Uploads a file to s3
        Usage: !s3_upload_file file_name bucket_key stack_name::output_name
        :return:
        """
        try:
            cwd = os.getcwd()
            print(f'[{self.NAME}]: The current working directory is: {cwd}')
            file_name, bucket_key, stack_param = self.argument.split(' ', 2)
            bucket_name = StackOutput(argument=stack_param,
                                 connection_manager=self.connection_manager,
                                 environment_config=self.environment_config,
                                 stack_config=self.stack_config,
                                 ).resolve()
            print(f"[{self.NAME}]: Copying {file_name} to bucket: s3://{bucket_name}/{bucket_key}")
            s3 = self.connection_manager.boto_session.resource('s3')
            bucket = s3.Bucket(bucket_name)
            bucket.upload_file(file_name, bucket_key)
        except Exception as e:
            print(e)
