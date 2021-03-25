kubectl get pods --all-namespaces -o wide | grep Evicted | awk '{ printf "kubectl delete pod %s \n", $1}' | sh
kubectl get pods --all-namespaces -o wide | grep Terminating | awk '{ printf "kubectl delete pod %s \n", $1}' | sh
