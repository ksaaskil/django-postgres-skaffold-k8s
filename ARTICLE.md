# Getting started with Kubernetes development with Skaffold

## Introduction

- Introduce Kubernetes
- Introduce Skaffold
- What we'll build
  - Django with Postgres

## Prerequisites

Before getting started, please ensure you have a working installation of [Python 3](https://www.python.org/).

Note that the installing all the prerequisites below may take a long time, so feel free to proceed to the next section while waiting.

### `kubectl`

First we'll install `kubectl` to interact with our Kubernetes cluster. The exact details will vary depending on your platform, so you may have to follow the instructions [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install `kubectl` on your own machine.

On [macOS](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-macos), `kubectl` can be installed as follows:

My commands:

```bash
$ cd ~/bin
$ curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl"
$ chmod +x kubectl
```

Here I download the `kubectl` executable in the `bin/` folder in my home directory. I have added this folder to my `$PATH` with `export PATH=$PATH:~/bin` in my `~/.bash_profile`, so I can execute the binary anywhere with the `kubectl` command. You can put the binary anywhere in your `$PATH`, say, in `/usr/local/bin/kubectl`.

After installation, check that it works:

```bash
$ kubectl version --client
```

### Minikube

The next step is to [install Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/). Again, the exact details vary on the platform. First, you may need to [install a Hypervisor](https://kubernetes.io/docs/tasks/tools/install-minikube/#install-a-hypervisor). I had [`hyperkit`](https://github.com/moby/hyperkit) installed on my machine already by [Docker Desktop](https://www.docker.com/products/docker-desktop), which I confirmed by running

```bash
$ hyperkit -h
```

Alternatively, you can install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

After ensuring a Hypervisor is installed, you can install `minikube` as stand-alone executable as follows:

```bash
$ cd ~/bin
$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64 \
$ chmod +x minikube
```

After this, you can bravely try and start your local Minikube cluster with:

```bash
$ minikube start
```

Note that running this command for the first time requires downloading big disk images, so be patient. If everything goes well, the cluster starts and you can enter the following command to access the Kubernetes dashboard:

```bash
$ minikube dashboard
```

If anything goes wrong, you can try and explicitly specify the driver as instructed [here](https://kubernetes.io/docs/tasks/tools/install-minikube/#confirm-installation).

### Skaffold

Next, we'll need to [install Skaffold](https://skaffold.dev/docs/install/). For macOS, I installed the stand-alone binary with:

```bash
$ cd ~/bin
$ curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-darwin-amd64
$ chmod +x skaffold
```

To verify your installation, run:

```bash
$ skaffold
```

### `django-admin`

Finally, our example project requires [installing Django](https://www.djangoproject.com/download/) to setup the project. You can install Django in your Python environment with [`pip`](https://pip.pypa.io/en/stable/):

```bash
$ pip install Django==3.0.7
```

If you don't want to mess with your global Python installation, you may want to ensure you're in a [virtual environment](https://docs.python.org/3/tutorial/venv.html) before running the command.

## Creating Django project

- Start project
- Start app
- Setup database
- Dockerfile
- nginx

## Preparing Skaffold

## Postgres deployment

## Troubleshooting

On macOS Mojave, I had to install C headers with:

```bash
$ sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
```

If you're having trouble with C on macOS, you may want to go through [this](https://github.com/golang/go/issues/31159#issuecomment-561413013):

```bash
sudo rm -rf /Library/Developer/CommandLineTools
xcode-select --install
cd /Library/Developer/CommandLineTools/Packages/
open macOS_SDK_headers_for_macOS_10.14.pkg
```
