1. Clone git repository
git clone https://github.com/trainosoft/energy-tariff-calculation-engine-service.git

2. Swith on dev branch
D:\rutusoft\energy-tariff-calculation-engine-service>git switch dev
Switched to branch 'dev'

3. Verify you are on dev branch
D:\rutusoft\energy-tariff-calculation-engine-service>git branch
* dev
  main
4. Create virtual env
D:\rutusoft\energy-tariff-calculation-engine-service>python -m venv venv

5. Activate virtual environment
D:\rutusoft\energy-tariff-calculation-engine-service>venv\Scripts\activate

(venv) D:\rutusoft\energy-tariff-calculation-engine-service>

6. Install dependencies
(venv) D:\rutusoft\energy-tariff-calculation-engine-service>pip install -r requirements.txt

7. Run your app
(venv) D:\rutusoft\energy-tariff-calculation-engine-service>uvicorn main:app --reload



Opta
---------------------------
D:\rutusoft\energy-tariff-calculation-engine-service>py --list
 -V:3.13 *        Python 3.13 (64-bit)
 -V:3.11          Python 3.11 (64-bit)

D:\rutusoft\energy-tariff-calculation-engine-service>py -3.11 -m venv venv
D:\rutusoft\energy-tariff-calculation-engine-service>venv\Scripts\activate
(venv) D:\rutusoft\energy-tariff-calculation-engine-service>pip install -r requirements.txt
(venv) D:\rutusoft\energy-tariff-calculation-engine-service>uvicorn main:app --reload

Deploy on linux VM

Login to VM:
ssh root@147.93.28.130
root@147.93.28.130's password: Hello@Nov2025
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.8.0-87-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Sun Nov 23 04:25:15 UTC 2025

  System load:  0.0               Processes:             127
  Usage of /:   5.1% of 95.82GB   Users logged in:       0
  Memory usage: 10%               IPv4 address for eth0: 147.93.28.130
  Swap usage:   0%                IPv6 address for eth0: 2a02:4780:12:8c39::1


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


1 updates could not be installed automatically. For more details,
see /var/log/unattended-upgrades/unattended-upgrades.log

*** System restart required ***
Last login: Sun Nov 23 04:17:43 2025 from 103.240.204.236
root@srv1139088:~#
root@srv1139088:~# pwd
/root
root@srv1139088:/# cd home/
root@srv1139088:/# cd home/
root@srv1139088:/home# ls
mcp-admin  ubuntu
root@srv1139088:/home# sudo apt update
Hit:1 https://download.docker.com/linux/ubuntu noble InRelease
Hit:2 http://mirror.cse.iitk.ac.in/ubuntu noble-backports InRelease
Hit:3 http://mirror.cse.iitk.ac.in/ubuntu noble InRelease
Hit:4 http://mirror.cse.iitk.ac.in/ubuntu noble-security InRelease
Hit:5 http://archive.ubuntu.com/ubuntu noble InRelease
Hit:6 http://mirror.cse.iitk.ac.in/ubuntu noble-updates InRelease
Hit:7 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:8 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Hit:9 https://repository.monarx.com/repository/ubuntu-noble noble InRelease
Hit:10 http://archive.ubuntu.com/ubuntu noble-security InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
1 package can be upgraded. Run 'apt list --upgradable' to see it.


root@srv1139088:/home# sudo apt install nginx -y
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  nginx-common
Suggested packages:
  fcgiwrap nginx-doc ssl-cert
The following NEW packages will be installed:
  nginx nginx-common
0 upgraded, 2 newly installed, 0 to remove and 1 not upgraded.
Need to get 564 kB of archives.
After this operation, 1596 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 nginx-common all 1.24.0-2ubuntu7.5 [43.4 kB]
Get:2 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 nginx amd64 1.24.0-2ubuntu7.5 [520 kB]
Fetched 564 kB in 2s (324 kB/s)
Preconfiguring packages ...
Selecting previously unselected package nginx-common.
(Reading database ... 106767 files and directories currently installed.)
Preparing to unpack .../nginx-common_1.24.0-2ubuntu7.5_all.deb ...
Unpacking nginx-common (1.24.0-2ubuntu7.5) ...
Selecting previously unselected package nginx.
Preparing to unpack .../nginx_1.24.0-2ubuntu7.5_amd64.deb ...
Unpacking nginx (1.24.0-2ubuntu7.5) ...
Setting up nginx-common (1.24.0-2ubuntu7.5) ...
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /usr/lib/systemd/system/nginx.service.
Could not execute systemctl:  at /usr/bin/deb-systemd-invoke line 148.
Setting up nginx (1.24.0-2ubuntu7.5) ...
Not attempting to start NGINX, port 80 is already in use.
Processing triggers for man-db (2.12.0-4build2) ...
Processing triggers for ufw (0.36.2-6) ...
Scanning processes...
Scanning candidates...
Scanning linux images...

Pending kernel upgrade!
Running kernel version:
  6.8.0-87-generic
