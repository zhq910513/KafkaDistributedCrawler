// 可能传递参数如下：
// 任务ID
// 初始化任务链接
// 子节点列表
// 部署类型 # TODO 默认Scrapy / 直接部署项目
// 数据落库 # TODO 数据类型、数据库类型
// 安装爬虫环境 # TODO


fetch('http://main-node/api/start-task', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ taskId: '12345', taskData: 'some data' }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
