echo "Cluster Name: "
read CLUSTER

echo "Enter Namespace : "
read NAMESPACE

context=$(kubectl config set-context --current --namespace=$NAMESPACE)

kubectl get deploy -o json | ./jq '[.items[] | {apiname: .metadata.name, replicas: .status.replicas }]' > /home/user/Logs/${CLUSTER}_${NAMESPACE}_deploy.txt
