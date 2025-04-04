import requests, threading

# requests.post('https://web-programming-course.onrender.com/messages', 'Johnny: What do you mean by OMG?')

threads = []
for i in range(10):
    t = threading.Thread(target=requests.get, args=('http://localhost:5000/sync',))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
    # print(t)
