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
published: true
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

### Persistent volumes and volume claims

Next we'll setup volumes for our Postgres installation. This part is not required if you only use Postgres for local development with small data volumes. If you're deploying Postgres for production in Kubernetes, you need to think carefully where and how to persist data.

Persistent volume (PV) [documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) describe it as "a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)." Storage classes can be used to provision storage on-demand from, say, [Amazon Elastic Block Store](https://aws.amazon.com/ebs/) or [Google Cloud Persistent Disk](https://cloud.google.com/persistent-disk). In this tutorial, we'll provision local storage upfront without storage classes.

In this tutorial, we'll provision storage from the host with _hostPath_ persistent volume. As the [docs explain](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/), "In a production cluster, you would instead provision a network resource like a Google Compute Engine persistent disk, an NFS share, or an Amazon Elastic Block Store volume."

Here's how to use _hostPath_ to provision storage from the single-node cluster's host:

```yaml
# k8s/postgres.yaml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt1/postgres-data
```

We specify that a persistent volume called `postgres-pv` of 1 GB capacity should be provisioned at `/mnt1/postgres-data` on the cluster's node. Access mode is defined as `ReadWriteOnce`, meaning that the volume can be mounted by a single node for reading and writing.

Once we get Postgres running, we can ssh into your Minikube node with `minikube ssh` and execute `ls /mnt1/postgres-data` to browse the data stored by Postgres.

Now that we have provisioned storage, we need to create a _persistent volume claim_ to request access to it. Volume claims are similar to how pods request resources from nodes. Instead of requesting CPU or memory, volume claims request specific storage size ("5 GB") and specific access mode. Let's create a volume claim to request 500 MB from `postgres-pv` volume:

```yaml
# k8s/postgres.yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  labels:
    type: local
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
  volumeName: postgres-pv
```

Now we can use this claim named `postgres-pvc` to mount the claimed storage to our Postgres pod.

### Stateful set

We're ready to declare how to deploy Postgres itself. Just for fun, we'll deploy Postgres using [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/). StatefulSet manages not only the deployment and scaling of pods but also "provides guarantees about the ordering and uniqueness of these pods". In particular, StatefulSet provides unique network identifiers, persistent storage, graceful deployment and scaling, and automated rolling updates. For example, if you were deploying [Apache Cassandra](https://cassandra.apache.org/), an open-source distributed database, on Kubernetes, StatefulSet would guarantee your pods would have stable identifiers such as `cassandra-1`, `cassandra-2`, etc. you could use to communicate between pods even after rescheduling. See [here](https://kubernetes.io/docs/tutorials/stateful-application/cassandra/) for an example how to deploy Cassandra on Kubernetes.

In our case of Postgres, we are dealing with a centralized, non-distributed database, so we'll only have one pod in our StatefulSet. However, StatefulSet is still a very useful and powerful concept for any stateful application.

We'll declare StatefulSet as follows:

```yaml
# k8s/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-statefulset
spec:
  serviceName: "postgres"
  replicas: 1
  selector:
    matchLabels:
      app: postgres # has to match .spec.template.metadata.labels
  template: ...
```

As expected, we use `kind: StatefulSet`. In `spec`, we declare `serviceName` to be `postgres`. You can read [here](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#stable-network-id) how `serviceName` controls the DNS for pods in the StatefulSet. Do not confuse this with how you would use [Service](https://kubernetes.io/docs/concepts/services-networking/service/) to expose Postgres to other applications in the cluster or to the outside world. In the next section, we'll see how to use Service to expose the StatefulSet as a network service.

After `serviceName`, we set `replicas` equal to one as we're dealing with a non-replicated, centralized database. The `.spec.selector` field defines which pods belong to the StatefulSet.

The spec for pods in the StatefulSet is defined in `.spec.template` as follows:

```yaml
# k8s/postgres.yaml
...
spec:
  ...
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:12
          envFrom:
            - configMapRef:
                name: postgres-configuration
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
          ports:
            - containerPort: 5432
              name: postgresdb
          volumeMounts:
            - name: postgres-volume-mount
              mountPath: /var/lib/postgresql/data
          readinessProbe:
            exec:
              command:
                - bash
                - "-c"
                - "psql -U$POSTGRES_USER -d$POSTGRES_DB -c 'SELECT 1'"
            initialDelaySeconds: 15
            timeoutSeconds: 2
          livenessProbe:
            exec:
              command:
                - bash
                - "-c"
                - "psql -U$POSTGRES_USER -d$POSTGRES_DB -c 'SELECT 1'"
            initialDelaySeconds: 15
            timeoutSeconds: 2
      volumes:
        - name: postgres-volume-mount
          persistentVolumeClaim:
            claimName: postgres-pvc
```

We first set pod labels to `postgres` to match the selector in the StatefulSet. In `.spec.template.spec`, we define our pods to have a single container running `postgres:12` image from [DockerHub](https://hub.docker.com/_/postgres/). The pod uses environment variables from the `postgres-configuration` ConfigMap and `postgres-credentials` Secret, both of which we defined above. We then set the pod to expose port 5432. In `volumeMounts`, we mount a volume named `postgres-volume-mount` to `/var/lib/postgresql/data`, the folder used by Postgres for storing data. This volume is defined in `.spec.template.spec.volumes`, where we use the `postgres-pvc` volume claim defined above.

Finally, we also set `readinessProbe` as well as `livenessProbe` to let Kubernetes monitor the pod's health. You can read more about probes [here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

### Service

Having declared our StatefulSet, we'll finally need to define a [Service](https://kubernetes.io/docs/concepts/services-networking/service/) to expose the StatefulSet as a network application to other applications. Compared to above, this is simple enough:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  ports:
    - port: 5432
      name: postgres
  type: NodePort
  selector:
    app: postgres
```

In our service, we expose port 5432 from the pod as `NodePort`. You can read more about different options [here](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types). Choosing `NodePort` will let us contact the service from outside the cluster. In production, you of course very carefully want to consider if you want your database to be exposed outside of the cluster.

### Did it work?

If you had `skaffold dev --port-forward` running throughout this tutorial, you should now have Postgres running in your Minikube cluster. You can verify this by, for example, running `minikube dashboard` to browse the resources in Minikube and hopefully see everything glowing green. If anything went wrong, please let me know in the comments!

## Conclusion

That concludes the tutorial on how to get Postgres running on Kubernetes. In the next and final part, we'll finally deploy the Django application we built in Part 2, backed by Postgres. See you then!

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

## Part 4

---
title: How to deploy Django on Kubernetes with Skaffold for development and production
published: true
description: Learn Kubernetes concepts such as deployments, services, and jobs
tags: django,kubernetes,beginner,skaffold
series: How to develop Kubernetes-native applications with Skaffold
---

In this article, we'll see how to deploy the Django application built in [Part 2](https://dev.to/ksaaskil/setting-up-django-app-with-postgres-database-and-health-check-2cpd) of this series to local Kubernetes cluster. We'll be using [Skaffold](https://skaffold.dev/) for the deployment. Skaffold offers support for multiple [profiles](https://skaffold.dev/docs/environment/profiles/), making it useful both local development with hot code reloading as well as production deployments.

Our Django application has a single view at `/status` endpoint. Calling the endpoint checks the connection to the Postgres database. We created the Kubernetes deployment for the database in [Part 3](https://dev.to/ksaaskil/how-to-deploy-postgres-on-kubernetes-with-skaffold-32fl).

The accompanying code for this article can be found in [this GitHub repository](https://github.com/ksaaskil/django-postgres-skaffold-k8s).

### Dockerfiles

Let's start by containerizing our Django application. In Part 2, we created the following `Dockerfile` for the Django app:

```dockerfile
# src/store/Dockerfile
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /store
WORKDIR /store

COPY requirements.txt /store
RUN pip install -r requirements.txt

COPY . /store

RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "store.wsgi"]
```

We use [Gunicorn](https://gunicorn.org/) server for serving the Django application as instructed in [Django documentation](https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/gunicorn/).

Now we want to tell Skaffold to build this Docker image. Let's modify the `skaffold.yaml` we created in Part 3 as follows:

```yaml
# skaffold.yaml
apiVersion: skaffold/v2beta4
kind: Config
metadata:
  name: learning-local-kubernetes-development-with-skaffold
build:
  artifacts:
    - image: django-store
      context: src/store
deploy:
  kubectl:
    manifests:
      - k8s/*.yaml
  kubeContext: minikube # Default
```

The important part here is the list of `artifacts` under `build`. We name the Docker image for our Django application as `django-store` and use `src/store` as its build context. Run `skaffold build` and Skaffold should build the Docker image.

Before deployments, you should set [`kubeContext`](https://skaffold.dev/docs/environment/kube-context/) in `skaffold.yaml` to point to the Kubernetes cluster you want to use. If you're using Docker Desktop, you'd use `kubeContext: docker-for-desktop`. When deploying to production, you should override the `kubeContext` with a suitable Skaffold profile.

Before moving to Kubernetes deployments, we need to add a reverse proxy before our Gunicorn server. We use an [nginx](https://nginx.org/en/) proxy server with custom `nginx.conf`. In production usage, you'd probably use something like [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/) instead.

Here's the Dockerfile for our reverse proxy:

```dockerfile
# src/store/Dockerfile.nginx
FROM nginx:1.16.1
COPY nginx.conf /etc/nginx/nginx.conf
```

You can find an example `nginx.conf` in the [repository](https://github.com/ksaaskil/django-postgres-skaffold-k8s/blob/master/src/store/nginx.conf). See also [Part 2](https://dev.to/ksaaskil/setting-up-django-app-with-postgres-database-and-health-check-2cpd) of this series if you need a reminder.

Let's add this Dockerfile also to the list of artifacts to build:

```yaml
# skaffold.yaml
...
build:
  artifacts:
    - image: django-store
      context: src/store
    - image: django-store-nginx
      context: src/store
      docker:
        dockerfile: Dockerfile.nginx
```

We use the same build context as before but a different `Dockerfile`. Again you can run `skaffold build` and you should see Skaffold now building two images (unless found locally already).

### Deployment

We'll be adding our deployment configuration to `k8s/store.yaml`. Remember how we configured `skaffold.yaml` to search for manifests in the `k8s/` folder:

```yaml
# skaffold.yaml
...
deploy:
  kubectl:
    manifests:
      - k8s/*.yaml
```

Let's first create a [Kubernetes deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) for our Django application. Deployments are a declarative way to manage [pods](https://kubernetes.io/docs/concepts/workloads/pods/) and [replica sets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/). We want to specify tha Kubernetes should always have one pod running for our application. If the pod crashes, Kubernetes automatically restarts the pod for us.

Here's the full configuration for the deployment:

```yaml
# k8s/store.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: store-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: store
  template:
    metadata:
      labels:
        app: store
    spec:
      containers:
        - name: store
          image: django-store
          ports:
            - containerPort: 8000
          env:
            - name: POSTGRES_HOST
              value: "postgres-service"
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
          envFrom:
            - configMapRef:
                name: postgres-configuration
        - name: store-nginx
          image: django-store-nginx
          ports:
            - containerPort: 8080
```

We name our deployment `store-deployment` by specifying `.metadata.name` field. The `.spec.replicas` field says we want the deployment to have one running replica. The `.spec.selector` tells the deployment how to find which pods to manage as part of the deployment: we tell it to watch for pods with label `app: store`. The deployed pods are given this `app:store` label in `.spec.template.metadata.labels` field.

The `.spec.template.spec.containers` defines the two containers running in the pod. The first container is running the `django-store` image, with Gunicorn as entrypoint. The second container is running nginx, routing requests to `django-store` container. The two containers are exposing ports 8000 and 8080, respectively. Remember, this second container would most likely be replaced by an NGINX Ingress Controller in your production deployment.

The environment variable `POSTGRES_HOST` is set to point to `postgres-service`, the [Service](https://kubernetes.io/docs/concepts/services-networking/service/) we created in the previous part to expose the Postgres database. The variable `POSTGRES_PASSWORD` is read from the [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/) `postgres-credentials` and its data named `password`. This secret was created as follows in the previous part:

```yaml
# k8s/postgres.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-credentials
type: Opaque
data:
  # This should not be in version control in real deployments
  password: c3VwZXItc2VjcmV0
---
```

The variables `POSTGRES_DB` and `POSTGRES_USER` are filled by reading from the [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) named `postgres-configuration` we also created:

```yaml
# k8s/postgres.yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-configuration
  labels:
    app: postgres
data:
  POSTGRES_DB: "django-db"
  POSTGRES_USER: "postgres-user"
---
```

### Service

Now we must expose our application as Kubernetes Service. This is reasonably simple:

```yaml
# k8s/store.yaml
---
apiVersion: v1
kind: Service
metadata:
  name: django-store-service
spec:
  ports:
    - port: 8080
      targetPort: 8080
  type: NodePort
  selector:
    app: store
---
```

The service named `django-store-service` exposes port 8080. It routes requests to port `8080` in the `app: store` pod. This port is served by the NGINX container in the pod.

### Django migrations

We run Django's [database migrations](https://docs.djangoproject.com/en/3.1/topics/migrations/) as [Kubernetes jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/). We'll simply include the migration job in `store.yaml` as follows:

```yaml
# k8s/store.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: django-migrations-job
spec:
  backoffLimit: 10
  template:
    spec:
      containers:
        - name: django-migration
          image: django-store
          command: ["python", "manage.py", "migrate"]
          env:
            - name: POSTGRES_HOST
              value: "postgres-service"
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
          envFrom:
            - configMapRef:
                name: postgres-configuration
      restartPolicy: Never
```

This job is tried ten times before failing. It's very common the first job fails because the service may not be ready. That's fine as Kubernetes will take care of retries.

### Conclusion

Now we have everything ready to deploy the application to our Kubernetes cluster! Let's make a one-off deployment with `skaffold run`:

```bash
$ skaffold run --tail --port-forward
```

The `--tail` argument allows us to watch the logs and `--port-forward` exposes all services in the cluster. Once the application becomes available, you can make a request to `localhost:8080`:

```bash
$ curl http://localhost:8080/status/
{"message": "OK"}
```

Congratulations, you've deployed Django on Kubernetes!

For development and hot reloading of code, use `skaffold dev`:

```bash
$ skaffold dev --port-forward
```

Whenever you change the code in your application, Skaffold will re-build the Docker image and re-deploy it to the cluster. No more messing with Docker Compose and volume mounts, you've built a true Kubernetes-native application! See the full list of Skaffold's commands [here](https://skaffold.dev/docs/references/cli/).

Please leave a comment if you have any questions or thoughts on this article! Thanks for reading, see you next time!
