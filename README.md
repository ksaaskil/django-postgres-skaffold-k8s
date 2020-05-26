# Django + Postgres + Skaffold + Kubernetes

Example [Django](https://www.djangoproject.com/) application running on [Postgres](https://www.postgresql.org/) with Kubernetes deployment using [Skaffold](https://skaffold.dev/). See [`skaffold.yaml`](./skaffold.yaml) for Skaffold configuration.

## ⚠️ Pre-requisites

- [Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)
- [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [`kustomize`](https://github.com/kubernetes-sigs/kustomize)
- [Skaffold](https://skaffold.dev/)

## Getting started

The project uses [Skaffold](https://skaffold.dev/) to build resources and deploy to Kubernetes. See the configuration in [`./skaffold.yaml`](./skaffold.yaml) and manifests in [`k8s/`](./k8s) folder.

Postgres data is persisted to `/var/lib/postgres-data` by default, so you need to create the folder and add permissions to access it:

```bash
$ sudo mkdir /var/lib/postgres-data
$ sudo chown -R $USER /var/lib/postgres-data
```

Run in build and deploy in development mode:

```bash
$ skaffold dev [--port-forward]
```

Run build and deploy once:

```bash
$ skaffold run
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
$ PGPASSWORD=super-secret sql -p 5433 -h 127.0.0.1 -Upostgres-user django-db
```
