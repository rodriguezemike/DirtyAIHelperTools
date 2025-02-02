#ToDo: Make this work.

'''
write a dockerfile that runs on debian linux a go program on go version 1.23 and has the following github go.yml dependencies 
          sudo apt update && sudo apt upgrade
          sudo apt-get install -y qt5-qmake qtbase5-dev libqt5webkit5-dev ffmpeg libasound2-dev
          go get github.com/aws/aws-sdk-go@v1.55.5
          go get github.com/chromedp/cdproto@v0.0.0-20241003230502-a4a8f7c660df
          go get github.com/chromedp/chromedp@v0.10.0
          go get github.com/chromedp/sysutil@v1.0.0
          go get github.com/ebitengine/oto/v3@v3.2.0
          go get github.com/ebitengine/purego@v0.7.1
          go get github.com/gobwas/httphead@v0.1.0
          go get github.com/gobwas/pool@v0.2.1
          go get github.com/gobwas/ws@v1.4.0
          go get github.com/gopherjs/gopherjs@v0.0.0-20190411002643-bd77b112433e
          go get github.com/gopxl/beep@v1.4.1
          go get github.com/gopxl/beep/v2@v2.1.0
          go get github.com/jmespath/go-jmespath@v0.4.0
          go get github.com/josharian/intern@v1.0.0
          go get github.com/konsorten/go-windows-terminal-sequences@v1.0.2
          go get github.com/mailru/easyjson@v0.7.7
          go get github.com/pkg/errors@v0.9.1
          go get github.com/sirupsen/logrus@v1.4.1
          go get github.com/therecipe/env_darwin_amd64_513@v0.0.0-20190626001412-d8e92e8db4d0
          go get github.com/therecipe/env_linux_amd64_513@v0.0.0-20190626000307-e137a3934da6
          go get github.com/therecipe/env_windows_amd64_513@v0.0.0-20190626000028-79ec8bd06fb2
          go get github.com/therecipe/env_windows_amd64_513/Tools@v0.0.0-20190626000028-79ec8bd06fb2
          go get github.com/therecipe/qt@v0.0.0-20200904063919-c0c124a5770d
          go get github.com/therecipe/qt/internal/binding/files/docs/5.12.0@v0.0.0-20200904063919-c0c124a5770d
          go get github.com/therecipe/qt/internal/binding/files/docs/5.13.0@v0.0.0-20200904063919-c0c124a5770d
          go get github.com/u2takey/ffmpeg-go@v0.5.0
          go get github.com/u2takey/go-utils@v0.3.1
          go get golang.org/x/crypto@v0.0.0-20200622213623-75b288015ac9
          go get golang.org/x/sys@v0.26.0
          go get golang.org/x/tools@v0.0.0-20190420181800-aa740d480789
'''


'''
Response with explanation (remove this too) have flags for various steps after if desired

To create a Dockerfile that runs on Debian Linux, installs the required dependencies, and sets up your Go environment with the specified Go version and dependencies, you can follow these steps.

Here is the Dockerfile that will build an image with all your requirements:

Dockerfile
Copy
# Use Debian as the base image
FROM debian:bullseye-slim

# Set environment variables for Go
ENV GO_VERSION 1.23
ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

# Install necessary dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    sudo \
    qt5-qmake \
    qtbase5-dev \
    libqt5webkit5-dev \
    ffmpeg \
    libasound2-dev \
    wget \
    curl \
    git \
    ca-certificates

# Install Go (version 1.23)
RUN wget https://go.dev/dl/go$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xvzf go$GO_VERSION.linux-amd64.tar.gz && \
    rm go$GO_VERSION.linux-amd64.tar.gz

# Install Go dependencies
RUN go get github.com/aws/aws-sdk-go@v1.55.5 && \
    go get github.com/chromedp/cdproto@v0.0.0-20241003230502-a4a8f7c660df && \
    go get github.com/chromedp/chromedp@v0.10.0 && \
    go get github.com/chromedp/sysutil@v1.0.0 && \
    go get github.com/ebitengine/oto/v3@v3.2.0 && \
    go get github.com/ebitengine/purego@v0.7.1 && \
    go get github.com/gobwas/httphead@v0.1.0 && \
    go get github.com/gobwas/pool@v0.2.1 && \
    go get github.com/gobwas/ws@v1.4.0 && \
    go get github.com/gopherjs/gopherjs@v0.0.0-20190411002643-bd77b112433e && \
    go get github.com/gopxl/beep@v1.4.1 && \
    go get github.com/gopxl/beep/v2@v2.1.0 && \
    go get github.com/jmespath/go-jmespath@v0.4.0 && \
    go get github.com/josharian/intern@v1.0.0 && \
    go get github.com/konsorten/go-windows-terminal-sequences@v1.0.2 && \
    go get github.com/mailru/easyjson@v0.7.7 && \
    go get github.com/pkg/errors@v0.9.1 && \
    go get github.com/sirupsen/logrus@v1.4.1 && \
    go get github.com/therecipe/env_darwin_amd64_513@v0.0.0-20190626001412-d8e92e8db4d0 && \
    go get github.com/therecipe/env_linux_amd64_513@v0.0.0-20190626000307-e137a3934da6 && \
    go get github.com/therecipe/env_windows_amd64_513@v0.0.0-20190626000028-79ec8bd06fb2 && \
    go get github.com/therecipe/env_windows_amd64_513/Tools@v0.0.0-20190626000028-79ec8bd06fb2 && \
    go get github.com/therecipe/qt@v0.0.0-20200904063919-c0c124a5770d && \
    go get github.com/therecipe/qt/internal/binding/files/docs/5.12.0@v0.0.0-20200904063919-c0c124a5770d && \
    go get github.com/therecipe/qt/internal/binding/files/docs/5.13.0@v0.0.0-20200904063919-c0c124a5770d && \
    go get github.com/u2takey/ffmpeg-go@v0.5.0 && \
    go get github.com/u2takey/go-utils@v0.3.1 && \
    go get golang.org/x/crypto@v0.0.0-20200622213623-75b288015ac9 && \
    go get golang.org/x/sys@v0.26.0 && \
    go get golang.org/x/tools@v0.0.0-20190420181800-aa740d480789

# Set up working directory
WORKDIR /app

# Copy Go source code into the container
COPY . .

# Build the Go application
RUN go build -o myapp .

# Expose the port your app runs on (Optional)
EXPOSE 8080

# Command to run the Go program
CMD ["./myapp"]
Explanation:
Base Image: We're using the debian:bullseye-slim base image, which is lightweight but still has the essential package manager (apt).
Install Dependencies: We install the required libraries and tools (qt5, ffmpeg, libasound2, and others).
Install Go: We download and install Go version 1.23 manually.
Go Get Dependencies: The go get commands install all the dependencies you mentioned from the Go modules.
Copy Code: Copies your Go source code (assumed to be in the same directory as the Dockerfile) into the container.
Build: The Go application is built using go build.
Expose Port: Optionally exposes a port (change it to match your app's port).
Run Command: When the container runs, it executes the compiled Go program.
Usage:
Build the Docker image:
bash
Copy
docker build -t my-go-app .
Run the container:
bash
Copy
docker run -p 8080:8080 my-go-app
This will set up a container with your Go application and all the dependencies installed, ready to run on Debian.
'''
