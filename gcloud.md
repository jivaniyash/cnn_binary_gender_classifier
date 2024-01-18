## Instructions for deploying in GCP

1. Create a Project in Gcloud

[Optional Step = create VM instance to connect Mongo using this guide](#steps-for-creating-instance-in-vm) - if you are not creating VM instance, no need to configure Google Secret Manager (Step 11)

2. Create artifact repo & enable artifact api in Gcloud
    ```
    gcloud artifacts repositories create REPOSITORY \
        --repository-format=docker \
        --location=LOCATION \
        --description="DESCRIPTION" \
    ```

3. for Windows -- https://cloud.google.com/artifact-registry/docs/docker/

net localgroup docker-users DOMAIN\USERNAME /add
- DOMAIN is your Windows domain.
- USERNAME is your user name.

4. Download and Install Gcloud CLI for desktop version

5. Run `gcloud init` & `gcloud auth login`

6. if new artifact repo for new region, then run  
gcloud auth configure-docker <path to repo>
gcloud auth configure-docker us-east4-docker.pkg.dev

Build docker image from Dockerfile
docker build -t <image_name>
docker build -t tensorflow .

7. tag image 
<tag name> =  REPOSITORY of output => docker image ls
<path to repo> = HOST-NAME/PROJECT-ID/REPOSITORY/IMAGE

docker tag <tag name> <path to repo>

see new image using docker image ls

8. push image to registry
docker push <tag name/REPOSITORY>

9. open cloud run , create service - add this registry image to the service

10. Run code to deploy and start service in Google Cloud Run
```
gcloud run deploy <service_name> \
--image=<artifact_img_url> \
--allow-unauthenticated \
--port=8080 \
--service-account=<service_account> \
--memory=1Gi \
--cpu-boost \
--region=us-central1 \
--project=<project_name>
```

11. (Optional step) If VM instance is created for connecting db, Add secrets (.env) to secret managaer and grant access. 
Pass this arguments to gcloud_run commond - 
```
--set-env-vars= \
--set-secrets=env=<env_secret_name> 
```

---

## steps for creating instance in VM

this is completely optional

1. create new VM instance in gcp
- change boot disk to ubuntu 20.04LTS
- firewall -> allow http & https

2. create firewall rules
- targets = all instance in network
- source ip = 0.0.0.0/0   - please be sure that anyone can connect to the VM, so bind only specific IP address.
- protocols = tcp = 27017

3. connect to ssh using gcloud
    ```
    gcloud compute ssh --zone "us-central1-c" "<vm_name>" --project "<project_name"
    ```

https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
https://www.mongodb.com/docs/manual/tutorial/enable-authentication/

run following code to start mongo instance inside VM= 
```
sudo apt-get install gnupg curl
```

```
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

```
sudo apt-get update
```

```
sudo apt-get install -y mongodb-org
```

```
sudo systemctl start mongod
```

```
sudo systemctl status mongod
```

it should show (acitve running)


You can optionally ensure that MongoDB will start following a system reboot by issuing the following command
```
sudo systemctl enable mongod
```

`mongo` -> `show dbs`  to check mongo is running

to connect using different IP = 
`mongod --bind_ip 0.0.0.0`-please be sure that anyone can connect to the VM, so bind only specific IP address.

