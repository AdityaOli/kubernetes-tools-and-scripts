import subprocess
import os

def compare_clusters(namespace):
    ftc_pods=get_all_pods('cluster1',namespace)
    ldv_pods=get_all_pods('cluster2',namespace)      
      
    ftc_pod_names=[]
    ldv_pod_names=[]
      
    for podline in ftc_pods:
        pod=podline.split(' ')[0]
        if "snmp-trap" not in pod and "health-check" not in pod and "NAME" not in pod and pod!='':
            pod=pod.split("-")
            pod='-'.join([str(x) for x in pod[:len(pod)-2]])
            ftc_pod_names.append(pod)
    
    for podline in ldv_pods:
        pod=podline.split(' ')[0]
        if "snmp-trap" not in pod and "health-check" not in pod and "NAME" not in pod and pod != '':
            pod=pod.split("-")
            pod='-'.join([str(x) for x in pod[:len(pod)-2]])
            ldv_pod_names.append(pod)
            
    unique_ftc_pods = list(set(ftc_pod_names))
    for eachPod in unique_ftc_pods:
        if eachPod in ldv_pod_names:
            print(eachPod)
            print("Cluster2 :"+str(ldv_pod_names.count(eachPod)))
            print("Cluster1 :"+str(ftc_pod_names.count(eachPod)))
        else:
            print(eachPod+" NotFound In LDV")
    print("Total Cluster1 Pods Are : "+str(len(ftc_pod_names)))
    print("Total Cluster2 Pods Are : "+str(len(ldv_pod_names)))

     
      
def get_all_pods(cluster,namespace):
      os.system('export PATH=/home/user:$PATH')
      out=subprocess.Popen(['Login command to the cluster'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      out, err = out.communicate()
      out=subprocess.Popen(['kubectl', 'get','pods','-n',namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      out, err = out.communicate()
      return(out.split("\n"))      
        
def main():
    namespace=["namespace1","namespace2","namespace3","namespace4..."]
    for eachNamespace in namespace:
        print("========== Checking for namespace : "+eachNamespace)
        compare_clusters(eachNamespace)
    
if __name__ == "__main__":
    main()
    
