'''
Prompt based on this, find it in the go.mod file. and find necessary things.
Write a github actions go.yml file that for a program called program that uses go version 1.23 and creates a go get commands for the following requirements
	github.com/aws/aws-sdk-go v1.55.5 // indirect
	github.com/chromedp/cdproto v0.0.0-20241003230502-a4a8f7c660df // indirect
	github.com/chromedp/chromedp v0.10.0 // indirect
	github.com/chromedp/sysutil v1.0.0 // indirect
	github.com/ebitengine/oto/v3 v3.2.0 // indirect
	github.com/ebitengine/purego v0.7.1 // indirect
	github.com/gobwas/httphead v0.1.0 // indirect
	github.com/gobwas/pool v0.2.1 // indirect
	github.com/gobwas/ws v1.4.0 // indirect
	github.com/gopherjs/gopherjs v0.0.0-20190411002643-bd77b112433e // indirect
	github.com/gopxl/beep v1.4.1 // indirect
	github.com/gopxl/beep/v2 v2.1.0 // indirect
	github.com/jmespath/go-jmespath v0.4.0 // indirect
	github.com/josharian/intern v1.0.0 // indirect
	github.com/konsorten/go-windows-terminal-sequences v1.0.2 // indirect
	github.com/mailru/easyjson v0.7.7 // indirect
	github.com/pkg/errors v0.9.1 // indirect
	github.com/sirupsen/logrus v1.4.1 // indirect
	github.com/therecipe/env_darwin_amd64_513 v0.0.0-20190626001412-d8e92e8db4d0 // indirect
	github.com/therecipe/env_linux_amd64_513 v0.0.0-20190626000307-e137a3934da6 // indirect
	github.com/therecipe/env_windows_amd64_513 v0.0.0-20190626000028-79ec8bd06fb2 // indirect
	github.com/therecipe/env_windows_amd64_513/Tools v0.0.0-20190626000028-79ec8bd06fb2 // indirect
	github.com/therecipe/qt v0.0.0-20200904063919-c0c124a5770d // indirect
	github.com/therecipe/qt/internal/binding/files/docs/5.12.0 v0.0.0-20200904063919-c0c124a5770d // indirect
	github.com/therecipe/qt/internal/binding/files/docs/5.13.0 v0.0.0-20200904063919-c0c124a5770d // indirect
	github.com/u2takey/ffmpeg-go v0.5.0 // indirect
	github.com/u2takey/go-utils v0.3.1 // indirect
	golang.org/x/crypto v0.0.0-20200622213623-75b288015ac9 // indirect
	golang.org/x/sys v0.26.0 // indirect
	golang.org/x/tools v0.0.0-20190420181800-aa740d480789 // indirect

'''
from openai import OpenAI
import dotenv
import subprocess
import shlex
import sys
import os


dotenv.load_dotenv()

client = OpenAI(
	api_key = os.environ["OPENAI_API_KEY"]
)


name = "program"
requires = []
go_version = "1.0"
require_flag = False
path = sys.argv[1]

if not path.endswith("go.mod"):
	raise Exception("WE need a go.mod file to do this sir.")

with open(path, 'r') as f:
	lines = f.readlines()

for line in lines:
	if require_flag and not line.startswith(")"):
		requires.append(line)
	else:
		if lines.starts with("module"):
			name = line.split()[1] + "Github CI"
		if line.startswith("go"):
			go_version = line.split()[1]
		if line.startswith("require ("):
			require_flag = True
	

requirements = "\n".join(requires)

prompt = "Write only a github actions go.yml file for a module called %s that uses go version %s and creates go get commands for the follow requirements with no explanation\n%s" % (name, go_version, requirements) 

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": prompt}
  ]
)

print("Completion -> %s" % completion.choices[0].message.content.split("\n"))

#ToDo -> Write this to a file called go.yml for the user to move into their .git folder. also debug






