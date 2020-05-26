# Example Skaffold project

## Prerequisites

- [Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)
- [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [`kustomize`](https://github.com/kubernetes-sigs/kustomize)
- [Skaffold](https://skaffold.dev/)

## Skaffold

The project uses [Skaffold](https://skaffold.dev/) to build resources and deploy to Kubernetes. See the configuration in [./skaffold.yaml](./skaffold.yaml) and manifests in [`k8s/`](./k8s) folder.

Run in development mode:

```bash
$ skaffold dev [--port-forward]
```

Run one time:

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
