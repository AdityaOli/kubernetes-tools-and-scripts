NAMESPACES=$(kubectl get ns)
ALL_NAMESPACES=($NAMESPACES)
for namespace in "${ALL_NAMESPACES[@]}"; do 
  KUBENS_RUN=$(kubectl config set-context --current --namespace=$namespace)
  echo "========================================= $namespace ========================================="  
  all_namespace_pods=$(kubectl get pods --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
  arrayOfPods=($all_namespace_pods)
  for eachPod in "${arrayOfPods[@]}"; do 
    podStatus=$(kubectl describe pods $eachPod | grep ^Status: | head -1 | awk '{print $2}' | tr -d '\n')
      if [ "$podStatus" != "Running" ] && [ "$podStatus" != "Completed" ] && [ "$podStatus" != "Succeeded" ];
        then
          echo "$eachPod | $podStatus"
      fi
  done  
done
