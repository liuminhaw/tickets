# booking
Automation daily booking process
- sport-center (badminton)

## Version 3.0.0
- Daan sport center bandminton booking process automation

## Requirements
#### GCP Vision API 
Solve login captcha using GCP Vision API
- [Vision API prep](https://cloud.google.com/vision/docs/before-you-begin)
    - Service account credential to use API service (default: `credential.json`)
- [Vision API reference](https://cloud.google.com/vision/docs/ocr#vision_text_detection-python)


## Usage
```bash
usage: booking.py [-h] [-c CONFIG] [-V] {daan-sport}

positional arguments:
  {daan-sport}          Booking running type

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Specify configuration file
  -V, --version         show program's version number and exit
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

