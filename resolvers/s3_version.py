from sceptre.resolvers import Resolver
from sceptre.resolvers.stack_output import StackOutput


class S3Version(Resolver):
    NAME = "s3_version"

    def get_stack_output(self, stack_name):
        return StackOutput(argument=stack_name,
                           connection_manager=self.connection_manager,
                           environment_config=self.environment_config,
                           stack_config=self.stack_config,
                           ).resolve()

    def __init__(self, *args, **kwargs):
        super(S3Version, self).__init__(*args, **kwargs)

    def resolve(self):
        if self.argument:
            s3_bucket, s3_key = self.argument.split("/", 1)
            if '::' in s3_bucket:
                s3_bucket = self.get_stack_output(s3_bucket)
            print(f"[{self.NAME}]: S3 bucket/key parsed from the argument")
            print(f"[{self.NAME}]: s3_bucket={s3_bucket}, s3_key={s3_key}")
        else:
            raise Exception(
                f"[{self.NAME}]: S3 bucket/key could not be parsed nor from the argument")

        result = self.connection_manager.call(
            service="s3",
            command="head_object",
            kwargs={"Bucket": s3_bucket, "Key": s3_key},
        )

        version_id = result.get("VersionId")

        print("[{}]: object s3://{}/{} latest version: {}".format(self.NAME, s3_bucket, s3_key, version_id))

        return version_id