Diagnostics:
  The currently running kernel version is not the expected kernel version 6.8.0-88-generic.

Restarting the system to load the new kernel will not be handled automatically, so you should consider rebooting.

Restarting services...

Service restarts being deferred:
 systemctl restart unattended-upgrades.service

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
root@srv1139088:/home#

You can verify:
root@srv1139088:/home# which nginx
/usr/sbin/nginx
root@srv1139088:/home#


As port 80 is already beeen used by docker, we need to change default port of nginx from 80 to 8080

server {
	listen 8080 default_server;
	listen [::]:8080 default_server;

	root /var/www/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
        	proxy_pass http://127.0.0.1:8000;

		proxy_set_header Host $host;
        	proxy_set_header X-Real-IP $remote_addr;
        	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        	proxy_set_header X-Forwarded-Proto $scheme;
        	try_files $uri /index.html;
    	}
}

root@srv1139088:/etc/nginx/sites-enabled# sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

Navigate to /etc/nginx/sites-enabled to edit chage port configuration
root@srv1139088:/home# cd /etc/nginx/sites-enabled
root@srv1139088:/etc/nginx/sites-enabled# ls
default
root@srv1139088:/etc/nginx/sites-enabled#nano default

Test Nginx config
root@srv1139088:/etc/nginx/sites-enabled# sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

Restart nginx
root@srv1139088:/etc/nginx/sites-enabled# sudo systemctl restart nginx
root@srv1139088:/etc/nginx/sites-enabled#

Verify Nginx is listening on new port 8080
root@srv1139088:/etc/nginx/sites-enabled# sudo ss -tulpn | grep nginx
tcp   LISTEN 0      511          0.0.0.0:8080       0.0.0.0:*    users:(("nginx",pid=61370,fd=5),("nginx",pid=61369,fd=5),("nginx",pid=61368,fd=5))
tcp   LISTEN 0      511             [::]:8080          [::]:*    users:(("nginx",pid=61370,fd=6),("nginx",pid=61369,fd=6),("nginx",pid=61368,fd=6))

Access nginx welcome page:
http://147.93.28.130:8080/


Copy python code to nginx
root@srv1139088:/var/www# mkdir energy-tariff-calculation-engine-service

root@srv1139088:/var/www/energy-tariff-calculation-engine-service# python3 -m venv venv
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.12-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: /var/www/energy-tariff-calculation-engine-service/venv/bin/python3

root@srv1139088:/var/www/energy-tariff-calculation-engine-service# apt install python3.12-venv
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  python3-pip-whl python3-setuptools-whl
The following NEW packages will be installed:
  python3-pip-whl python3-setuptools-whl python3.12-venv
0 upgraded, 3 newly installed, 0 to remove and 1 not upgraded.
Need to get 2429 kB of archives.
After this operation, 2777 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3-pip-whl all 24.0+dfsg-1ubuntu1.3 [1707 kB]
Get:2 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3-setuptools-whl all 68.1.2-2ubuntu1.2 [716 kB]
Get:3 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3.12-venv amd64 3.12.3-1ubuntu0.8 [5678 B]
Fetched 2429 kB in 2s (1517 kB/s)
Selecting previously unselected package python3-pip-whl.
(Reading database ... 106815 files and directories currently installed.)
Preparing to unpack .../python3-pip-whl_24.0+dfsg-1ubuntu1.3_all.deb ...
Unpacking python3-pip-whl (24.0+dfsg-1ubuntu1.3) ...
Selecting previously unselected package python3-setuptools-whl.
Preparing to unpack .../python3-setuptools-whl_68.1.2-2ubuntu1.2_all.deb ...
Unpacking python3-setuptools-whl (68.1.2-2ubuntu1.2) ...
Selecting previously unselected package python3.12-venv.
Preparing to unpack .../python3.12-venv_3.12.3-1ubuntu0.8_amd64.deb ...
Unpacking python3.12-venv (3.12.3-1ubuntu0.8) ...
Setting up python3-setuptools-whl (68.1.2-2ubuntu1.2) ...
Setting up python3-pip-whl (24.0+dfsg-1ubuntu1.3) ...
Setting up python3.12-venv (3.12.3-1ubuntu0.8) ...
Scanning processes...
Scanning candidates...
Scanning linux images...

Pending kernel upgrade!
Running kernel version:
  6.8.0-87-generic
Diagnostics:
  The currently running kernel version is not the expected kernel version 6.8.0-88-generic.

Restarting the system to load the new kernel will not be handled automatically, so you should consider rebooting.

Restarting services...

Service restarts being deferred:
 systemctl restart unattended-upgrades.service

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.

root@srv1139088:/var/www/energy-tariff-calculation-engine-service# python3 -m venv venv

activate venv
root@srv1139088:/var/www/energy-tariff-calculation-engine-service# source venv/bin/activate
(venv) root@srv1139088:/var/www/energy-tariff-calculation-engine-service#

install dependencies
(venv) root@srv1139088:/var/www/energy-tariff-calculation-engine-service# pip install -r requirements.txt

