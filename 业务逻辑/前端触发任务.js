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
