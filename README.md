# mClass DYD Download Script
Script to download DYD report from commandline.

# Setup
## Prerequisites
- Python [3.9.0 or higher](https://www.python.org/downloads/)
- Filled in **config file** in YAML format
- **Username** and **Password** used to login and access DYDs

## Setting up the project
- create new virtual env `mkvirtualenv -p <path/to/python3> dyd-downloader`,
you could use any other name instead of `dyd-downloader`
- activate the env by running `workon dyd-downloader`
- run `pip install -r requirement.txt`

## Running the script
### Required Args
- `--username`: username of the user being used to download DYDs
- `--password`: password of the user being used to download DYDs
- `--config`: YAML file with config variables needed to download DYDs

### Optional Args
- `--out`: Specified file where DYDs are downloaded to. Not specifying will result in DYDs being printed in terminal

### To Run
- `python mclass_dyd_download.py --username <username here> --password <password here> -- config <config.yaml>`

This will run the script using `<username>` and `<password>` as the login and `<config.yaml>` as the configuration.
eg. python mclass_dyd_download.py --username john --password 1234 --config my_district_config.yaml


For running with an output file:
- `python mclass_dyd_download.py --username <username here> --password <password here> -- config <config.yaml> --out <output.csv>`

This will run the script in the same way as above, but additionally outputting all gathered dyds to the file `<output.csv>`.
There is an attached video demo on how to run this script that teaches how to create the yaml file.


### Example YAML File
```
"result": "download_your_data"
"users": "1234567"
"dyd_assessments": "7_32"
"dyd_results": "BM"
"years": "20"
"periods": "20_31,20_32"
"school_grouping": "3"
"districts": "1234567890,1234567891,1234567892"
"schools": "0987654321,1987654321,2987654321,3987654321"
"grades": "1,2,3,4,5,6,7,8,9,10,11,12,13,14"
"ready": "YES"
"accounts": "0123456789"
"roster_option": "2"
"assessment_groups": "1"
```

### YAML File Args

#### Variable Args
- `users`: AMP User SID (e.g.: 1234567)
- `years`: Which year (e.g.: 20)
- `periods`: TOY (Option(s): BOY: 20_31, MOY: 20_32, EOY: 20_33)
- `districts`: Inst SID for the district(s) (e.g.: 1234567890)
- `schools`: Inst SID for the school(s) (e.g.: 0987654321)
- `grades`: Grade level(s) (e.g.: 1,2,3,4,5,6,7,8,9,10,11,12,13,14)
- `accounts`: Account SID (e.g.: 123456789)

#### Static Args
- `result`: "download_your_data"
- `dyd_results`: "BM" (Results window)
- `school_grouping`: "3"
- `ready`: "YES"
- `roster_option`: "2"
- `assessment_groups`: "1"
- `dyd_assessments`: "7_32" (if you want D8 results, set to "7_D8")