Create a systemd Service for FastAPI (Gunicorn + Uvicorn workers)
root@srv1139088:/etc/nginx/sites-enabled# sudo nano /etc/systemd/system/energy.service

[Unit]
Description=Energy Tariff Calculation Engine FastAPI
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/energy-tariff-calculation-engine-service
Environment="PATH=/var/www/energy-tariff-calculation-engine-service/venv/bin"
ExecStart=/var/www/energy-tariff-calculation-engine-service/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target


Reload systemd & Start the service
sudo systemctl daemon-reload
sudo systemctl start energy
sudo systemctl enable energy
sudo systemctl status energy

nginx: configuration file /etc/nginx/nginx.conf test is successful
(venv) root@srv1139088:/var/www/energy-tariff-calculation-engine-service# sudo systemctl reload nginx
(venv) root@srv1139088:/var/www/energy-tariff-calculation-engine-service# sudo systemctl daemon-reload
(venv) root@srv1139088:/var/www/energy-tariff-calculation-engine-service# sudo systemctl start energy
(venv) root@srv1139088:/var/www/energy-tariff-calculation-engine-service# sudo systemctl enable energy
(venv) root@srv1139088:/var/www/energy-tariff-calculation-engine-service# sudo systemctl status energy
● energy.service - Energy Tariff Calculation Engine FastAPI
     Loaded: loaded (/etc/systemd/system/energy.service; enabled; preset: enabled)
     Active: active (running) since Sun 2025-11-23 05:48:56 UTC; 17min ago
   Main PID: 62472 (gunicorn)
      Tasks: 3 (limit: 9484)
     Memory: 46.3M (peak: 46.6M)
        CPU: 2.348s
     CGroup: /system.slice/energy.service
             ├─62472 /var/www/energy-tariff-calculation-engine-service/venv/bin/python3 /var/www/energy-tariff-calculation-engine-service/venv/bin/gunicorn -k uvicorn.wo>
             └─62473 /var/www/energy-tariff-calculation-engine-service/venv/bin/python3 /var/www/energy-tariff-calculation-engine-service/venv/bin/gunicorn -k uvicorn.wo>

Nov 23 05:48:56 srv1139088 gunicorn[62472]: [2025-11-23 05:48:56 +0000] [62472] [INFO] Listening at: http://127.0.0.1:8000 (62472)
Nov 23 05:48:56 srv1139088 gunicorn[62472]: [2025-11-23 05:48:56 +0000] [62472] [INFO] Using worker: uvicorn.workers.UvicornWorker
Nov 23 05:48:56 srv1139088 gunicorn[62473]: [2025-11-23 05:48:56 +0000] [62473] [INFO] Booting worker with pid: 62473
Nov 23 05:48:56 srv1139088 gunicorn[62473]: [2025-11-23 05:48:56 +0000] [62473] [INFO] Started server process [62473]
Nov 23 05:48:56 srv1139088 gunicorn[62473]: [2025-11-23 05:48:56 +0000] [62473] [INFO] Waiting for application startup.
Nov 23 05:48:56 srv1139088 gunicorn[62473]: [2025-11-23 05:48:56 +0000] [62473] [INFO] Application startup complete.
Nov 23 05:56:27 srv1139088 gunicorn[62473]: 2025-11-23 05:56:27,341 - INFO - 62473 - [main.log_origin:18] - request_id=None trace_id=None - Request from origin: None
Nov 23 05:56:27 srv1139088 gunicorn[62473]: 2025-11-23 05:56:27,342 - INFO - 62473 - [main.log_origin:19] - request_id=None trace_id=None - FASTAPI --> POST /calculate-t>
Nov 23 05:56:27 srv1139088 gunicorn[62473]: 2025-11-23 05:56:27,343 - INFO - 62473 - [electricityRarrifCcalculation.evaluateTarrifCalcaulationRules:14] - request_id=None>
Nov 23 05:56:27 srv1139088 gunicorn[62473]: 2025-11-23 05:56:27,348 - INFO - 62473 - [electricityRarrifCcalculation.evaluateTarrifCalcaulationRules:29] - request_id=None>
lines 1-21/21 (END)


Run decision table through REST API

curl --location 'http://localhost:8000/calculate-tarrif/evaluate?decision_table_key=MIZO-FY-24-25.json' \
--header 'Content-Type: application/json' \
--data '{
  "category":"Domestic",
  "subcategory":"LT",
  "units_consumed":86,
  "contracted_load":0.500,
  "connected_load":0.500,
  "days":23,
  "meter_rent":0.00,
  "adjustment":-0.87
}'

