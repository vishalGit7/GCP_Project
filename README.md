# GCP_Project

This Repository Contains source code data ingestion from GCS(GOOGLE CLOUD STORAGE) TO BIGQUERY.
It uses CLOUD RUN SERVICE for loading the files.

```
This Repo follows below directory strcture 
├── .github
│   ├── workflows
      ├──CI/CD Yaml files
├── infra
│   ├── cloudbuild files
│   ├── terraform files
├── script
  ├── python script files
└── README.md
```

## .github - 
This folder contains CID/CD action files which are resposibile for creating and destroying infrastrcture.

## infra - 
This folder contains source code for creating and destoring infrastrcture.

## script - 
This folder contains python script and dockerfile related files for creating cloud build image.

## Architcture
Below is the architecture of the entire operation.
![FLowchart](/Flowchart.jpg)

The GCP architecture goes as below.


![Architecture](/GCP_Arch.png)

## Deployment 
On executing deploy_cr_gcs_to_bq.yaml to create the infrastructre , Below resources gets created
1)An IAM service account with required permissions.
2)Cloud build trigger to create dockerimage and deploy the cloud run.
3)GCS bucket and landing folder
4)Bigquery Dataset and table.

![Infra](/Deploy_infra.PNG)

![deploy](/terraform.PNG)

## Testing 

1)Load a new file to GCS landing bucket.
![GCS](/GCS.PNG)

2)The cloud gets triggered on event.
![event](/trigger.PNG)

3)File gets loaded to BQ.
![Bq](/BQ.PNG)






