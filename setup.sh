# install service
cd /etc/systemd/system; sudo ln -s /home/pi/water/water.service .
sudo systemctl daemon-reload
sudo systemctl enable water.service
sudo systemctl start water.service
