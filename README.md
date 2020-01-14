## Kube Context Switcher (GKE/Openshift)

This script assists with the headache of switching between kubernetes clusters on two different
platforms (GKE and Openshift). When switching between GCP Projects and/or Openshift clusters,
k8s gets really confused. Also not helping is Google logging you out frequently, and seems
to be unable to be logged into two different projects at the time.

Running this prompt/wizard based system gets you to the cluster you need and quickly.

There are a lot of unclosed if statements simply because the pick module only lets
you choose certain values, so its impossible to use any value that does not comply.

Prereqs:
- python3
- pick module (pip3 install pick)
- Credentials and permissions to the saas-rally-prod and saas-rally-dev projects
- Credentials and permissions from Active Directory to dev and prod Openshift clusters
- Google Cloud SDK (https://cloud.google.com/sdk/install)
- OC (0penshift Kubectl) (https://github.com/openshift/origin/releases)
