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

##Architcture
Below is the architecture of the entire operation.
![FLowchart](/Flowchart.jpg)

The GCP architecture goes as below.
![Architecture](/GCP_Arch.png)






