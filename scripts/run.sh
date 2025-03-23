#!/bin/bash
cd /home/ec2-user/app
gunicorn -w 4 -b 0.0.0.0:80 app:app --daemon