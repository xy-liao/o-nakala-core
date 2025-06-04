python nakala-client-upload.py --mode folder --dataset "sample_dataset" --folder-config "sample_dataset/folder_data_items.csv" --api-key "aae99aba-476e-4ff2-2886-0aaf1bfa6fd2"


python nakala-client-collection.py --api-key "aae99aba-476e-4ff2-2886-0aaf1bfa6fd2" --from-folder-collections "sample_dataset/folder_collections.csv" --from-upload-output "output.csv" --collection-report "collections_output.csv"