# Django + Postgres + Skaffold + Kubernetes

Example [Django](https://www.djangoproject.com/) application running on [Postgres](https://www.postgresql.org/) with Kubernetes deployment using [Skaffold](https://skaffold.dev/). See [`skaffold.yaml`](./skaffold.yaml) for Skaffold configuration.

## ⚠️ Pre-requisites

- [Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/) or [Docker Desktop](https://www.docker.com/products/kubernetes)
- [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Skaffold](https://skaffold.dev/)
- Optional: [`kustomize`](https://github.com/kubernetes-sigs/kustomize)

## Getting started

The project uses [Skaffold](https://skaffold.dev/) to build resources and deploy to Kubernetes. See the configuration in [`./skaffold.yaml`](./skaffold.yaml) and manifests in [`k8s/`](./k8s) folder.

If you want to persist Postgres data, you can create a folder such as `~/postgres-data` and mount it to Minikube:

```bash
$ mkdir ~/postgres-data
$ minikube mount ~/postgres-data:/mnt1/postgres-data
```

Build images:

```bash
$ skaffold build
```

Deploy in development mode with hot reloading of code:

```bash
$ skaffold dev [--port-forward]
```

You can test the deployment by making a request to `localhost:8080`:

```bash
$ curl http://localhost:8080/status/
{ "message": "OK" }
```

Run build and deploy once:

```bash
$ skaffold run [--tail] [--port-forward]
```

Delete resources:

```bash
$ skaffold delete
```

See what Skaffold deploys:

```bash
$ skaffold render
```

Connect to Postgres at forwarded port (here assumed to be 5433):

```bash
$ psql -p 5433 -h 127.0.0.1 -Upostgres-user django-db
```

## Debugging

List pods:

```bash
$ kubectl get pods
```

Access Python in Django pod (replace pod name with your `store` pod):

```bash
$ kubectl exec $PODNAME -it -- python manage.py shell
```

Access `psql` in Postgres container:

```bash
$ kubectl exec postgres-statefulset-0 -it -- psql -Upostgres-user -ddjango-db
```
