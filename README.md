# Welcome to your CDK Python project!

##Prerequisite
This package uses AWS CDK for deployment of resources. Please refer to these [instructions](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) for installing CDK.

##Instructions

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

Package contains a file cdk.context.json. It has two properties - brokerid and vpcid. The brokerid represents the RabbitMQ cluster that you currently for which we need to create a NLB facade. The vpcid represents the vpc in which the broker vpc endpoint is created or simply that vpc that you used when deploying the broker.

1. Update the file with your broker id and vpc id.
1. At this point you can now synthesize the CloudFormation template for this code.

    ```
    $ cdk synth
    ```
    You will notice that it will output a cloudformation template that will provision the NLB.
1. You can now run the cdk deployment to create NLB.
    ```
    cdk deploy
    ```
1. The output of the deployment will show a property NLBArn. The value of this property will be used in the SAM template that creates the resources needed to update the target group of this NLB during new broker deployment.
