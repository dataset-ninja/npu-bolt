Dataset **NPU-BOLT** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/f/e/7E/6gkz6Tbl8zNQEtlcv6024b0vmLmUQ2dprqPtVuwDpIlQsTUjb92ZRDHVfligb92qUMkATMy3KyUbKJzDTFtcIqtFcGEre8F84ZaBo5X4dgEPGwFOen0YDSu5w4GF.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='NPU-BOLT', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/yartinz/npu-bolt/download?datasetVersionNumber=3).