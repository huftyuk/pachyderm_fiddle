# pachyderm_fiddle
A simple play at this

# Setup a kubernetes cluster 
First thing you need to do is setup a kubernetes cluster.  This is all based on the instructions in 

CLUSTER_NAME="pach-cluster"

GCP_ZONE="us-west1-a"

gcloud config set compute/zone ${GCP_ZONE}

gcloud config set container/cluster ${CLUSTER_NAME}

MACHINE_TYPE="n1-standard-2"

--By default the following command spins up a 3-node cluster. You can change the default with `--num-nodes VAL`.

gcloud container clusters create ${CLUSTER_NAME} --scopes storage-rw --machine-type ${MACHINE_TYPE}

--once up and running.

kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value account)

# Create a storage bucket
-- Storage size in gb

STORAGE_SIZE="2"

-- The Pachyderm bucket name needs to be globally unique across the entire GCP region.

BUCKET_NAME="huftyukpackyderm"

-- Create the bucket.

gsutil mb gs://${BUCKET_NAME}

# Run Pachyderm
-- Install pachyderm if it ins't already

curl -o /tmp/pachctl.deb -L https://github.com/pachyderm/pachyderm/releases/download/v1.9.0/pachctl_1.9.0_amd64.deb && sudo dpkg -i /tmp/pachctl.deb

-- And delpoy it

pachctl deploy google ${BUCKET_NAME} ${STORAGE_SIZE} --dynamic-etcd-nodes=1

-- And port forward, you may need to background this

pachctl port-forward &

# Create our initial repo
pachctl create repo trackparams

-- check it is there!

pachctl list repo

# Create our pipeline
pachctl create pipeline -f https://raw.githubusercontent.com/huftyuk/pachyderm_fiddle/master/pipelines/ProcessTrackParams.json

# Then add a file to the repo
pachctl put file trackparams@master:test1.txt -f https://raw.githubusercontent.com/huftyuk/pachyderm_fiddle/master/paramfiles/track

this will run the pipeline and we can then look at the result.

pachctl list file track2@master

pachctl get file track2@master:test1.txt

