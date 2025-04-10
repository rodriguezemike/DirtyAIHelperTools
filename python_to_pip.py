from openai import OpenAI
import dotenv
import subprocess
import shlex
import sys
import os

#This should be used to generate a pip install command from looking through python files in a given directory.

dotenv.load_dotenv()
run_pip_requirements_generation = False
run_pip_install = False
run_pip_requirements_freeze = False

import_grep_command = 'grep -rio "^import \w*" %s' % os.path.abspath(sys.argv[1])
from_grep_command = 'grep -rio "^from \w*" %s' % os.path.abspath(sys.argv[1])

print("Import Command %s" % import_grep_command)
print("From Grep Command %s" % from_grep_command)

import_process = subprocess.run(shlex.split(import_grep_command), capture_output = True)
from_process = subprocess.run(shlex.split(from_grep_command), capture_output = True)

imports = [i.decode("utf-8").split(":")[1].strip() for i in import_process.stdout.splitlines() if ":" in i.decode("utf-8")]

from_imports = [i.decode("utf-8").split(":")[1].strip().replace("from", "import") for i in from_process.stdout.splitlines() if ":" in i.decode("utf-8")]

import_list = list(set(imports + from_imports))

print("Import List -> %s"% import_list)

prompt = "Generate a pip install command of the available PyPI packages from the following import list excluding internal packages or non-PyPI packages with no explanation %s" % ",".join(import_list)

print("Prompt -> %s\n\n" % prompt)


client = OpenAI(
  api_key=os.environ["POPENAI_API_KEY"]
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": prompt}
  ]
)

print("Completion -> %s" % completion.choices[0].message.content.split("\n"))

for content in completion.choices[0].message.content.split("\n"):
	if content.startswith("pip"):
		pip_command = content
		break

print("pip command\n")
print(pip_command)
print()

if run_pip_requirements_generation:
	python_directory = os.path.abspath(sys.argv[1])
	requirements_path = os.path.join(python_directory, "requirements.txt")
	packages = pip_command.split("install")[1].split()
	with open(requirements_path, 'w') as f:
		f.write("\n".join(packages))
	print("Wrote requirements file at %s" % requirements_path)

if run_pip_install:
	print("Running auto install. I hope you know what youre doing")
	install_process = subprocess.run(shlex.split(pip_command), capture_output = True)
	print("stdout -> %s" % install_process.stdout)
	print("stderr -> %s" % install_process.stderr)

if run_pip_requirements_freeze:
	print("Generating requirements.txt")
	cmd = "pip freeze > %s/requirements.txt" % sys.argv[1].rstrip("/")
	requirements_process = subprocess.call(cmd, shell=True)
	print("%s/requirements.txt generated" % sys.argv[1].rstrip("/"))
