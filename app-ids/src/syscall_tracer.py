#!/usr/bin/env python3

# *****************************************************************************
#  Copyright (c) 2018 Fraunhofer IEM and others
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#
#  Contributors: Fraunhofer IEM
# *****************************************************************************



#When contributing, please make sure to stick to PEP8 as much as possible.
#https://www.python.org/dev/peps/pep-0008/
import paho.mqtt.client as mqtt
from subprocess import Popen, PIPE, STDOUT
import threading
from datetime import datetime
import simplejson
import psutil
import config_handler


class SyscallTracer(object):

    def __init__(self):

        self.cfg_handler = config_handler.config_loader("./config.json")
        self.config      = self.cfg_handler.get_config("SYSCALL_TRACER")

        self.PID        = self.cfg_handler.get_config_point("PID",self.config)
        self.PNAMES      = self.cfg_handler.get_config_point("PNAMES",self.config)
        self.BROKER_IP  = self.cfg_handler.get_config_point("BROKER_IP",self.config)
        self.QOS        = self.cfg_handler.get_config_point("QOS",self.config)

        self.client = mqtt.Client()
        
        try:
            self.client.connect(self.BROKER_IP)
        except Exception:
            print("Connection to MQTT broker failed.")
            raise SystemExit(0)

        if self.PID != "" and self.PNAMES == "":
            print("Tracing by PID")
            self.trace_by_pid()
        elif self.PID == "" and self.PNAMES != "":
            self.trace_by_process()
            #PNAMES are preferred if both are provided
        elif self.PID != "" and self.PNAMES != "":
            self.trace_by_process()
        else:
            print("No PNAME or PID found")
            raise SystemExit(1)

        self.client.loop_start()

    def find_pids(self):
        """Given a list of keywords for process identification, searches running processes for these exact keywords
        If multiple matches are found, the first one is returned"""
        import os
        process_ids = []
        try:
            for proc in psutil.process_iter():#iterate through all processes
               for cmdline in proc.cmdline():
                    for name in self.PNAMES:
                        if name in cmdline:
                            process_ids.append(proc.pid)
                            print("Found {0}".format(name))
        except:
            print("Process resolution failed.")
            raise SystemExit(0)
        if len(process_ids) > 0:
            return process_ids[0] 
        else:
            raise ValueError("Could not find a fitting process")

    
    def trace_by_pid(self):
        """Unbuffered python wrapper for strace, refer to the documentation to understand design choices."""
        proc = Popen(['stdbuf', '-oL', 'strace', '-p',str(self.PID), '-tt'],
                    bufsize=1, stdout=PIPE, stderr=STDOUT, close_fds=True)
        for line in iter(proc.stdout.readline, b''):
            trace = str(line,'utf-8')
            self.send_trace(trace)
        proc.stdout.close()
        proc.wait()

    def get_process_name(self,pid):
        process = psutil.Process(int(pid))
        process_name = process.name()
        return process_name

    def trace_by_process(self):
        self.PID = self.find_pids()
        self.trace_by_pid()
        

    def send_trace(self,trace):
        print("Sending trace {0}".format(trace))
        datadict = {
            'data' : trace,
            'processname': "".join(self.PNAMES)
        }
        self.client.publish('TRACED',simplejson.dumps(datadict),qos=self.QOS)

    def load_config(self,JSON_PATH):
        """Loads config from a given JSON file, extracts the relevant config parameters"""
        with open(JSON_PATH) as json_file:
            data = simplejson.load(json_file)
            config = data['syscall_tracer']
            return config

    def get_config(self,key):
        """Extracts a configuration key from the config if it exists"""
        if key in self.config:
            return self.config["key"]

if __name__ == "__main__":
    Tracer = SyscallTracer()