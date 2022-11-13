# install flask service
cd /etc/systemd/system; sudo ln -s /home/pi/water/flask-site.service .
sudo systemctl daemon-reload
sudo systemctl enable flask-site.service
sudo systemctl start flask-site.service

# install util-site service
cd /etc/systemd/system; sudo ln -s /home/pi/water/water.service .
sudo systemctl daemon-reload
sudo systemctl enable water.service
sudo systemctl start water.service
