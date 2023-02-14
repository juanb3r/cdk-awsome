from os import getenv

import aws_cdk as cdk
from aws_cdk import (
    Stack,
)
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct
from my_pipeline.my_pipeline_app_stage import MyPipelineAppStage


class MyPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = CodePipeline(
            self,
            "Pipeline",
            pipeline_name="MyPipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(
                    "juanb3r/cdk-awsome",
                    "master",
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        pipeline.add_stage(
            MyPipelineAppStage(
                self,
                "test",
                env=cdk.Environment(
                    account=getenv('CDK_DEFAULT_ACCOUNT'),
                    region=getenv('CDK_DEFAULT_REGION')
                )
            )
        )
