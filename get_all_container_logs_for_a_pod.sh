POD_NAME=$1
currentContainers=$(kubectl get pod $POD_NAME -o jsonpath={.spec.containers[*].name})
  arrayOfContainers=($currentContainers)
  for eachContainer in "${arrayOfContainers[@]}"; do 
      kubectl logs $POD_NAME -c $eachContainer > Logs/$POD_NAME$eachContainer.txt
done
