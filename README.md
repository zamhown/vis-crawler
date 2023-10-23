# vis-crawler
数据可视化论文列表爬虫
## 运行环境
* Python3
* 需要Requests、Pandas等第三方包

## 使用方法
### VIS 论文
在项目根目录执行：
```
python vis.py [start [end]]  
```
（方括号表示可选参数）  
* `start`：开始年份，默认值为 2022
* `end`：结束年份，默认值为 2022

该脚本会爬取这段时间范围内的论文列表，并自动写入以下 3 种类型的文件：
- csv 表格文件
- md 表格文件
- json 原始数据文件

这些文件将存入`./data`目录。
