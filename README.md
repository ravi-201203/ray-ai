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

