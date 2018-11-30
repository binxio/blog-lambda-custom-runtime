from sceptre.hooks import Hook
from sceptre.resolvers.stack_output import StackOutput

class S3DeleteBucket(Hook):
    NAME = 's3_delete_bucket'
    def __init__(self, *args, **kwargs):
        super(S3DeleteBucket, self).__init__(*args, **kwargs)

    def run(self):
        """
        Deletes a bucket
        Usage: !s3_delete_bucket stack_name::output_name
        :return:
        """
        try:
            bucket_name = StackOutput(argument=self.argument,
                                 connection_manager=self.connection_manager,
                                 environment_config=self.environment_config,
                                 stack_config=self.stack_config,
                                 ).resolve()
            s3 = self.connection_manager.boto_session.resource('s3')
            bucket = s3.Bucket(bucket_name)
            print(f"[{self.NAME}]: Deleting bucket: {bucket_name}")
            bucket.delete()
        except Exception as e:
            print(e)
