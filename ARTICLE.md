---
title: Getting started with local development on Kubernetes with Skaffold
published: false
description: First part of the tutorial on creating and running a Django application backed by Postgres on local Kubernetes
tags: python,kubernetes,tutorial
series: Learning local development on Kubernetes with Skaffold
---

Containerization has been a revolution in software development. Technologies such as Docker allow developers package their software and all its dependencies in containers runnable in any computing environment, be it your local desktop, public cloud or your company's datacenter, drastically simplifying the deployment process.

Containers are often deployed in container orchestration platforms such as [Kubernetes](https://kubernetes.io/). However, when locally developing services, I have always resorted to tools such as [Docker Compose](https://docs.docker.com/compose/) to run multiple related containers with a single command. This is great, but it feels a bit 2000s: My service has its own Kubernetes manifest describing how the service should be deployed, so why can't I use that for local development as well?

Enter [Skaffold](https://skaffold.dev/), a command-line tool for continuous development on Kubernetes. The tool was [open-sourced](https://github.com/GoogleContainerTools/skaffold) by Google in 2018. Skaffold watches your code and, detecting changes, it handles building, pushing and deploying the application to your local Kubernetes installation. You can even use Skaffold to build your CI/CD pipeline, handling the deployment all the way from local workstation to the production cluster.

In this series of articles, we'll learn how to develop a Kubernetes-native web application. We'll use [Django](https://www.djangoproject.com/) to build our web application, connect it to [Postgres](https://www.postgresql.org/) database, and write Kubernetes manifests to continuously develop the application on a local Minikube cluster. We'll lean Kubernetes concepts such as [deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [services](https://kubernetes.io/docs/concepts/services-networking/service/), [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/), [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/), [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), and [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/).

In this first part of this series, we'll install all the requirements. After you've completed the first part, you can clone the [accompanying repository](https://github.com/ksaaskil/django-postgres-skaffold-k8s) and run

```bash
$ skaffold dev
```

in the root of the repository to deploy the application to your local Minikube cluster. In the next part(s) of the series, we'll build the repository step-by-step.

## Prerequisites

### `kubectl`

First, we'll need `kubectl` to interact with our Kubernetes cluster. The exact details will vary depending on your platform, so follow the instructions [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install `kubectl` on your own machine.

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

If you want to follow along building the repository, you'll need [`django-admin`](https://docs.djangoproject.com/en/3.0/ref/django-admin/) to bootstrap the Django application. Note that this step is optional: we only need to install Django to create the project boilerplate. If you don't want to install Python 3 and Django on your own machine, feel free to copy the code from [the accompanying repository](https://github.com/ksaaskil/django-postgres-skaffold-k8s/tree/master/src/store).

Installing Django requires, first of all, a working installation of [Python 3](https://www.python.org/), so make sure you have that available.

Our Django project will live in `src/store`, so create that folde and `cd` into it:

```bash
$ mkdir -p src/store
$ cd src/store
```

Create `requirements.txt` and include `django`:

```bash
# src/store/requirements.txt
django
```

Now activate your [virtual environment](https://docs.python.org/3/tutorial/venv.html) and install Django:

```bash
$ pip install -r requirements.txt
```

Now, you should be able to find `django-admin` in your `PATH`. We'll use that to bootstrap the project in the next part.

## Conclusion

That concludes the first part. If you followed through this far, you can try and run

```bash
$ skaffold dev
```

in the accompanying repository to ensure everything works. In the next part of the series, we'll build a simple Django application and after that get to the fun stuff: writing Kubernetes manifests. See you then!

## Part 2

---
title: Setting up Django app with Postgres database and health check
published: false
description: Second part of the tutorial on developing a Django application backed by Postgres on local Kubernetes
tags: python,kubernetes,tutorial
series: Learning local development on Kubernetes with Skaffold
---

In [Part 1](https://dev.to/ksaaskil/getting-started-with-local-development-on-kubernetes-with-skaffold-1plc) of this series, we installed all tools required for developing our Django application on local Kubernetes with [Skaffold](https://skaffold.dev/). In this part, we'll create the Django application. In the next part, we'll finally get to the fun part: defining Kubernetes manifests and Skaffold configuration file.

Since this tutorial is not about Django but about Skaffold and Kubernetes, I'll move quickly in this part. If you have any questions, please add them in the comments and I'll do my best to answer! As before, you can find all code in the [accompanying GitHub repository](https://github.com/ksaaskil/django-postgres-skaffold-k8s).

## Creating Django project

We'll create a Django project named `store` in `src/store` with the `startproject` command of `django-admin`:

```bash
# In the root of repository
$ cd src
$ mkdir store
$ cd store
$ django-admin startproject store .
```

Add the following to `requirements.txt`:

```txt
# src/store/requirements.txt
django
gunicorn
psycopg2
```

Here, [`gunicorn`](https://gunicorn.org/) is used for serving the application and [`psycopg2`](https://pypi.org/project/psycopg2/) is the Postgres driver.

Now, let's create an app that we'll use for status-checking:

```bash
# Inside src/store
$ python manage.py startapp status
```

This creates the `status/` folder in `src/store`. Add the following to `store/urls.py`:

```python
# src/store/store/urls.py
from django.urls import path, include

urlpatterns = [path("status/", include("status.urls"))]
```

This will boostrap the `status` app to `status/` endpoint.

Define a view in the root of `status/` path:

```python
# src/store/status/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

In `status/views.py`, add a view that returns 200 for successful database connection and 500 otherwise:

```python
# src/store/status/views.py
from django.db import connection
from django.http import JsonResponse

def index(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({ "message": "OK"}, status=200)
    except Exception as ex:
        return JsonResponse({ "error": str(ex) }, status=500)

```

We check if the database cursor can execute a `SELECT 1` statement and return an error for any exception.

With this, we have created a Django application with `status/` endpoint that checks the database connection. Now we still need to setup [Postgres](https://www.postgresql.org/).

### Setting up Postgres

To setup Postgres, modify `src/store/settings.py` as follows:

```python
# src/store/settings.py
import os

# Keep everything else as-is

POSTGRES_CONFIG = {
    "username": os.environ.get("POSTGRES_USER", "postgres"),
    "db_name": os.environ.get("POSTGRES_DB", "store"),
    "host": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
    "password": os.environ.get("POSTGRES_PASSWORD", ""),
    "port": os.environ.get("POSTGRES_PORT", 5432),
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_CONFIG["db_name"],
        "USER": POSTGRES_CONFIG["username"],
        "PASSWORD": POSTGRES_CONFIG["password"],
        "HOST": POSTGRES_CONFIG["host"],
        "PORT": POSTGRES_CONFIG["port"],
    }
}
```

Here we read the Postgres settings from environment variables and set sane defaults.

### Dockerfile

To deploy the application to Kubernetes, we'll need to create a `Dockerfile`:

```Dockerfile
# src/store/Dockerfile
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /store
WORKDIR /store
COPY . /store/
RUN pip install -r requirements.txt
CMD ["gunicorn", "store.wsgi"]
```

We use `gunicorn` for serving the app, starting from `store/wsgi.py` created by the `django-admin startproject` command.

### Nginx

In any production environment, we need to run Django behind a reverse proxy or ingress, so we'll create an [nginx](https://nginx.org/en/) proxy. Add the following to `Dockerfile.nginx`:

```Dockerfile
# src/store/Dockerfile.nginx
FROM nginx:1.16.1
COPY nginx.conf /etc/nginx/nginx.conf
```

Add the following setup from [gunicorn documentation](https://docs.gunicorn.org/en/latest/deploy.html#nginx-configuration) to `nginx.conf`:

```nginx
# src/store/nginx.conf
# https://docs.gunicorn.org/en/latest/deploy.html#nginx-configuration
user nobody nogroup;
# 'user nobody nobody;' for systems with 'nobody' as a group instead
error_log  /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024; # increase if you have lots of clients
    accept_mutex off; # set to 'on' if nginx worker_processes > 1
}
http {
    upstream store {
        server localhost:8000;
    }

    server {
        listen 8080;

        location / {
            proxy_pass http://store;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host;
            proxy_redirect off;
        }
    }
}
```

Here we simply hard-code the proxy to forward requests to `localhost:8000`, where our Django app will be running. In production usage, we would read the address from environment variables at deploy time. 

## Conclusion

This concludes Part 2 of our tutorial for local development on Skaffold. In the next part, we'll get to deploying our application and database on Minikube with Skaffold. See you then!

## Part 3

---
title: How to deploy Postgres on Kubernetes with Skaffold
published: false
description: Learn Kubernetes concepts such as config maps, secrets, persistent volumes and claims, stateful sets, and services
tags: postgres,kubernetes,tutorial,skaffold
series: Learning local development on Kubernetes with Skaffold
---

Hello again! In this part of the series, we'll finally get our hands dirty using [Skaffold](https://skaffold.dev/) to build, push and deploy applications on [Kubernetes](https://kubernetes.io/). In this part, we'll deploy a [Postgres](https://www.postgresql.org/) database on our local Minikube cluster. Along the way, we'll learn Kubernetes concepts such as [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/), [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/), [Persistent Volumes and Persistent Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/), and [Services](https://kubernetes.io/docs/concepts/services-networking/service/).

In [Part 1](https://dev.to/ksaaskil/getting-started-with-local-development-on-kubernetes-with-skaffold-1plc) of this series, we installed all dependencies required for this tutorial. Most notably, you'll need a [Skaffold](https://skaffold.dev/docs/install/) installation and a Kubernetes cluster. I assume you're using [Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/), but you could also use other [local clusters](https://skaffold.dev/docs/environment/local-cluster/) such as [Docker Desktop](https://docs.docker.com/docker-for-mac/kubernetes/).

You can find all code accompanying this series in [this GitHub repository](https://github.com/ksaaskil/django-postgres-skaffold-k8s).

## Configuring Skaffold

First we'll need to configure Skaffold by creating a [`skaffold.yaml`](https://skaffold.dev/docs/references/yaml/) file in our repository. I suggest you take a quick glance at the link to get an overview of Skaffold's configuration.

Like any resource definition in Kubernetes, `skaffold.yaml` has `apiVersion`, `kind`, and `metadata` fields. We therefore add the following to `skaffold.yaml`:

```yaml
# skaffold.yaml
apiVersion: skaffold/v2beta4
kind: Config
metadata:
  name: learning-local-kubernetes-development-with-skaffold
```

The meat of Skaffold is in `build` and `deploy` fields. For now, we assume there are no artifacts to build and add the following below the definition above:

```yaml
build:
  artifacts: []
```

In `deploy`, we tell Skaffold where to find the Kubernetes manifests and how to process them. We'll tell Skaffold to deploy with `kubectl`, look for manifests in a folder called `k8s/` and to use the `minikube` context for deployment with the following configuration:

```yaml
# skaffold.yaml
deploy:
  kubectl:
    manifests:
      - k8s/*.yaml
  kubeContext: minikube
```

Both `manifests` and `kubeContext` are set to above values by default, but I think it's always better to be explicit with such things. Instead of deploying bare Kubernetes manifests with [`kubectl`](https://kubernetes.io/docs/reference/kubectl/overview/), you could also tell Skaffold to process your manifests with [`kustomize`](https://kustomize.io/) or use [`helm`](https://helm.sh/) charts.

Instead of writing `skaffold.yaml` yourself, you can also use [`skaffold init`](https://skaffold.dev/docs/pipeline-stages/init/) command to auto-generate `build` and `deploy` config.

## Postgres deployment

### `ConfigMap` and `Secrets`

We'll put our Kubernetes manifest for the Postgres deployment in `k8s/postgres.yaml`. We'll first include non-confidential Postgres configuration data in a ConfigMap. By storing configuration in ConfigMap, we can easily re-use the configuration in other services using our Postgres cluster.

For Postgres, we'll need to define the Postgres user name and the database to use. We add these as configuration variables `POSTGRES_USER` and `POSTGRES_DB` in `k8s/postgres.yaml`:

```yaml
# k8s/postgres.yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-configuration
data:
  POSTGRES_DB: "django-db"
  POSTGRES_USER: "postgres-user"
```

We'll see later how to use this configuration.

Postgres also wants us to configure the password that can be used to access the database. Such confidential data should be stored as [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/). Kubernetes wants us to base64-encode our secrets, so we'll have to do that first. Assuming that we choose `"super-secret"` as our password, here's how to base64-encode:

```
$ echo -n "super-secret" | base64
c3VwZXItc2VjcmV0
# Or with Python:
$ python -c "import base64; print(base64.b64encode('super-secret'));"
c3VwZXItc2VjcmV0
```

For the purposes of this tutorial, I'll simply add the base64-encoded secret in `postgres.yaml`:

```yaml
# k8s/postgres.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-credentials
type: Opaque
data:
  # This should **not** be in version control
  password: c3VwZXItc2VjcmV0
```

In any real-world use, you probably wouldn't add secrets like this to version control. You would put the secrets in their own `secrets.yaml` file and keep it out of version control or read secrets at deployment time from services such as [Vault](https://www.vaultproject.io/).

At this point, we can see if our Skaffold deployment works by running `skaffold dev`. Skaffold should discover `postgres.yaml` and deploy our ConfigMap and Secret. If you then open Minikube dashboard with

```bash
$ minikube dashboard
```

you should find the ConfigMap and Secret in the created resources. If you modify your deployment manifests, Skaffold should automatically take care of updating the deployment so from now on, you can keep `skaffold dev` running in the background.

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