Response:
{
    "performance": "362.1µs",
    "result": {
        "adjustment": -0.87,
        "arrears": 0,
        "category": "Domestic",
        "connected_load": 0.5,
        "contracted_load": 0.5,
        "days": 23,
        "fix_charge_rate_per_kw_per_month": 50,
        "meter_rent": 0,
        "pf_rebate": 0,
        "pole_usage_charge": 0,
        "rebate": 0,
        "slab_1_rate_per_unit": 9.53,
        "slab_1_subsidized_rate_per_unit": 4.9,
        "slab_1_subsidized_total_rate": 421.4,
        "slab_1_total_rate": 819.58,
        "slab_2_rate_per_unit": 13.81,
        "slab_2_subsidized_rate_per_unit": 7.1,
        "slab_2_subsidized_total_rate": 0,
        "slab_2_total_rate": 0,
        "slab_3_rate_per_unit": 15.94,
        "slab_3_subsidized_rate_per_unit": 8.2,
        "slab_3_subsidized_total_rate": 0,
        "slab_3_total_rate": 0,
        "subcategory": "LT",
        "subsidized_fix_charge_rate_per_kw_per_month": 50,
        "subsidy_on_energy_charge": -438.09,
        "surcharge": 0,
        "surcharge_on_outstanding_principal": 8.79,
        "total_bill_amount_payable": 439.7,
        "total_bill_amount_payable_after_due_date": 448.49,
        "total_energry_charge": 859.49,
        "total_fix_charge": 19.17,
        "total_subsidized_energry_charge": 421.4,
        "transformation_loss_percent": 4.87,
        "units_consumed": 86,
        "units_slab_1": 86,
        "units_slab_2": 0,
        "units_slab_3": 0
    }
}


curl --location 'http://localhost:8000/calculate-tarrif/evaluate?decision_table_key=MIZO-FY-24-25.json' \
--header 'Content-Type: application/json' \
--data '{
  "category":"Domestic",
  "subcategory":"HT",
  "units_consumed":528,
  "contracted_load":10.000,
  "connected_load":10.000,
  "days":23,
  "meter_rent":0.00,
  "adjustment":-0.93
}'

Response:
{
    "performance": "280.9µs",
    "result": {
        "adjustment": -0.93,
        "arrears": 0,
        "category": "Domestic",
        "connected_load": 10,
        "contracted_load": 10,
        "days": 23,
        "fix_charge_rate_per_kw_per_month": 50,
        "meter_rent": 0,
        "pf_rebate": 0,
        "pole_usage_charge": 0,
        "rate_per_unit": 10.6,
        "rebate": 0,
        "subcategory": "HT",
        "subsidized_fix_charge_rate_per_kw_per_month": 50,
        "subsidized_rate_per_unit": 8.65,
        "subsidy_on_energy_charge": -1029.6,
        "surcharge": 0,
        "surcharge_on_outstanding_principal": 98.99,
        "total_bill_amount_payable": 4949.6,
        "total_bill_amount_payable_after_due_date": 5048.59,
        "total_energry_charge": 5596.8,
        "total_fix_charge": 383.33,
        "total_subsidized_energry_charge": 4567.2,
        "units_consumed": 528
    }
}


curl --location 'http://147.93.28.130:8080/calculate-tarrif/evaluate?decision_table_key=MIZO-FY-24-25.json' \
--header 'Content-Type: application/json' \
--data '{
  "category":"Domestic",
  "subcategory":"HT",
  "units_consumed":528,
  "contracted_load":10.000,
  "connected_load":10.000,
  "days":23,
  "meter_rent":0.00,
  "adjustment":-0.93
}'

Response:
{
    "performance": "188.0µs",
    "result": {
        "adjustment": -0.93,
        "arrears": 0,
        "category": "Domestic",
        "connected_load": 10,
        "contracted_load": 10,
        "days": 23,
        "fix_charge_rate_per_kw_per_month": 50,
        "meter_rent": 0,
        "pf_rebate": 0,
        "pole_usage_charge": 0,
        "rate_per_unit": 10.6,
        "rebate": 0,
        "subcategory": "HT",
        "subsidized_fix_charge_rate_per_kw_per_month": 50,
        "subsidized_rate_per_unit": 8.65,
        "subsidy_on_energy_charge": -1029.6,
        "surcharge": 0,
        "surcharge_on_outstanding_principal": 98.99,
        "total_bill_amount_payable": 4949.6,
        "total_bill_amount_payable_after_due_date": 5048.59,
        "total_energry_charge": 5596.8,
        "total_fix_charge": 383.33,
        "total_subsidized_energry_charge": 4567.2,
        "units_consumed": 528
    }
}


curl --location 'http://147.93.28.130:8080/calculate-tarrif/evaluate?decision_table_key=MIZO-FY-24-25.json' \
--header 'Content-Type: application/json' \
--data '{
  "category":"Domestic",
  "subcategory":"LT",
  "units_consumed":86,
  "contracted_load":0.500,
  "connected_load":0.500,
  "days":23,
  "meter_rent":0.00,
  "adjustment":-0.87
}'

