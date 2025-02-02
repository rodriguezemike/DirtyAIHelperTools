from openai import OpenAI
import dotenv
import subprocess
import shlex
import sys
import os

#This should be used to generate a pip install command from looking through python files in a given directory.

dotenv.load_dotenv()
run_pip_install = False
run_pip_requirements_freeze = False

import_grep_command = 'grep -rio "^import \w*" %s' % sys.argv[1]
from_grep_command = 'grep -rio "^from \w*" %s' % sys.argv[1]

import_process = subprocess.run(shlex.split(import_grep_command), capture_output = True)
from_process = subprocess.run(shlex.split(from_grep_command), capture_output = True)


import_list = list(set([i.decode("utf-8").split(":")[1].strip() for i in import_process.stdout.splitlines()] + [i.decode("utf-8").split(":")[1].strip().replace("from", "import") for i in from_process.stdout.splitlines()]))

prompt = "Generate a pip install command of the available PyPI packages from the following import list excluding internal packages or non-PyPI packages with no explanation %s" % ",".join(import_list)

print("Prompt -> %s\n\n" % prompt)


client = OpenAI(
  api_key=os.environ["OPENAI_API_KEY"]
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
