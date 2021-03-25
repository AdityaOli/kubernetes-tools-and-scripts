ssh-keygen
LIST_OF_FIRST_CLUSTER_NODES=(node1 node2 node3)
LIST_OF_SECOND_CLUSTER_NODES=(node4 node5 node6)

for server in "${LIST_OF_FIRST_CLUSTER_NODES[@]}"; do 
    APPEND_STRING="user@$server"
    ssh-copy-id $server
done

for server in "${LIST_OF_SECOND_CLUSTER_NODES[@]}"; do 
    APPEND_STRING="user@$server"
    ssh-copy-id $server
done