Response:
{
    "performance": "263.5µs",
    "result": {
        "adjustment": -0.87,
        "arrears": 0,
        "category": "Domestic",
        "connected_load": 0.5,
        "contracted_load": 0.5,
        "days": 23,
        "fix_charge_rate_per_kw_per_month": 50,
        "meter_rent": 0,
        "pf_rebate": 0,
        "pole_usage_charge": 0,
        "rebate": 0,
        "slab_1_rate_per_unit": 9.53,
        "slab_1_subsidized_rate_per_unit": 4.9,
        "slab_1_subsidized_total_rate": 421.4,
        "slab_1_total_rate": 819.58,
        "slab_2_rate_per_unit": 13.81,
        "slab_2_subsidized_rate_per_unit": 7.1,
        "slab_2_subsidized_total_rate": 0,
        "slab_2_total_rate": 0,
        "slab_3_rate_per_unit": 15.94,
        "slab_3_subsidized_rate_per_unit": 8.2,
        "slab_3_subsidized_total_rate": 0,
        "slab_3_total_rate": 0,
        "subcategory": "LT",
        "subsidized_fix_charge_rate_per_kw_per_month": 50,
        "subsidy_on_energy_charge": -438.09,
        "surcharge": 0,
        "surcharge_on_outstanding_principal": 8.79,
        "total_bill_amount_payable": 439.7,
        "total_bill_amount_payable_after_due_date": 448.49,
        "total_energry_charge": 859.49,
        "total_fix_charge": 19.17,
        "total_subsidized_energry_charge": 421.4,
        "transformation_loss_percent": 4.87,
        "units_consumed": 86,
        "units_slab_1": 86,
        "units_slab_2": 0,
        "units_slab_3": 0
    }
}

Opta REST APIs
----------------------------------------------------------------
curl --location 'http://127.0.0.1:8000/optapy/solve' \
--header 'Content-Type: application/json' \
--data '{
    "timeslot_list": [
        {
            "id": 1,
            "day_of_week": "MONDAY",
            "start_time": "08:30:00",
            "end_time": "09:30:00"
        },
        {
            "id": 2,
            "day_of_week": "MONDAY",
            "start_time": "09:30:00",
            "end_time": "10:30:00"
        },
        {
            "id": 3,
            "day_of_week": "MONDAY",
            "start_time": "10:30:00",
            "end_time": "11:30:00"
        },
        {
            "id": 4,
            "day_of_week": "MONDAY",
            "start_time": "13:30:00",
            "end_time": "14:30:00"
        },
        {
            "id": 5,
            "day_of_week": "MONDAY",
            "start_time": "14:30:00",
            "end_time": "15:30:00"
        },
        {
            "id": 6,
            "day_of_week": "TUESDAY",
            "start_time": "08:30:00",
            "end_time": "09:30:00"
        },
        {
            "id": 7,
            "day_of_week": "TUESDAY",
            "start_time": "09:30:00",
            "end_time": "10:30:00"
        },
        {
            "id": 8,
            "day_of_week": "TUESDAY",
            "start_time": "10:30:00",
            "end_time": "11:30:00"
        },
        {
            "id": 9,
            "day_of_week": "TUESDAY",
            "start_time": "13:30:00",
            "end_time": "14:30:00"
        },
        {
            "id": 10,
            "day_of_week": "TUESDAY",
            "start_time": "14:30:00",
            "end_time": "15:30:00"
        }
    ],
    "room_list": [
        {
            "id": 1,
            "name": "Room A"
        },
        {
            "id": 2,
            "name": "Room B"
        },
        {
            "id": 3,
            "name": "Room C"
        }
    ],
    "lesson_list": [
        {
            "id": 1,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 2,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 3,
            "subject": "Physics",
            "teacher": "M. Curie",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 4,
            "subject": "Chemistry",
            "teacher": "M. Curie",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 5,
            "subject": "Biology",
            "teacher": "C. Darwin",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 6,
            "subject": "History",
            "teacher": "I. Jones",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 7,
            "subject": "English",
            "teacher": "I. Jones",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 8,
            "subject": "English",
            "teacher": "I. Jones",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 9,
            "subject": "Spanish",
            "teacher": "P. Cruz",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 10,
            "subject": "Spanish",
            "teacher": "P. Cruz",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 11,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 12,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 13,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 14,
            "subject": "Physics",
            "teacher": "M. Curie",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 15,
            "subject": "Chemistry",
            "teacher": "M. Curie",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 16,
            "subject": "French",
            "teacher": "M. Curie",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 17,
            "subject": "Geography",
            "teacher": "C. Darwin",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 18,
            "subject": "History",
            "teacher": "I. Jones",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 19,
            "subject": "English",
            "teacher": "P. Cruz",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 20,
            "subject": "Spanish",
            "teacher": "P. Cruz",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        }
    ]
}'

