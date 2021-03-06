
#!/usr/bin/env bash

echo `date`

echo "Changing into ~/EmailNotifier"
cd /home/uwcc-admin/EmailNotifier
echo "Inside `pwd`"


# If no venv (python3 virtual environment) exists, then create one.
if [ ! -d "venv" ]
then
    echo "Creating venv python3 virtual environment."
    virtualenv -p python3 venv
fi

# Activate venv.
echo "Activating venv python3 virtual environment."
source venv/bin/activate

# Install dependencies using pip.
if [ ! -f "mail_notifier.log" ]
then
    echo "Installing pytz"
    pip install pytz
    echo "Installing mysql-connector"
    pip install mysql-connector
    touch /home/uwcc-admin/mail_notifier.log
fi


echo "Running mail_notifier main.py"
python main.py >> /home/uwcc-admin/mail_notifier.log 2>&1

# Deactivating virtual environment
echo "Deactivating virtual environment"
deactivate