# Example Skaffold project

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

```bahs
$ skaffold render
```
