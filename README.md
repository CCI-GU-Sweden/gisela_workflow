# gisela_workflow

create a file called .venv in the workflow/scripts directory. It should contain the following information:

WK_TOKEN = "the_access_toke_for_webknossos" #2024-07-04
WK_TIMEOUT="3600" # in seconds
ORG_ID = "the_org_id_for_the_webknossos" # gisela's webknossos

make sure you have a running snakemake in your environment. Either create one or use the workflow/envs/snakemake.yml file with conda

In th root directory run 

snakemake --profile ./profiles/with_conda all 

this downloads trining data and setsup a dataset for trining a  yolov8 model

In the same directory run 

snakemake --profile ./profiles/with_conda yolo_train_py 

this trains a yolov8 model

The file workflow/scripts/layers_config.json contains configuration data for the different annotations layers. if you supply --config current_confg=myelin for example, the configuration with short_name myelin will be used. Use the short_name of the configuration you would like to use.





