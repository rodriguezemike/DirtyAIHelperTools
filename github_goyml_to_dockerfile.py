from openai import OpenAI
import dotenv
import subprocess
import shlex
import sys
import os

dotenv.load_dotenv()

client = OpenAI(
	api_key = os.environ["POPENAI_API_KEY"]
)

path = sys.argv[1]
try:
	custom_distro = sys.argv[2]
except IndexError:
	custom_distro = None

program_name = "program"
distro = custom_distro if custom_distro else "debian" 
go_version = "1.0"
working_directory = "./"
dependency_section = False
dependency_lines = []
os_software_package_depends = ["apt", "apt-get", "sudo apt-get", "go get"]

if not path.endswith("go.yml"):
	raise Exception("We need a go.yml file to do this human.")

with open(path, 'r') as f:
	lines = f.readlines()

for line in [l.strip(" ").lstrip("\t").strip("\n") for l in lines]:
	if line.startswith("name"):
		program_name = line
	elif line.startswith("go-version"):
		go_version = line.split(":")[1].strip("'")
	elif line.startswith("runs-on") and custom_distro == None:
		distro = line.split(":")[1]
	elif  dependency_section and any([i in line.lower() for i in os_software_package_depends ]):
		dependency_lines.append(line)
	elif dependency_section and line.startswith("working-directory"):
		working_directory = line.split(":")[1]
	elif "dependencies" in line.lower():
		dependency_section = True
	elif "name" in line and dependency_section == True:
		dependency_section = False	
	
prompt = "Write dockerfiles for windows, linux, and unix seperated with '###' and with comments and no explanation and commented out expose port line for a go program named %s having the working directory %s that builds on %s using go version %s and has the following dependency commands %s" % (program_name, working_directory, distro, go_version, "\n".join(dependency_lines))


completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": prompt}
  ]
)

print("Composite Dockerfile\n%s\n" % "\n".join([l for l in completion.choices[0].message.content.split("\n") if not l.startswith("```")]))
completion = "\n".join([l for l in completion.choices[0].message.content.split("\n") if not l.startswith("```")])


#may have to work this delimiter ### into the prompt
dockerfiles = completion.split("###")


windows_dockerfile_path = "docker/windows/Dockerfile"
linux_dockerfile_path = "docker/linux/Dockerfile"
unix_dockerfile_path = "docker/unix/Dockerfile"

print ("WHY YOU NO WORK")
print(dockerfiles)

for dockerfile in dockerfiles:
	if 'for windows' in dockerfile.lower():
		path = os.path.join(os.getcwd(), windows_dockerfile_path)
	elif "for unix" in dockerfile.lower():		
		path = os.path.join(os.getcwd(), unix_dockerfile_path)
	else:
		path = os.path.join(os.getcwd(), linux_dockerfile_path)

	print("\n", path, "\n", dockerfile)
	if not os.path.exists(os.path.dirname(path)):	
		os.makedirs(os.path.dirname(path))

	with open(path, 'w') as f:
		f.write(dockerfile)

compose_prompt = "write a docker-compose.yml file with no explanation from the following dockerfile contents %s" % completion


compose_completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": compose_prompt}
  ]
)

compose_completion = "\n".join([l for l in compose_completion.choices[0].message.content.split("\n") if not l.startswith("```")])

print("Boilerplate Compose Spec Dockerfile\n%s" % compose_completion)

with open("docker-compose.yml", 'w') as f:
	f.write(compose_completion)
