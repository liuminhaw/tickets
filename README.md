# tickets
#### Buy Railway tickets
Buy Taiwan railway tickets

#### Additional Requirement
`web-driver` for `selenium` need to be installed before use.

#### Configuration
Use `train_tickets.ini` to setup tickets information  
Configuration file format can be referenced in `train_template.ini`

### Version 2.0.1
- Fix select inpur problem when checking train type

#### Version 2.0.0
- Validation form auto fill
- Program period time repeat


##### Steps
- Setup `train_tickets.ini` configuration file.
- Run `tickets.py`.

##### Commands

##### tickets.py
Give target time as argument to run the program

    tickets.py YYYY-MM-DD HH:MM:SS

##### Methods
- version

##### version
Show current using version of the program

    tickets.py version
