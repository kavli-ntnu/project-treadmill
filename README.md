# project-treadmill
Repository for *Treadmill tracking* as part of the ***Secondary Tracking***.

The *Treadmill* tracking data are extracted from Optitrack file (opti.csv) - from a column named "Treadmill".

## Setup and installation

### Step 1 - cloning the ***project-treadmill***
The first step for new users is to fork the ***project-treadmill*** from kvali GitHub repository ([here](https://github.com/kavli-ntnu/project-treadmill)) to their own GitHub account

Then users can clone the ***project-treadmill*** from their github fork to the local computer:

+ Launch a new terminal and change directory to where you want to clone the repository to
    ```
    cd C:/Projects
    ```
+ Clone the repository:
    ```
    clone https://github.com/your_github_username/project-treadmill.git 
    ```
+ Change directory to ***project-treadmill***
    ```
    cd project-treadmill
    ```

### Step 2 - setup virtual environment
It is highly recommended (though not strictly required) to create a virtual environment to run the pipeline.
+ To create a new virtual environment named ***venv***:
    ```
    virtualenv venv
    ```
+ To activated the virtual environment:
    + On Windows:
        ```
        .\venv\Scripts\activate
        ```
    + On Linux/macOS:
        ```
        source venv/bin/activate
        ```
*note: if `virtualenv` not yet installed, do `pip install --user virtualenv`*

### Step 3 - Installation of the Moser ephys pipeline
Installing (or updating) the ***dj-elphys*** repository:

    pip install git+https://github.com/kavli-ntnu/dj-elphys.git
    
To update to the latest version:
  
    pip install git+https://github.com/kavli-ntnu/dj-elphys.git --upgrade
    
### Step 4 - Configure the ***dj_local_conf.json***:
In the ***project-treadmill*** directory, create a new json file named ***dj_local_conf.json*** and add the following content:

```json
{
    "database.host": "datajoint.it.ntnu.no",
    "database.user": "username",
    "database.password": "password",
    "database.port": 3306,
    "connection.init_function": null,
    "database.reconnect": true,
    "enable_python_native_blobs": true,
    "loglevel": "INFO",
    "safemode": true,
    "display.limit": 7,
    "display.width": 14,
    "display.show_tuple_count": true,
    "secure_s3": true,
    "stores":
        {
        "ephys_store":
            {
            "protocol": "s3",
            "endpoint": "s3.stack.it.ntnu.no:443",
            "access_key": "**********",
            "secret_key": "**********",
            "bucket": "ephys-store-computed",
            "secure": true,
            "location": ""
            },
        "ephys_store_manual":
            {
            "protocol": "s3",
            "endpoint": "s3.stack.it.ntnu.no:443",
            "access_key": "**********",
            "secret_key": "**********",
            "bucket": "ephys-store-manual",
            "secure": true,
            "location": ""
            }
        },
    "custom":
    {
        "database.prefix": "group_shared_",
        "project.db.prefix": "project_",
        "mlims.database": "prod_mlims_data",
        "flask.database": "group_shared_flask",
        "drive_config":
        {
          "local": "/data",
          "network": "/mnt/N"
        }
	}
}
```

Make sure to specify the ***project.db.prefix*** correctly (if you're unsure, contact the pipeline administrator)

For database credentials, or access key and secret key to the *ephys stores*, contact your administrator.


