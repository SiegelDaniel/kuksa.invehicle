# Copyright Fraunhofer IEM, 2020. Part of the Eclipse Kuksa Project.
#
# All rights reserved. This configuration file is provided to you under the
# terms and conditions of the Eclipse Distribution License v1.0 which
# accompanies this distribution, and is available at
# http://www.eclipse.org/org/documents/edl-v10.php

FROM arm32v6/python:3.7-alpine

COPY qemu-arm-static /usr/bin/qemu-arm-static


ADD ./src/ /app
WORKDIR /app
RUN pip install --target=./ --no-cache-dir -r requirements.txt

CMD ["/usr/local/bin/python", "attack.py"]
