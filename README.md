# SnipBalancer

A Load-Balanced URL Shortener

---
<details>
<summary>Week 1</summary>

## Week 1: To Build the URL Shortener in Docker


## 1. Set Up a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2. Create a Docker Network for Redis

```bash
docker network create redis
```

---

## 3. Prepare the Clustering Environment (Navigate to the clustering directory)

```bash
chmod +x script.sh
./script.sh
docker pull redis:7.4.2-alpine
```

---

## 4. Build and Run the SnipBalancer Docker Image

Build the image (development target):

```bash
docker build --target dev -t snipbal .
```

Or build the default image:

```bash
docker build -t snipbal .
```

Run the container:

```bash
docker run -it -v "${PWD}:/work" -p 5000:5000 \
    --net redis \
    -e REDIS_SENTINELS="sentinel-0:5000,sentinel-1:5000,sentinel-2:5000" \
    -e REDIS_MASTER_NAME="mymaster" \
    -e REDIS_PASSWORD="okok" \
    snipbal
```

---

## 5. Check Redis Status

Access a Redis container shell:

```bash
docker exec -it redis-0 sh
```

Connect with Redis CLI:

```bash
redis-cli
auth <password>
KEYS *
GET <key_val>
```

---

## Notes

- Replace `<password>` and `<key_val>` with your password and desired Redis key.

</details>


<details>
<summary> Week 2</summary>

## Week 2: Deploy the URL Shortener using Kubernetes

### 1. Create a Kubernetes Cluster with Kind

```bash
kind create cluster --name redis --image kindest/node:v1.23.5
```

### 2. Create a Namespace for Redis

```bash
kubectl create ns redis
```

### 3. Deploy Redis Cluster

Navigate to the `redis/kubernetes/` directory and apply the configuration files:

```bash
kubectl apply -n redis -f ./redis/redis-configmap.yaml
kubectl apply -n redis -f ./redis/redis-statefulset.yaml
```

Check the status of pods and persistent volumes:

```bash
kubectl -n redis get pods
kubectl -n redis get pv
```

### 4. Verify Redis Cluster

Access the Redis pod shell:

```bash
kubectl -n redis exec -it redis-0 -- sh
```

Connect to Redis CLI and check replication status:

```bash
redis-cli
auth <your-redis-password>
info replication
```

View logs for Redis pods:

```bash
kubectl -n redis logs redis-0
kubectl -n redis logs redis-1
kubectl -n redis logs redis-2
```

### 5. Deploy Redis Sentinel

Apply the Sentinel StatefulSet:

```bash
kubectl apply -n redis -f ./sentinel/sentinel-statefulset.yaml
```

Check Sentinel pods and logs:

```bash
kubectl -n redis get pods
kubectl -n redis get pv
kubectl -n redis logs sentinel-0
```

### 6. Deploy SnipBalancer Application

Navigate to the `/redis/kubernetes/app/` directory and deploy the application:

```bash
kubectl apply -n redis -f app-deployment.yaml
kubectl apply -n redis -f app-configmap.yaml
kubectl apply -n redis -f app-secret.yaml
```

### 7. Verify Application Deployment

Check if the SnipBalancer pods are running:

```bash
kubectl get pods -n redis -l app=snipbal
```

Check deployment and service status:

```bash
kubectl get deployment -n redis snipbal
kubectl get service -n redis snipbal
```

### 8. Access the Application

Port-forward the SnipBalancer service to your local machine:

```bash
kubectl port-forward -n redis service/snipbal 5000:5000
```

### 9. Debugging and Logs

Get the names of SnipBalancer pods:

```bash
kubectl get pods -n redis -l app=snipbal
```

Check logs for a specific pod:

```bash
kubectl logs -n redis <pod-name>
```

### 10. Interact with Redis

Access the Redis CLI from a pod:

```bash
kubectl exec -it -n redis redis-0 -- redis-cli
```

Authenticate and interact with Redis:

```bash
auth <your-redis-password>
KEYS *
GET <key_name>
```

### 11. Testing Failover and High Availability

To verify Redis Sentinel failover and cluster availability:

1. **Check Current Redis Master:**
    ```bash
    kubectl exec -n redis sentinel-0 -- redis-cli -p 5000 SENTINEL get-master-addr-by-name mymaster
    ```

2. **Simulate Master Failure:**
    ```bash
    kubectl delete pod -n redis redis-0
    ```

3. **Monitor Sentinel Logs for Failover Events:**
    ```bash
    kubectl logs -f -n redis sentinel-0
    ```

4. **Check Pod Status and Master Re-election:**
    ```bash
    kubectl -n redis get pods -o wide
    ```

5. **Verify New Master:**
    - Repeat step 1 to confirm which Redis pod is now the master.
    - You can also refer to step 4 above to check the roles of `redis-0`, `redis-1`, and `redis-2`.

> These steps help ensure your Redis cluster remains available and automatically recovers from node failures.

## Notes

- Replace `<password>` and `<key_val>` with your password and desired Redis key.

</details>


<details>
<summary>Week 3 </summary>

## Week 3: Scaling, Load Balancing & Monitoring

### 1. Enable Horizontal Pod Autoscaling (HPA)

Navigate to the `/redis/kubernetes/app` directory and apply the HPA configuration:

```bash
kubectl apply -f app-hpa.yaml -n redis
```

### 2. Deploy Metrics Server

Navigate to the `/redis/kubernetes/metric-server` directory and deploy the metrics server:

```bash
kubectl apply -f components.yaml -n redis
```

### 3. Generate Load for Autoscaling

Start a temporary load generator pod:

```bash
kubectl run -n redis -it --rm load-generator --image=busybox -- /bin/sh
```

Inside the `load-generator` pod shell, run the following command to continuously send requests to the SnipBalancer service:

```bash
while true; do wget -q -O- http://snipbal:5000; done
```

You can exit the load generator at any time by pressing `Ctrl + C`.

### 4. Monitor Autoscaling Activity

In separate terminals, monitor the status of pods and the HPA:

```bash
kubectl get pods -n redis --watch
kubectl get hpa -n redis --watch
```

Observe as the HPA scales the number of SnipBalancer pods up and down in response to the generated load. After stopping the load generator, the number of replicas will decrease following the HPA cooldown period (typically 10–15 minutes).

> **Note:** The cooldown period is a standard HPA property and may vary based on your configuration.


## Stress Testing

To perform stress testing on the SnipBalancer application, follow these steps:

1. **Navigate to the `stress-tests` directory:**
    ```bash
    cd stress-tests
    ```

2. **Make the test scripts executable:**
    ```bash
    chmod +x get-test.sh
    chmod +x post-test.sh
    ```

3. **Run the Application and Start Stress Tests**

```bash
kubectl port-forward -n redis service/snipbal 5000:5000
```

Then, in a separate terminal, run a stress test:

```bash
# For GET requests:
./get-test.sh

# Or for POST requests:
./post-test.sh
```

4. **Monitor Scaling Activity in Real Time**

Open another terminal and watch the scaling behavior:

```bash
kubectl get pods -n redis --watch
kubectl get hpa -n redis --watch
```

These steps will help you observe how the application automatically scales up and down in response to increased load.

</details>

> **Reference:**  
> This project setup was taken from [this guide](https://github.com/marcel-dempers/docker-development-youtube-series/blob/master/python/introduction/part-5.database.redis/README.md).