Response:
{
    "solution": {
        "timeslot_list": [
            {
                "id": 1,
                "day_of_week": "MONDAY",
                "start_time": "08:30:00",
                "end_time": "09:30:00"
            },
            {
                "id": 2,
                "day_of_week": "MONDAY",
                "start_time": "09:30:00",
                "end_time": "10:30:00"
            },
            {
                "id": 3,
                "day_of_week": "MONDAY",
                "start_time": "10:30:00",
                "end_time": "11:30:00"
            },
            {
                "id": 4,
                "day_of_week": "MONDAY",
                "start_time": "13:30:00",
                "end_time": "14:30:00"
            },
            {
                "id": 5,
                "day_of_week": "MONDAY",
                "start_time": "14:30:00",
                "end_time": "15:30:00"
            },
            {
                "id": 6,
                "day_of_week": "TUESDAY",
                "start_time": "08:30:00",
                "end_time": "09:30:00"
            },
            {
                "id": 7,
                "day_of_week": "TUESDAY",
                "start_time": "09:30:00",
                "end_time": "10:30:00"
            },
            {
                "id": 8,
                "day_of_week": "TUESDAY",
                "start_time": "10:30:00",
                "end_time": "11:30:00"
            },
            {
                "id": 9,
                "day_of_week": "TUESDAY",
                "start_time": "13:30:00",
                "end_time": "14:30:00"
            },
            {
                "id": 10,
                "day_of_week": "TUESDAY",
                "start_time": "14:30:00",
                "end_time": "15:30:00"
            }
        ],
        "room_list": [
            {
                "id": 1,
                "name": "Room A"
            },
            {
                "id": 2,
                "name": "Room B"
            },
            {
                "id": 3,
                "name": "Room C"
            }
        ],
        "lesson_list": [
            {
                "id": 1,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 4,
                    "day_of_week": "MONDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 2,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 2,
                    "day_of_week": "MONDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 3,
                "subject": "Physics",
                "teacher": "M. Curie",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 1,
                    "day_of_week": "MONDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 4,
                "subject": "Chemistry",
                "teacher": "M. Curie",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 5,
                    "day_of_week": "MONDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 5,
                "subject": "Biology",
                "teacher": "C. Darwin",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 3,
                    "day_of_week": "MONDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 6,
                "subject": "History",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 7,
                    "day_of_week": "TUESDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 7,
                "subject": "English",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 10,
                    "day_of_week": "TUESDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 8,
                "subject": "English",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 8,
                    "day_of_week": "TUESDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 9,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 6,
                    "day_of_week": "TUESDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 10,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 9,
                    "day_of_week": "TUESDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 11,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 5,
                    "day_of_week": "MONDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 12,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 1,
                    "day_of_week": "MONDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 13,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 3,
                    "day_of_week": "MONDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 14,
                "subject": "Physics",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 4,
                    "day_of_week": "MONDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 15,
                "subject": "Chemistry",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 9,
                    "day_of_week": "TUESDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 16,
                "subject": "French",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 10,
                    "day_of_week": "TUESDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 17,
                "subject": "Geography",
                "teacher": "C. Darwin",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 2,
                    "day_of_week": "MONDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 18,
                "subject": "History",
                "teacher": "I. Jones",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 6,
                    "day_of_week": "TUESDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 19,
                "subject": "English",
                "teacher": "P. Cruz",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 8,
                    "day_of_week": "TUESDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 20,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 7,
                    "day_of_week": "TUESDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            }
        ],
        "score": {},
        "_optapy_solver_run_id": [
            1743452826400,
            1742041450928,
            "7017acc3-d5a2-11f0-a00f-00155dd9fec7"
        ]
    },
    "status": "Completed"
}

curl --location 'http://127.0.0.1:8000/optapy/solve/async' \
--header 'Content-Type: application/json' \
--data '{
    "timeslot_list": [
        {
            "id": 1,
            "day_of_week": "MONDAY",
            "start_time": "08:30:00",
            "end_time": "09:30:00"
        },
        {
            "id": 2,
            "day_of_week": "MONDAY",
            "start_time": "09:30:00",
            "end_time": "10:30:00"
        },
        {
            "id": 3,
            "day_of_week": "MONDAY",
            "start_time": "10:30:00",
            "end_time": "11:30:00"
        },
        {
            "id": 4,
            "day_of_week": "MONDAY",
            "start_time": "13:30:00",
            "end_time": "14:30:00"
        },
        {
            "id": 5,
            "day_of_week": "MONDAY",
            "start_time": "14:30:00",
            "end_time": "15:30:00"
        },
        {
            "id": 6,
            "day_of_week": "TUESDAY",
            "start_time": "08:30:00",
            "end_time": "09:30:00"
        },
        {
            "id": 7,
            "day_of_week": "TUESDAY",
            "start_time": "09:30:00",
            "end_time": "10:30:00"
        },
        {
            "id": 8,
            "day_of_week": "TUESDAY",
            "start_time": "10:30:00",
            "end_time": "11:30:00"
        },
        {
            "id": 9,
            "day_of_week": "TUESDAY",
            "start_time": "13:30:00",
            "end_time": "14:30:00"
        },
        {
            "id": 10,
            "day_of_week": "TUESDAY",
            "start_time": "14:30:00",
            "end_time": "15:30:00"
        }
    ],
    "room_list": [
        {
            "id": 1,
            "name": "Room A"
        },
        {
            "id": 2,
            "name": "Room B"
        },
        {
            "id": 3,
            "name": "Room C"
        }
    ],
    "lesson_list": [
        {
            "id": 1,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 2,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 3,
            "subject": "Physics",
            "teacher": "M. Curie",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 4,
            "subject": "Chemistry",
            "teacher": "M. Curie",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 5,
            "subject": "Biology",
            "teacher": "C. Darwin",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 6,
            "subject": "History",
            "teacher": "I. Jones",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 7,
            "subject": "English",
            "teacher": "I. Jones",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 8,
            "subject": "English",
            "teacher": "I. Jones",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 9,
            "subject": "Spanish",
            "teacher": "P. Cruz",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 10,
            "subject": "Spanish",
            "teacher": "P. Cruz",
            "student_group": "9th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 11,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 12,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 13,
            "subject": "Math",
            "teacher": "A. Turing",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 14,
            "subject": "Physics",
            "teacher": "M. Curie",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 15,
            "subject": "Chemistry",
            "teacher": "M. Curie",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 16,
            "subject": "French",
            "teacher": "M. Curie",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 17,
            "subject": "Geography",
            "teacher": "C. Darwin",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 18,
            "subject": "History",
            "teacher": "I. Jones",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 19,
            "subject": "English",
            "teacher": "P. Cruz",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        },
        {
            "id": 20,
            "subject": "Spanish",
            "teacher": "P. Cruz",
            "student_group": "10th grade",
            "timeslot": null,
            "room": null
        }
    ]
}'

