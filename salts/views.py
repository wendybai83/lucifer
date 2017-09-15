# -*- coding: utf-8 -*-
# author: itimor

import sys
import subprocess

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from salts.models import SaltServer, SaltCmdrun
from salts.serializers import SaltServerSerializer, SaltCmdrunSerializer

def run(cmd):
    try:
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = output.stdout.readlines()
        stderr = ''
    except:
        stdout = ''
        stderr = str(sys.exc_info()[1])

    if len(stderr):
        return stderr
    else:
        return stdout


class SaltServerViewSet(viewsets.ModelViewSet):
    queryset = SaltServer.objects.all()
    serializer_class = SaltServerSerializer


@api_view(['POST'])
def cmdrun(request):
    if request.method == 'POST':
        cmd = request.data['cmd']
        results = run(cmd)
        serializer = SaltCmdrunSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(results, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)