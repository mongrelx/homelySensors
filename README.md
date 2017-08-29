apt-get install python-pip


Install as systemd service
sudo cp /opt/homeSensors/homelySensor.service  /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/homelySensor.service
sudo systemctl daemon-reload
sudo systemctl enable homelySensor.service
sudo systemctl start homelySensor.service
