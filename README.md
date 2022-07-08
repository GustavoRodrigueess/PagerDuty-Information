# Information PagerDuty

The information PagerDuty is for situations where you need to check all the statistics returned by PagerDuty quickly. That is, you run the script, it pulls all the information from the last (x) days, it's your choice, with several fields.

With all this data we return a worksheet in the same folder where the script is running.

# How to Use? 

- First of all, have your token in hand.
> How do I get access to my token?
    - You can access your token in the keys tab inside My Account on PagerDuty

- I recommend that you run the file in Google Collab. Since you have it you will only need to copy and paste the code, without downloading anything.

### But I want to download the script on my machine, how to proceed?

- Download, unzip the file and run the following command (with the terminal inside the folder)

> For Linux
```
python3 pagerduty.py
```

> For Windows
- Downloading Libraries
```
python -m pip install DateTime
python -m pip install requests
python pip install os-sys
python pip install syspath
```
- Running Script
```
python pagerduty.py
```

# What columns are generated in CSV?

- incident_number
- title
- description
- created_at
- status
- summary
- type
- urgency
- service-summary
- Event date
- Event host
- Event host ip
- Event tags
- Event time
- Trigger opdata
- check_id
- check_name
- hostname
- long_description
- tags
- Total Records
- uptime_173
- uptime_174
- avg
- Trigger description

# License 

MIT License