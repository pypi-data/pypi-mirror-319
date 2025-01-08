# 统一云存储接口

## 概述

统一云存储接口（Unified Cloud Storage Interface，简称 UCSI）是一个开源工具，旨在为各种云存储服务提供统一的 API。无论您使用的是 Google Drive、Dropbox、OneDrive 还是其他任何云存储服务，UCSI 都能抽象掉不同 API 的复杂性，使开发者能够通过一个一致的接口与多个云存储服务进行交互。

## 功能特点

- **统一 API**：通过一个 API 与多个云存储服务进行交互。
- **可扩展性**：通过实现提供的接口，轻松添加对新云存储服务的支持。
- **文件管理**：在不同的云存储服务之间上传、下载、删除和列出文件。
- **权限管理**：统一管理不同云存储服务的权限和访问控制。
- **跨平台支持**：支持多种编程语言和平台，方便集成到现有项目中。

## 安装

### 使用 pip 安装

```bash
pip install fundrive
```

### 从源码安装

```bash
python install git+https://github.com/farfarfun/fundrive.git
```

## 快速开始

以下是一个简单的示例，展示如何使用。

```python
from fundrive import LanZouDrive, AlipanDrive, GiteeDrive, GithubDrive, OSSDrive

drive = LanZouDrive()
drive = AlipanDrive()
drive = GiteeDrive()
drive = GithubDrive()
drive = OSSDrive()

drive.login('***每个网盘需要的东西不一样***')

# 上传
drive.upload_file(local_path="./download", fid=888666)
# 下载文件
drive.download_file(fid=888666, local_dir='./download')
# 下载文件夹
drive.download_dir(fid=888666, local_dir="./download")
# 获取目录下的所有目录
drive.get_dir_list(fid=888666)
# 获取目录下的所有文件
drive.get_file_list(fid=888666)
# 删除某个文件
drive.delete(fid=888666)
# 某个文件是否存在
drive.exist(path='upload/README.md')
# 分享
drive.share("root", password="123456", expire_days=1)
# 转存
drive.save_shared("https://www.aliyundrive.com/s/kXLX7XLXLXL", "root")
```

## 支持的云存储服务

| 序号 | 网盘             | 支持内容          | 对应的包 |
| :--: | :--------------- | :------------- | :-- | 
|  1   | [蓝奏云](src/fundrive/drives/lanzou/README.md)     | 上传/下载/删除    |fundrive-lanzou | 
|  2   | [OSS](src/fundrive/drives/oss/README.md)           | 上传/下载/删除   | fundrive[oss] |
|  3   | [github](src/fundrive/fungit/README.md)            | 上传/下载/删除   | fundrive |
|  4   | [gitee](src/fundrive/fungit/README.md)             | 上传/下载/删除   | fundrive |
|  5   | [阿里云盘](src/fundrive/drives/alipan/README.md)     | 上传/下载/删除   | fundrive[alipan] |
|  6   | [百度网盘](src/fundrive/drives/baidu/README.md)      | 上传/下载/删除   | fundrive[baidu] |
|  7   | [谷歌网盘](src/fundrive/drives/google/README.md)     | TODO           | fundrive |
|  8   | [Dropbox](src/fundrive/drives/dropbox/README.md)   | TODO            | fundrive |
|  9   | [OneDrive](src/fundrive/drives/onedrive/README.md) | TODO            | fundrive |
|  10  | [Amazon](src/fundrive/drives/amazon/README.md)     | TODO            | fundrive |

- 更多服务即将推出...



## 资源汇总

### [acoooder/aliyunpanshare](https://github.com/acoooder/aliyunpanshare)

狗狗盘搜网站：https://gogopanso.com

全量影视资源：https://link3.cc/alipan

今日新增资源：https://link3.cc/zuixin



## 贡献

我们欢迎任何形式的贡献！如果您想为 UCSI 做出贡献，请遵循以下步骤：

1. Fork 项目仓库。
2. 创建一个新的分支 (`git checkout -b feature/your-feature-name`)。
3. 提交您的更改 (`git commit -am 'Add some feature'`)。
4. 推送到分支 (`git push origin feature/your-feature-name`)。
5. 创建一个新的 Pull Request。

<!-- 
## 许可证

本项目采用 MIT 许可证。有关更多信息，请参阅 [LICENSE](LICENSE) 文件。
 -->

## 联系我们

如果您有任何问题或建议，请通过 [issues](https://github.com/farfarfun/fundrive/issues) 或 [email](1007530194@qq.com) 联系我们。

---

感谢您使用统一云存储接口！我们希望这个工具能够简化您的云存储集成工作。



#参考
百度云盘的 python-api，[官方 API](https://openapi.baidu.com/wiki/index.php?title=docs/pcs/rest/file_data_apis_list)  
蓝奏云的 python-api [参考](https://github.com/zaxtyson/LanZouCloud-API)
