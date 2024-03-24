Overview
========

A utility for converting S-COM Programmer files into a DTMF stream that 
can be played into an S-COM 5K/6K/7K repeater controller.  This eliminates
the need to be using modems or other old-school ways of playing the 
required tones into the repeater.

Advanced Language Features
==========================

Commands
========

Build Docker image:

        docker build -t dtmf-robot .  
        docker login
        docker tag dtmf-robot:latest brucemack/dtmf-robot:0.0        
        docker push brucemack/dtmf-robot:0.0      

Start Docker container:

        docker run -d --name dtmf-robot --restart=unless-stopped -p 8081:8080 dtmf-robot
        docker run -d --name dtmf-robot --restart=unless-stopped -p 8081:8080 brucemack/dtmf-robot:0.0

Starting the web server:

        uvicorn main:app --host 0.0.0.0 --port 8081 --reload --no-use-colors

Getting a token for AWS ECS (lasts for 12 hours) (see https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)

        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCTIDACCTID.dkr.ecr.us-east-1.amazonaws.com

Tag the image:
        
        docker tag dtmf-robot ACCTIDACCID.dkr.ecr.us-east-1.amazonaws.com/dtmf-robot:latest

Push the image:

        docker push ACCTIDACCID.dkr.ecr.us-east-1.amazonaws.com/dtmf-robot:latest


References
==========

S-COM
* [The 5K Users Guide](http://www.scomcontrollers.com/downloads/5kmanualv20.pdf)
* [Repeater Controller Article](https://www.repeater-builder.com/scom/controller-direct-programming.html)
* Demo URL: https://sqqe3umktm.us-east-1.awsapprunner.com/robot?demo=http://www.scomcontrollers.com/downloads/sample.txt

Licensing 
=========

This software is provided under the GNU GPL V3 license.  However, a commercial 
license is also available.  Please contact bruce at mackinnon dot com for more
information.

License Statement
=================

DTMWFT
Copyright (C) 2024, Bruce MacKinnon 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

NOT FOR COMMERCIAL USE WITHOUT PERMISSION.
