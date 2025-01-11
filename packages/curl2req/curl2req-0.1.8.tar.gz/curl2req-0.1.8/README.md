# curl2req

把浏览器请求转换为 requests 请求的工具

## 用法

1 打开浏览器F12，右键 Copy -> Copy as cURL (bash)
2 把请求保存到文件，例如 `.curl`
3 运行命令
```python
from curl2req import curl_to_req

curl_to_req('./.curl', "", ".res", output_file_prefix="samples-res-")
```
4 查看结果
vim .res/samples-res-xxx.json

5 查看 json 结构

```python
from curl2req import get_json_paths
keys = get_json_paths(host, show=False)
for k in keys:
    k2 = k.replace('[]', '[0]')
    print(k, json_get_data(host, k2)[0])
```

## 上传

```bash
pip install build
rm -rf dist/* && python -m build
twine upload dist/*

pip install -e .
```
