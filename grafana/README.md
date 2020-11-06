# Grafana Playground

Install Grafana dashboard to Brani cluster using following helm-chart:

https://github.com/grafana/helm-charts/tree/main/charts/grafana

## Deploying Grafana

1. Add grafana repo to helm.

    ```console
    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update
    ```

2. Modify the values file in `grafana-chart/values.yaml` as needed. Note the following key points:

    - `rbac` values should be set to `false`
    - Enable ingress by setting `ingress.enabled` to `true` and `ingress.hosts` to `<URL_NAME>.k8s.brani.aisingapore.net` where `<URL_NAME>` can be url name that you fancy.
    - you can set the admin password at the `adminPassword` field
    - If you know the prometheus URL beforehand (URL can be clusterIP of the prometheus service), you can set it in `datasources.url`. Else, comment out line `datasources.yaml` to line `isDefault` and append `{}` to `datasources`.
    - For repeated grafana deployments, you may choose save your dashboard as a json file during the first deployment and then reuse it in subsequent deployments. Instructions refer to the [grafana helm github](https://github.com/grafana/helm-charts/tree/main/charts/grafana#import-dashboards). A sample dashboard is provided at [grafana-chart/custom-dashboard](../grafana-chart/custom-dashboard)

3. Install helm chart using the modified values file.

    ```console
    helm install <NAME_OF_GRAFANA_DEPLOYMENT> grafana/grafana -f grafana.values.yaml
    ```

4. Log into Grafana using the adminuser and adminpassword from the values.yaml. If adminpassword is not set in values.yaml, run the following command to obtain password.

    ```console
    kubectl get secret <NAME_OF_GRAFANA_DEPLOYMENT> -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
    ```

5. To add the prometheus datasource (If datasource was already added using the values.yaml, skip this step):

    - On the left taskbar, under Configuration (cogwheel), click Data Sources.
    - Click Add data source
    - Enter the Name
    - Switch Default to On
    - Enter the URL of prometheus datasource. You can use kubectl service to get the URL of the prometheus service.
    - Leave the other settings alone.
    - Click Save & Test.
    - Ensure that the message Data source is working appears. Else, recheck the URL.

6. To create a new dashboard (If dashboard was already deployed using the values.yaml, skip this step):

    - On the left taskbar, under Create (plus sign), click Dashoard
    - Click Add new panel
    - Enter the PromQL query that Prometheus was scrapping.
    - Configure the panel accordingly.
    - To save panel, on the top right corner, click Save then click Apply.
    - To save dashboard, on the top right corner, click Save (diskette icon).

7. (Optional) To export dashboard as JSON
    - On the top right corner, click Dashboard Settings (cogwheel)
    - Click JSON model
    - Copy and paste json contents into json file. 

![alt text](/sample-chart.png "Tensorfood-Sample-Dashboard")