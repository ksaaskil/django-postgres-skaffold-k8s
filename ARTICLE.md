# Getting started with Kubernetes development with Skaffold

## Introduction

Containerization has been a revolution in software development. Technologies such as Docker have allowed developers package their software in packages that can be deployed anywhere, be it your local desktop, public cloud or your company's datacenter.

Containers are often deployed through container orchestration platforms such as [Kubernetes](https://kubernetes.io/). However, when locally developing services, I have always resorted to tools such as [Docker Compose](https://docs.docker.com/compose/) to run multiple related containers with a single command. This is great, but it feels a bit 2000s. My service has its own Kubernetes manifest describing how the service should be deployed, so why can't I use that for local development as well?

Enter [Skaffold](https://skaffold.dev/), a command-line tool for continuous development on Kubernetes. The tool was [open-sourced](https://github.com/GoogleContainerTools/skaffold) by Google in 2018. Skaffold watches your code and, detecting changes, it handles building, pushing and deploying the application to your local Kubernetes installation. You can even use Skaffold to build your CI/CD pipeline, handling the deployment all the way from local workstation to the production cluster.

In this article, we'll see how to develop a Kubernetes-native web application. We'll use Django to bootstrap the application, connect the application to Postgres database, and write Kubernetes manifests to continuously develop the application on a local Minikube cluster.

First we'll install all dependencies. Note that installing e.g. Minikube can take a long time, so feel free to move to the next section while waiting.

All code for this article can be found in [this repository](https://github.com/ksaaskil/django-postgres-skaffold-k8s).

## Prerequisites

### `kubectl`

First we'll install `kubectl` to interact with our Kubernetes cluster. The exact details will vary depending on your platform, so follow the instructions [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install `kubectl` on your own machine.

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

Finally, our example project requires [installing Django](https://www.djangoproject.com/download/) to bootstrap the project. _Because we're building a Kubernetes-native application, this step is only required for bootstrapping the project_: our code will, at the end of the day, run inside Docker, so if you don't want to install Python 3 and Django, feel free to copy the boilerplate from [the accompanying repository](https://github.com/ksaaskil/django-postgres-skaffold-k8s/tree/master/src/store).

First, ensure you have a working installation of [Python 3](https://www.python.org/). Then, you can install Django in your Python environment with [`pip`](https://pip.pypa.io/en/stable/):

```bash
$ pip install Django==3.0.7
```

If you don't want to mess with your global Python installation, you may want to ensure you're in a [virtual environment](https://docs.python.org/3/tutorial/venv.html) before running the command.

## Creating Django project

The Django application lives inside the `src/` directory of our repository. The project can be created with the `django-admin` command:

```bash
# Inside src/
$ django-admin startproject store
```

We call the project `store`. Move to `store/` directory and add `requirements.txt` containing all the dependencies our application needs:

```txt
# src/store/requirements.txt
django
gunicorn
psycopg2
```

Naturally, our server needs `django`. `gunicorn` is used for serving the application and `psycopg2` is the Postgres driver.

If you're willing to install the dependencies in your virtual environment, install:

```bash
$ pip install -r requirements.txt
```

Now, let's create an app that we'll use for status-checking:

```bash
# src/store
$ python manage.py startapp status
```

Add the following to `store/urls.py`:

```python
# src/store/store/urls.py
from django.urls import path, include

urlpatterns = [path("status/", include("status.urls"))]
```

This will boostrap the `status` app to `status/` endpoint.

```python
# src/store/status/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

In `status/views.py`, add the view to status-check database connection:

```python
# src/store/status/views.py
from django.db import connection
from django.http import HttpResponse

def index(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return HttpResponse({ "message": "OK"}, status=200)
    except Exception as ex:
        return HttpResponse({ "message": str(exception) }status=500)
```

Here we check if the database cursor can execute a `SELECT 1` statement and return 500 for any exception.

### Dockerfile

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