Response:
{
    "problem_id": "fae523da-ab85-4808-9628-780c50224931",
    "status": "SOLVING_ACTIVE"
}


curl --location 'http://127.0.0.1:8000/optapy/solve/status/fae523da-ab85-4808-9628-780c50224931'

Response:
{
    "problem_id": "fae523da-ab85-4808-9628-780c50224931",
    "status": "NOT_SOLVING",
    "solution": {
        "timeslot_list": [
            {
                "id": 1,
                "day_of_week": "MONDAY",
                "start_time": "08:30:00",
                "end_time": "09:30:00"
            },
            {
                "id": 2,
                "day_of_week": "MONDAY",
                "start_time": "09:30:00",
                "end_time": "10:30:00"
            },
            {
                "id": 3,
                "day_of_week": "MONDAY",
                "start_time": "10:30:00",
                "end_time": "11:30:00"
            },
            {
                "id": 4,
                "day_of_week": "MONDAY",
                "start_time": "13:30:00",
                "end_time": "14:30:00"
            },
            {
                "id": 5,
                "day_of_week": "MONDAY",
                "start_time": "14:30:00",
                "end_time": "15:30:00"
            },
            {
                "id": 6,
                "day_of_week": "TUESDAY",
                "start_time": "08:30:00",
                "end_time": "09:30:00"
            },
            {
                "id": 7,
                "day_of_week": "TUESDAY",
                "start_time": "09:30:00",
                "end_time": "10:30:00"
            },
            {
                "id": 8,
                "day_of_week": "TUESDAY",
                "start_time": "10:30:00",
                "end_time": "11:30:00"
            },
            {
                "id": 9,
                "day_of_week": "TUESDAY",
                "start_time": "13:30:00",
                "end_time": "14:30:00"
            },
            {
                "id": 10,
                "day_of_week": "TUESDAY",
                "start_time": "14:30:00",
                "end_time": "15:30:00"
            }
        ],
        "room_list": [
            {
                "id": 1,
                "name": "Room A"
            },
            {
                "id": 2,
                "name": "Room B"
            },
            {
                "id": 3,
                "name": "Room C"
            }
        ],
        "lesson_list": [
            {
                "id": 1,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 4,
                    "day_of_week": "MONDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 2,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 2,
                    "day_of_week": "MONDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 3,
                "subject": "Physics",
                "teacher": "M. Curie",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 1,
                    "day_of_week": "MONDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 4,
                "subject": "Chemistry",
                "teacher": "M. Curie",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 5,
                    "day_of_week": "MONDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 5,
                "subject": "Biology",
                "teacher": "C. Darwin",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 3,
                    "day_of_week": "MONDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 6,
                "subject": "History",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 7,
                    "day_of_week": "TUESDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 7,
                "subject": "English",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 10,
                    "day_of_week": "TUESDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 8,
                "subject": "English",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 8,
                    "day_of_week": "TUESDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 9,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 6,
                    "day_of_week": "TUESDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 10,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 9,
                    "day_of_week": "TUESDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 11,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 5,
                    "day_of_week": "MONDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 12,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 1,
                    "day_of_week": "MONDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 13,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 3,
                    "day_of_week": "MONDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 14,
                "subject": "Physics",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 4,
                    "day_of_week": "MONDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 15,
                "subject": "Chemistry",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 9,
                    "day_of_week": "TUESDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 16,
                "subject": "French",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 10,
                    "day_of_week": "TUESDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 17,
                "subject": "Geography",
                "teacher": "C. Darwin",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 2,
                    "day_of_week": "MONDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 18,
                "subject": "History",
                "teacher": "I. Jones",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 6,
                    "day_of_week": "TUESDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 19,
                "subject": "English",
                "teacher": "P. Cruz",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 8,
                    "day_of_week": "TUESDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 20,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 7,
                    "day_of_week": "TUESDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            }
        ],
        "score": "0hard/10soft"
    }
}


curl --location 'http://127.0.0.1:8000/optapy/solution/fae523da-ab85-4808-9628-780c50224931'
Response:
{
    "solution": {
        "timeslot_list": [
            {
                "id": 1,
                "day_of_week": "MONDAY",
                "start_time": "08:30:00",
                "end_time": "09:30:00"
            },
            {
                "id": 2,
                "day_of_week": "MONDAY",
                "start_time": "09:30:00",
                "end_time": "10:30:00"
            },
            {
                "id": 3,
                "day_of_week": "MONDAY",
                "start_time": "10:30:00",
                "end_time": "11:30:00"
            },
            {
                "id": 4,
                "day_of_week": "MONDAY",
                "start_time": "13:30:00",
                "end_time": "14:30:00"
            },
            {
                "id": 5,
                "day_of_week": "MONDAY",
                "start_time": "14:30:00",
                "end_time": "15:30:00"
            },
            {
                "id": 6,
                "day_of_week": "TUESDAY",
                "start_time": "08:30:00",
                "end_time": "09:30:00"
            },
            {
                "id": 7,
                "day_of_week": "TUESDAY",
                "start_time": "09:30:00",
                "end_time": "10:30:00"
            },
            {
                "id": 8,
                "day_of_week": "TUESDAY",
                "start_time": "10:30:00",
                "end_time": "11:30:00"
            },
            {
                "id": 9,
                "day_of_week": "TUESDAY",
                "start_time": "13:30:00",
                "end_time": "14:30:00"
            },
            {
                "id": 10,
                "day_of_week": "TUESDAY",
                "start_time": "14:30:00",
                "end_time": "15:30:00"
            }
        ],
        "room_list": [
            {
                "id": 1,
                "name": "Room A"
            },
            {
                "id": 2,
                "name": "Room B"
            },
            {
                "id": 3,
                "name": "Room C"
            }
        ],
        "lesson_list": [
            {
                "id": 1,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 4,
                    "day_of_week": "MONDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 2,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 2,
                    "day_of_week": "MONDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 3,
                "subject": "Physics",
                "teacher": "M. Curie",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 1,
                    "day_of_week": "MONDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 4,
                "subject": "Chemistry",
                "teacher": "M. Curie",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 5,
                    "day_of_week": "MONDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 5,
                "subject": "Biology",
                "teacher": "C. Darwin",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 3,
                    "day_of_week": "MONDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 6,
                "subject": "History",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 7,
                    "day_of_week": "TUESDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 7,
                "subject": "English",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 10,
                    "day_of_week": "TUESDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 8,
                "subject": "English",
                "teacher": "I. Jones",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 8,
                    "day_of_week": "TUESDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 9,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 6,
                    "day_of_week": "TUESDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 10,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "9th grade",
                "timeslot": {
                    "id": 9,
                    "day_of_week": "TUESDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 11,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 5,
                    "day_of_week": "MONDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 12,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 1,
                    "day_of_week": "MONDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 13,
                "subject": "Math",
                "teacher": "A. Turing",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 3,
                    "day_of_week": "MONDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 14,
                "subject": "Physics",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 4,
                    "day_of_week": "MONDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 15,
                "subject": "Chemistry",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 9,
                    "day_of_week": "TUESDAY",
                    "start_time": "13:30:00",
                    "end_time": "14:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 16,
                "subject": "French",
                "teacher": "M. Curie",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 10,
                    "day_of_week": "TUESDAY",
                    "start_time": "14:30:00",
                    "end_time": "15:30:00"
                },
                "room": {
                    "id": 3,
                    "name": "Room C"
                }
            },
            {
                "id": 17,
                "subject": "Geography",
                "teacher": "C. Darwin",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 2,
                    "day_of_week": "MONDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 18,
                "subject": "History",
                "teacher": "I. Jones",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 6,
                    "day_of_week": "TUESDAY",
                    "start_time": "08:30:00",
                    "end_time": "09:30:00"
                },
                "room": {
                    "id": 1,
                    "name": "Room A"
                }
            },
            {
                "id": 19,
                "subject": "English",
                "teacher": "P. Cruz",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 8,
                    "day_of_week": "TUESDAY",
                    "start_time": "10:30:00",
                    "end_time": "11:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            },
            {
                "id": 20,
                "subject": "Spanish",
                "teacher": "P. Cruz",
                "student_group": "10th grade",
                "timeslot": {
                    "id": 7,
                    "day_of_week": "TUESDAY",
                    "start_time": "09:30:00",
                    "end_time": "10:30:00"
                },
                "room": {
                    "id": 2,
                    "name": "Room B"
                }
            }
        ],
        "score": "0hard/10soft"
    },
    "status": "COMPLETED"
}





https://priceline-editor.replit.app/


