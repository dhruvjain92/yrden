
# YRDEN - AWS Security Swiss Knife

Yrden was created to ease the job of AWS Security Engineers. With easy extensible modules for incident response, analysis scripts and creation of scheduled jobs, Yrden tries to make sure your Cloud Environment is secure and gives you the tools to do so.

It is a Work In Progress and constantly been upgraded. It can be used for basic functionality that has been developed.

## Installation

A proper setup file is in our roadmap. 

For current scenario, just clone the repo,run pip and start using. Make sure to give relevant file permissions to custom-scripts and yrden.py

```bash
pip install -r requirements.txt
```

    
## Usage/Examples

```bash
python3 yrden.py --mode MODE --name PLUGIN_NAME --format FORMAT --output-file OUTPUT_FILE
```

* **MODE** - Mode refers to the functionality that is being loaded. Currently, we support 2 options:
    * ir - For Incident Response
    * plugin - For Plugin Mode

**Example for Incident Responder**
```bash
python3 yrden.py --mode ir
```

* **PLUGIN_NAME** - This is only needed when mode is *plugin*. This refers to the plugin name which is the folder name of the plugin such as *public-s3*

* **FORMAT** - Format of the output. This is only needed while using *plugin* mode. It can be json/table/file. By default, if this is not provided, table mode will be used

* **OUTPUT_FILE** - Name of the output file to store results of the plugin. This is stored in output folder.

**Example for plugin**
```bash
python3 yrden.py --mode plugin --name public-s3 --format json
python3 yrden.py --mode plugin --name public-s3 --format table
python3 yrden.py --mode plugin --name public-s3 --format file --output-file public-s3-buckets.log

# Multiple Plugins
python3 yrden.py --mode plugin --name public-s3,public-elb --format table
```



## Documentation

### Code Structure

* **core** - contains the core files for this tool
    * **configuration** - configuration for the end user that have global tool impact
    * **incidents** - contains incident response scripts. 
    * **plugin** - Plugin loader
    * **responders** - Core AWS Funcitons
* **custom-scripts** - Custom Bash scripts that invokes multiple plugins
* **integrations** - For future slack/jira or other integrations
* **output** - output files in case *format* is set as *file*
* **plugins** - contains the plugin folders

### Creating new Plugin

All plugins inherit the IPlugin class which has some abstract methods and some global methods. Currently. we have 2 abstract methods: execute and description.

We should have **description** for each plugin and give necessary credits wherever due.

**execute** is basically the main function of the plugin.

Class name of the plugin needs to be same as foolder name but with **-** as **_**.
Example: *get-public-ec2* plugin's class would be *get_public_ec2*

Each plugin can have the optional requirements.yaml file which basically takes input from the user for plugin before executing the **execute** method.

#### Structure of requirements.yaml
```yaml
---
settings:
  - name: variable_key # Key using which this value will be read
    type: string # Type of variable
    display: Please enter the bucket name # Text to show before taking user input
    value: "" # Default Value
```

**Using variable from requirements.yaml**
Value can be read using
```python
self.get_req_value("variable_key") 
```

**Pre and Post execution**
Use the following functions for pre and post execution method.

```python
# You can override this function to change post execution steps in your plugin
def post_execution(self):
    speak("After execution is called")

# You can override this function to change pre execution steps in your plugin
def pre_execution(self):
    speak("Before execution is called")
```

**Using AWS functions defined in AWS_Functions**

Plugin can use some of the already created AWS Functions from our AWS_Functions file by using:
```python
# self.AWS.FUNCTIONNAME
self.AWS.check_public_bucket(bucket_name)
```


#### User Interaction
**Printing a response**

We have created a file named assistant.py which has function speak for response. This fill will integrate logging in future. To print a response:

```python
speak("This is a default color message") # Default color text
speak("This is a green message","info") # Green color text
speak("This is a yellow message","warning") # Yellow color text
speak("This is a red message","error") # Red color text
```

**Asking for user input**

Returns string response from user

```python
ask("What is your name","warning")
```

**Asking for confirmation**

Returns true or false

```python
confirm("Do you wish to execute this?","error")
```

**Throwing error and exiting**

Exits the program and throws a red error
```python
run("Couldn't find the AWS credentials file")
```


## Roadmap

- Cron Jobs
- Incident Response Cases
- More Audit Plugins
- Slaclk/JIRA Integrations
- REST API for third party consumption
- Automatic key rotation and credentials update
- More Custom Scripts that interlink plugins and generate the results
- Reporting


## Authors

- [@dhruvjain92](https://www.github.com/dhruvjain92) - [Binobe](https://binobe.com) 


## License

[MIT](https://choosealicense.com/licenses/mit/)
