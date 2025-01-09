# Canary Package Python

This Python package is a template designed to help create placeholder packages on public repositories (ex. PyPI). These placeholder packages trigger a Canary Token alert when installed, enabling identification of installations from public repositories. 

## How It Works

- On installation, the package sends a GET request to a Canary Token URL.
- The request includes the following details:
  - Contents of the `USER` environment variable.
  - Package name.

## File Descriptions

- `README.md`: Documentation for understanding and using the package.
- `canary_package/__init__.py`: Script that prints `"Canary Trigger for PyPI" when called.
- `setup.py`: Configuration script for building the package. During installation (e.g., `pip install canary_package`), `CustomInstallCommand` will be used and HTTP GET request is issued to a BASE64-encoded Canary Token URL, sending metadata (such as the host user and package name) to the decoded URL before completing the standard installation process.


## Usage Instructions

### Step 1: Customize the Template

1. **Rename the Package**  
   Rename the `canary_package` directory to the name of your desired package.

2. **Update the `setup.py` File**  
   Open the `setup.py` file and customize the following:  
   - **Canary URL**:  
     Replace the placeholder `BASE64_ENCODED_CANARY_URL` with the Base64-encoded version of your Canary Token URL. Use this Python snippet to generate the encoded URL:  
     ```python
     import base64
     encoded_url = base64.b64encode("<CANARY_URL>".encode()).decode()
     print(encoded_url)
     ```  
   - **Package Name**:  
     Update the `PACKAGE_NAME` variable to reflect the new package name.  
   - **Metadata**:  
     - Replace `name="<PACKAGE_NAME>"` with your package's name.  
     - Update the `author` and `author_email` fields with your information.  
     - Set the `url` field to your repository URL.

3. **Save and Proceed**  
   Save the updated `setup.py` file and continue with packaging or installation.

### Step 2: Publish the Package to PyPI

2. Build the distribution package:

```bash
python setup.py sdist
```

3. Upload the package to PyPI:

```bash
pip install twine
twine upload dist/*
```

4. Your package is now available on PyPI!

## Example Usage

The Canary Token alert will not be triggered until the package is imported in a Python script or application. For example:

```bash
pip install <PACKAGE_NAME>
```

```python
# Importing the package triggers the canary
import <PACKAGE_NAME>
```


## License

TODO: I really don't know yet and need to talk to someone about this.
