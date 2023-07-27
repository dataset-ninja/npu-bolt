Dataset **NPU-BOLT** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/Y/n/7g/xnCLFdRZXoiqoVhM1SfBwFg2DkGXenB4qHvX9Iti9ZKFcQ57B37P0EWnv8FQrDsK7D6t5BKwrzUwAQtchkdErWakePb6k31HV1y76HAbbHx32LlkU6r6QokV8gZJ.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='NPU-BOLT', dst_path='~/dtools/datasets/NPU-BOLT.tar')
```
The data in original format can be 🔗[downloaded here](https://www.kaggle.com/datasets/yartinz/npu-bolt/download?datasetVersionNumber=3)