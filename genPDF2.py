import os
import sys
import subprocess

def htmlToPdf(input, dest):
	subprocess.call(["wkhtmltopdf", input, dest])
