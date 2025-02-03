#ToDo: Optimize
from openai import OpenAI
import dotenv
import subprocess
import sys
import os


dotenv.load_dotenv()

client = OpenAI(
	api_key = os.environ["OPENAI_API_KEY"]
)

work_dir = "./"
action = "push"
name = "program"
distro = "ubtuntu-latest"
branch = "main"
requires = []
installs = []
go_version = "1.0"
require_flag = False
path = sys.argv[1]

if not path.endswith("go.mod"):
	raise Exception("We need a go.mod file to do this human.")

with open(path, 'r') as f:
	lines = f.readlines()

for line in lines:
	if require_flag and not line.startswith(")"):
		requires.append(line.split("//")[0])
		installs.append("/".join(line.split("//")[0].split("/")[2:]).strip()) #Sus
	else:
		if line.startswith("module"):
			name = line.split()[1]
		if line.startswith("go"):
			go_version = line.split()[1]
		if line.startswith("require ("):
			require_flag = True
	

requirements = "\n".join(requires)
installs = ", ".join(installs)

#Can optimize this, can also rip out the github repo names from the requirements to build the apt-get installs 
#We should structure this in dict with multiple sentences and a dictionary string sub. Joining together at the end to write the final prompt. 
prompt = "Write a github actions go.yml file that runs on %s with no explanation for a golang program called %s that uses go version %s, caches go modules using github actions using work directory %s, writes an apt-get install command with the --ignore-missing flag and the --no-install-recommends flag for the following \n%s.\n Install go dependencies by writing the following go get statements for the dependencies \n%s\n runs tests on the working directory %s\n runs build on working directory%s\n for the %s branch whenever a %s or pull-request happens" % (distro, name, go_version, work_dir, installs, requirements, work_dir, work_dir, branch, action) 


completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": prompt}
  ]
)

print("-===---------Writing to go.yml---------===-\n%s\n" % "\n".join([l for l in completion.choices[0].message.content.split("\n") if not l.startswith("```")]))

#ToDo -> Write this to a file called go.yml for the user to move into their .git folder. also debug
with open("./go.yml", 'w') as f:
	f.write("\n".join([l for l in completion.choices[0].message.content.split("\n") if not l.startswith("```")]))
	f.write('\n')
