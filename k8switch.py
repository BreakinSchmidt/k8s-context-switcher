#!/usr/bin/env python3
#
# This script assists with the headache of switching between kubernetes clusters on two different
# platforms (GKE and Openshift). When switching between GCP Projects and/or Openshift clusters,
# k8s gets really confused. Also not helping is Google logging you out frequently, and seems
# to be unable to be logged into two different projects at the time.
#
# Running this prompt/wizard based system gets you to the cluster you need and quickly.
#
# There are a lot of unclosed if statements simply because the pick module only lets
# you choose certain values, so its impossible to use any value that does not comply.
#
# Prereqs:
# - python3
# - pick module (pip3 install pick)
# - Credentials and permissions to the saas-rally-prod and saas-rally-dev projects
# - Credentials and permissions from Active Directory to dev and prod Openshift clusters
# - Google Cloud SDK (https://cloud.google.com/sdk/install)
# - OC (0penshift Kubectl) (https://github.com/openshift/origin/releases)
#
# Matt Schmidt - 1/14/2020

import os
from pick import pick

# This function queries the list of clusters in a datacenter, parses them, and shoves them into a dict.

def gke_cluster_table(region):
    table = os.popen('gcloud container clusters list | grep ' + region + ' | grep -v NAME | tr -s " " | cut -d " " -f 1,2').read()
    table = table[:-1]
    table = {key: str(val) for key, val in (item.split(' ')
                   for item in table.split('\n'))}
    return table

# This function uses gcloud to log you into the correct GCP project and lets you select
# the active cluster based on your project and region

def gke_platform():
    title = 'Neat, in which data center are you trying to fuck up GKE?'
    options = ['gi', 'gc', 'gidev', 'gcdev']
    datacenter, index = pick(options, title)
    print(datacenter)

    gcp_username = input('Enter your GCP username prefix (usually firstname.lastname): ')

    if datacenter == 'gi' or datacenter == 'gidev':
        region = 'central'

    if datacenter == 'gc' or datacenter == 'gcdev':
        region = 'east'

    if datacenter == 'gi' or datacenter == 'gc':
        gcp_username_suffix= 'saas.broadcom.com'
        gcp_project = 'saas-rally-prod'

    if datacenter == 'gidev' or datacenter == 'gcdev':
        gcp_username_suffix= 'saasdev.broadcom.com'
        gcp_project = 'saas-rally-dev'

    print('Logging into gcloud')

    os.system('gcloud auth login ' + gcp_username + '@' + gcp_username_suffix)

    print('Setting your GCP project to the correct location')

    os.system('gcloud config set project ' + gcp_project)

    gke_cluster_full = gke_cluster_table(region)
    gke_cluster_names = list(gke_cluster_full.keys())

    title = 'What cluster do you want to fuck up?'
    options = gke_cluster_names
    gke_cluster_name, index = pick(options, title)
    print(gke_cluster_name)

    gke_cluster_zone= gke_cluster_full[gke_cluster_name]

    print('Setting region/zone to ' + gke_cluster_zone)

    os.system('gcloud config set compute/zone ' + gke_cluster_zone)

    print('Setting kube config for ' + gke_cluster_name + 'in ' + gke_cluster_zone)

    os.system('gcloud container clusters get-credentials ' + gke_cluster_name)


# This function uses oc to log you into the correct Openshift cluster

def openshift_platform():
    title = 'Neat, in which data center are you trying to fuck up Openshift?'
    options = ['gi', 'gc', 'ai', 'an', 'test']
    datacenter, index = pick(options, title)
    print(datacenter)

    if datacenter in ('gi', 'gc', 'ai', 'an'):
        domain = 'rally.prod'

    if datacenter == 'test':
        domain = 'f4tech.com'
        datacenter = 'gcp'

    print('Alllllright let\'s get you logged into ' + datacenter)

    os.system('oc login --insecure-skip-tls-verify=true https://cluster.ose.' + datacenter + '.' + domain + ':8443')

def main():

    title = 'Let\'s switch kube contexts! GKE or Openshift?'
    options = ['GKE', 'Openshift']
    platform, index = pick(options, title)
    print(platform)

    if platform == 'GKE':
        gke_platform()

    if platform == 'Openshift':
        openshift_platform()

if __name__ == '__main__':
    main()
