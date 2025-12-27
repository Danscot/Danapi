from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework.exceptions import ValidationError

from rest_framework import status

from datetime import datetime

import subprocess

import psutil

import platform

import re

import time


def to_gb(bytes_value):

	return round(bytes_value / (1024 ** 3), 2)


@api_view(["GET"])

def root(request):

	return Response({"status": "Ok", "message": "Danscot Api System Is Running"}, status=status.HTTP_200_OK)


@api_view(["GET"])

def specs(request):

    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)

    cpu_cores = psutil.cpu_count(logical=True)

    # RAM
    ram = psutil.virtual_memory()

    ram_total_gb = to_gb(ram.total)

    ram_used_gb = to_gb(ram.used)

    ram_percent = ram.percent

    # Disk
    disk = psutil.disk_usage('/')

    disk_total_gb = to_gb(disk.total)

    disk_used_gb = to_gb(disk.used)

    disk_percent = disk.percent

    # Network
    net = psutil.net_io_counters()
    
    bytes_sent = net.bytes_sent

    bytes_recv = net.bytes_recv

    # Uptime
    
    boot_time = psutil.boot_time()
    
    uptime_seconds = int(time.time() - boot_time)

    # System info
    
    system = platform.system()
    
    release = platform.release()
    
    machine = platform.machine()

    
    return Response({

    	"status": "ok",
    
        "cpu": {"usage_percent": cpu_percent, "cores": cpu_cores},
    
        "ram": {"total_gb": ram_total_gb, "used_gb": ram_used_gb, "usage_percent": ram_percent},
    
        "disk": {"total_gb": disk_total_gb, "used_gb": disk_used_gb, "usage_percent": disk_percent},
    
        "network": {"bytes_sent": bytes_sent, "bytes_received": bytes_recv},
    
        "uptime_seconds": uptime_seconds,
    
        "system_info": {"os": system, "release": release, "arch": machine}
    },

    	status=status.HTTP_200_OK

   )
