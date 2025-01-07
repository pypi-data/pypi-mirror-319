## 2.0.0b1 (2025-01-07)

## 2.0.0b0 (2025-01-06)

### Feat

- **add_convenience_data.py**: add schoolpsy_address_multiline to convenience data

### Fix

- handle the fact that config_path is a list not a string
- **sampleconfig.yml**: change the field name for uid from uid to app_uid

### Refactor

- **clients.py**: add nta arguments to the constructor for clients
- **test_encrypt.py**: use the mock_config fixture from conftest.py

## 1.0.0b0 (2025-01-04)

### BREAKING CHANGE

- new_client --csv now requires a --name argument

### Feat

- handle the extraction of a student from a webuntis csv with several rows

### Fix

- **encrypt.py**: don't load the config file in encrypt.py
- **cli.py**: handle config files correctly
- **cli.py**: catch KeyError exception when no app_username is set

### Refactor

- remove redundant scripts
- **fill_form.py**: raise FileNotFoundError
- refactor tests
- mock keyring for testing
- use importlib.resources.files instead of deprecated path
- **pyproject.toml**: change name of dependency group to bwbackend

## 1.0.0 (2025-01-06)

### Fix

- handle the fact that config_path is a list not a string

## 1.0.0b1 (2025-01-06)

### Feat

- **add_convenience_data.py**: add schoolpsy_address_multiline to convenience data

### Fix

- **sampleconfig.yml**: change the field name for uid from uid to app_uid

### Refactor

- **clients.py**: add nta arguments to the constructor for clients
- **test_encrypt.py**: use the mock_config fixture from conftest.py

## 1.0.0b0 (2025-01-04)

### BREAKING CHANGE

- new_client --csv now requires a --name argument

### Feat

- handle the extraction of a student from a webuntis csv with several rows

### Fix

- **encrypt.py**: don't load the config file in encrypt.py
- **cli.py**: handle config files correctly
- **cli.py**: catch KeyError exception when no app_username is set

### Refactor

- remove redundant scripts
- **fill_form.py**: raise FileNotFoundError
- refactor tests
- mock keyring for testing
- use importlib.resources.files instead of deprecated path
- **pyproject.toml**: change name of dependency group to bwbackend

## 1.0.0a2 (2024-12-19)

### Fix

- do input validation for school
- **managers.py**: normalize form paths
- use form_paths variable name consistently
- **cli.py**: make form_paths optional in create documentation
- **taetigkeitsbericht_from_db.py**: set pdflibs_imported when the libraries can be imported
- **add_convenience_data.py**: correct wrong dict key

## 1.0.0a1 (2024-12-16)

### Fix

- **teatigkeitsbericht_from_db.py**: make dataframe_image and fpdf truly optional
- change version in __version__.py back to string

### Refactor

- remove superfluous version from pyproject.toml

## 1.0.0a0 (2024-12-15)

### BREAKING CHANGE

- You will need to add schoolpsy data to your config.yml. See
the sampleconfig.yml in ./data/
- This will break imports and shellscripts that call edupsy_admin instead of edupsyadmin. This also changes the config path and the data path.

### Feat

- **add_convenience_data.py**: set nta_font to True if lrst_diagnosis is lrst or iLst
- accept sets of form files from config and add schoolpsy convenience data
- **cli.py**: copy sample config if config.yml does not exist
- add a flatten_pdfs function

### Fix

- **core**: explicitly set the encoding for config files to UTF-8
- change default and type hint for encrypted variables

### Refactor

- **.gitignore**: ignore .pypirc
- move code for creation of sample pdf to separate file
- update readme with new project name
- change the project name
- move the test.sqlite db to tmp_path
