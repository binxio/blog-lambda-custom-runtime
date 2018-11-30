from sceptre.hooks import Hook
from sceptre.resolvers.stack_output import StackOutput

class S3EmptyBucket(Hook):
    NAME = 's3_empty_bucket'
    def __init__(self, *args, **kwargs):
        super(S3EmptyBucket, self).__init__(*args, **kwargs)

    def run(self):
        """
        Removes all objects from a bucket
        Usage: !s3_empty_bucket stack_name::output_name
        :return:
        """
        try:
            bucket_name = StackOutput(argument=self.argument,
                                      connection_manager=self.connection_manager,
                                      environment_config=self.environment_config,
                                      stack_config=self.stack_config,
                                      ).resolve()

            print(f"[{self.NAME}]: Emptying bucket: {bucket_name}")
            s3_client = self.connection_manager.boto_session.client('s3')
            paginator = s3_client.get_paginator('list_object_versions')
            bucket_iterator = paginator.paginate(Bucket=bucket_name)
            for page in bucket_iterator:
                for v in page['Versions']:
                    v_id = v['VersionId']
                    v_key = v['Key']
                    print(f"[{self.NAME}]: Deleting '{v_key}', '{v_id}")
                    s3_client.delete_object(
                        Bucket=bucket_name,
                        Key=v_key,
                        VersionId=v_id
                    )
        except Exception as e:
            print(f'[{self.NAME}]: Error: {e}')
