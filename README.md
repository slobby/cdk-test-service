# Test CDK Python project!

## How to run.

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Bootstraping your environment.

```
$ cdk bootstrap
```

Deploy your the app.

```
$ cdk deploy --all
```
