
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
- [Notion Documentation for Yrden](https://binobe.notion.site/Yrden-4a5a7a6c3220436d88ce8fa1914af734)


## Authors

- [@dhruvjain92](https://www.github.com/dhruvjain92) - [Binobe](https://binobe.com) 


## License

[MIT](https://choosealicense.com/licenses/mit/)
