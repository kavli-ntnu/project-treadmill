# project-treadmill
Repository for *Treadmill tracking* as part of the ***Secondary Tracking***.

The *Treadmill* tracking data are extracted from Optitrack file (opti.csv) - from a column named "Treadmill".

Requires installation of the Moser ephys pipeline - ***dj-elphys*** repo:

    pip install git+https://github.com/kavli-ntnu/dj-elphys.git
    
Configure the ***dj_local_conf.json***:

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
        "project.db.prefix": "some_prefix_for_secondary_tracking_shema",
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

