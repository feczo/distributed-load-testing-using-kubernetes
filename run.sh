export ZONE=europe-west1-d
export CLUSTER_NAME=crunch
read -p "Please enter your Project ID: " PROJECT_ID
gcloud config set compute/zone $ZONE
gcloud config set project $PROJECT_ID
gcloud app -q deploy sample-webapp/app.yaml --project=$PROJECT_ID

sed -i.bak "s/workload-simulation-webapp/$PROJECT_ID/" ./kubernetes-config/locust-master-controller.yaml
sed -i.bak "s/workload-simulation-webapp/$PROJECT_ID/" ./kubernetes-config/locust-worker-controller.yaml

gcloud alpha container clusters create $CLUSTER_NAME --zone=$ZONE --machine-type=f1-micro

kubectl config use-context "gke""_""$PROJECT_ID""_""$ZONE""_""$CLUSTER_NAME"
gcloud -q beta auth application-default login
gcloud config set container/cluster $CLUSTER_NAME
gcloud container clusters get-credentials $CLUSTER_NAME

# fixing a config validation bug
sed -i.bak '/key: LOCUST_MODE/d' ./kubernetes-config/locust-master-controller.yaml ./kubernetes-config/locust-worker-controller.yaml
sed -i.bak '/key: TARGET_HOST/d' ./kubernetes-config/locust-master-controller.yaml ./kubernetes-config/locust-worker-controller.yaml
sed -i.bak '/key: LOCUST_MASTER/d' ./kubernetes-config/locust-worker-controller.yaml

kubectl create -f ./kubernetes-config/locust-master-controller.yaml
kubectl create -f ./kubernetes-config/locust-master-service.yaml
kubectl create -f ./kubernetes-config/locust-worker-controller.yaml
echo gcloud compute firewall-rules create "$CLUSTER_NAME""_""8089" --allow=tcp:8089 --target-tags gke-CLUSTER-NAME-[...]-node

