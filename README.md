# booking
Automation daily booking process
- sport-center (badminton)

## Version 3.1.1-gcp
- Automatically deploy running program to gcp compute engine

#### Version 3.1.1
- New feature `--free`: free court check on specific date and section
- New feature `--freetime`: free court check on specific date and time
- Config setting: DRIVER -> driver-count
- Config setting: DRIVER -> execution-delta
- Config setting: DRIVER -> headless mode
- Config setting: DRIVER -> submit-time-sleep
- Config setting: DRIVER -> submit-time-offset
- Config setting: DRIVER -> driver-time-sleep

#### Version 3.1.0a
- fix issue #1 wrong logger function

#### Version 3.1.0
- Double browsers submit chance
- Test and add use headless mode with selenium
- Fetch and show booking result
- Update setup with config template 
- Check for credential file existence 

#### Version 3.0.0
- Daan sport center bandminton booking process automation

## Requirements
#### GCP Vision API 
Solve login captcha using GCP Vision API
- [Vision API prep](https://cloud.google.com/vision/docs/before-you-begin)
    - Service account credential to use API service (default: `credential.json`)
- [Vision API reference](https://cloud.google.com/vision/docs/ocr#vision_text_detection-python)

#### GCP Compute Engine
Deploying and run booking program on gcp cloud compute
- `gcloud` command installed
- machine image on gcp
    - `google-chrome` installed: [reference](https://hackmd.io/@liuminhaw/chrome)
    - selenium `chromedriver` installed: [reference](https://hackmd.io/@liuminhaw/chrome)
    - `tmux` command installed
```bash
./run-gcp.sh
```

## Usage
```bash
usage: booking.py [-h] [-c CONFIG] [--free] [--freetime] [-V] {daan-sport}

positional arguments:
  {daan-sport}          Booking running type

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Specify configuration file
  --free                Show available courts
  --freetime            Test free court at specific time
  -V, --version         show program's version number and exit
```

#### Run on gcp compute engine
First fill in configuration data `gcp_template` directory, then execute script
```bash
./run-gcp.sh
```

#### Setup
```bash
./setup.sh DESTINATION
```


## Error Code
`11` - `conf_mod` ConfigNotFoundError  
`12` - `conf_mod` NoSectionError  
`13` - `conf_mod` NoOptionError  
`14` - `conf_mod` OptionFormatError  
`15` - `conf_mod` FileNotFoundError
`21` - `booking_lib` NoMatchTextError  
`31` - `driver` FindElementError  

