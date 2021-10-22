# Performance tuning experimentation

I wanted to start tuning the resourse usage and the performance of the application to prepare for the production deployment. I wanted to create a fresh virtual machine with the resourses i expect our production server to have. To do this i decided to use vagrant which i learned to use back in the [server management course](https://heiskanen.rocks/server_management/h1). With vagrant i am able to essentially define the setup process so i wont have to redo it if i need to start from scratch. Here is the Vagrantfile i created to define the machine i am going to use for testing.

```ruby
$setup = <<SETUP
sudo usermod
apt update -y
apt install bash-completion docker-compose docker -y
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
usermod -a -G docker vagrant
systemctl start docker
sudo -u vagrant git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project
sudo -u vagrant docker-compose build
sudo -u vagrant docker-compose up -d
SETUP

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provision "shell", inline: $setup
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 1
  end
end
```

This will setup all the docker stuff, forward the 800 port, build the project and assign 2gb of memory and 1 cpu core to the machine. I tried running `ApacheBench` from my WSL ubuntu terminal but with kinda high concurrency but that just gives me the following error.

```powershell
heiskane@DESKTOP-BE6A02N:/mnt/c/Users/Heiskane$ ab -c 100 -n 1000 http://localhost:8000/async_books/
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
apr_socket_recv: Transport endpoint is not connected (107)
```

Apparently this some weird behaviour with wsl or something so instead of debugging that i looked for an alternative. After a few searches i decided to use [loadtest](https://github.com/alexfernandez/loadtest) that can be installed with `npm`. I ran a simple benchmark first just to see what the output looks like and to make sure it works. ps I had 20 books in the database for these tests.

```bash
PS C:\Users\Heiskane> loadtest -c 10 -n 100 http://localhost:8000/async_books/
INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
INFO
INFO Target URL:          http://localhost:8000/async_books/
INFO Max requests:        100
INFO Concurrency level:   10
INFO Agent:               none
INFO
INFO Completed requests:  100
INFO Total errors:        0
INFO Total time:          1.3902506000000001 s
INFO Requests per second: 72
INFO Mean latency:        133.5 ms
INFO
INFO Percentage of the requests served within a certain time
INFO   50%      125 ms
INFO   90%      204 ms
INFO   95%      226 ms
INFO   99%      287 ms
INFO  100%      287 ms (longest request)
```

I have omitted the timestamps here to make the output easier to read. I tried higher concurrency which was giving errors in WSL and it seems to work just fine now.

```bash
PS C:\Users\Heiskane> loadtest -c 100 -n 1000 http://localhost:8000/async_books/
INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
INFO Requests: 336 (34%), requests per second: 67, mean latency: 1261.2 ms
INFO Errors: 55, accumulated errors: 55, 16.4% of total requests
INFO Requests: 669 (67%), requests per second: 67, mean latency: 1545.8 ms
INFO Errors: 41, accumulated errors: 96, 14.3% of total requests
INFO
INFO Target URL:          http://localhost:8000/async_books/
INFO Max requests:        1000
INFO Concurrency level:   100
INFO Agent:               none
INFO
INFO Completed requests:  1000
INFO Total errors:        136
INFO Total time:          14.697792600000001 s
INFO Requests per second: 68
INFO Mean latency:        1417.9 ms
INFO
INFO Percentage of the requests served within a certain time
INFO   50%      1378 ms
INFO   90%      2011 ms
INFO   95%      2469 ms
INFO   99%      2944 ms
INFO  100%      3063 ms (longest request)
INFO
INFO  100%      3063 ms (longest request)
INFO
INFO   500:   121 errors
INFO    -1:   15 errors
```

Looking at the results i am getting some errors because i am running out database sessions so i will try to fix that in a moment. Also the results are not great even though this endpoint is using asynchronous code but compared to the "normal" endpoint it is much better.

```bash
PS C:\Users\Heiskane> loadtest -c 100 -n 1000 http://localhost:8000/books/
INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
INFO Requests: 129 (13%), requests per second: 26, mean latency: 2043.7 ms
INFO Errors: 53, accumulated errors: 53, 41.1% of total requests
INFO Requests: 256 (26%), requests per second: 25, mean latency: 4172 ms
INFO Errors: 25, accumulated errors: 78, 30.5% of total requests
INFO Requests: 370 (37%), requests per second: 23, mean latency: 3891.3 ms
INFO Errors: 30, accumulated errors: 108, 29.2% of total requests
INFO Requests: 528 (53%), requests per second: 32, mean latency: 3651 ms
INFO Errors: 50, accumulated errors: 158, 29.9% of total requests
INFO Requests: 652 (65%), requests per second: 25, mean latency: 3764.6 ms
INFO Errors: 36, accumulated errors: 194, 29.8% of total requests
INFO Requests: 774 (77%), requests per second: 24, mean latency: 3821.1 ms
INFO Errors: 43, accumulated errors: 237, 30.6% of total requests
INFO Requests: 903 (90%), requests per second: 26, mean latency: 3968.3 ms
INFO Errors: 50, accumulated errors: 287, 31.8% of total requests
INFO
INFO Target URL:          http://localhost:8000/books/
INFO Max requests:        1000
INFO Concurrency level:   100
INFO Agent:               none
INFO
INFO Completed requests:  1000
INFO Total errors:        294
INFO Total time:          38.726151599999994 s
INFO Requests per second: 26
INFO Mean latency:        3674.5 ms
INFO
INFO Percentage of the requests served within a certain time
INFO   50%      3963 ms
INFO   90%      5403 ms
INFO   95%      5709 ms
INFO   99%      6860 ms
INFO  100%      6983 ms (longest request)
INFO
INFO  100%      6983 ms (longest request)
INFO
INFO   500:   294 errors
```

So what to do now? Well i looked at the memory usage in the docker containers and saw it was pretty low even with 150 max connections in postgres so time to crank up those numbers.

```bash
CONTAINER ID   NAME                      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O        PIDS
ddec2205f8d6   bookstore-project_api_1   0.25%     227.5MiB / 1.941GiB   11.44%    6.14GB / 198MB   28.9MB / 0B      21
59ca56d5b3c6   bookstore-project_db_1    0.00%     324MiB / 1.941GiB     16.30%    110MB / 6.13GB   1.06MB / 125MB   157
```

I set the `max_connections` in postgres to 300 and gave both database engines (sync and async) 150 connection pool. Running the tests again a few times shows that the performance for `/books/` did not change much at all but for `/async_books/` the mean latency dropped to around 1200ms. Bringing the concurrency up to 200 show mean latency of 2240ms for `/async_books/` and 5668ms for `/books/`. Certainly not great results and i am still getting some errors so now i will try to bring the max session up to 500 but keep the pools the way they are at 150. This feels like it made things more inconsistent but i am getting slightly less errors. I tried to connect to postgres from the commandline but got an error saying `sorry, too many clients already`. Seems like the async engine is still using way more connections that what is assigned to it in the pool. I wanted to see what would happen if i just kept bringing up the amount of connections so i set the max connections to 1000 in postgres and gave both engines 300 connections in the pool. I am not expecting to get much out of this because at this point there is probably some bottleneck somewhere but i still wanted to try. Somehow the `/books/` endpoint only got slower but `/async_books/` did improve a bit although the results are still not great.

```bash
PS C:\Users\Heiskane> loadtest -c 200 -n 1000 http://localhost:8000/async_books/
INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
INFO Requests: 455 (46%), requests per second: 91, mean latency: 1636.5 ms
INFO Errors: 135, accumulated errors: 135, 29.7% of total requests
INFO Requests: 863 (86%), requests per second: 82, mean latency: 2397.4 ms
INFO Errors: 30, accumulated errors: 165, 19.1% of total requests
INFO
INFO Target URL:          http://localhost:8000/async_books/
INFO Max requests:        1000
INFO Concurrency level:   200
INFO Agent:               none
INFO
INFO Completed requests:  1000
INFO Total errors:        165
INFO Total time:          11.076019700000002 s
INFO Requests per second: 90
INFO Mean latency:        2041.2 ms
INFO
INFO Percentage of the requests served within a certain time
INFO   50%      2114 ms
INFO   90%      3406 ms
INFO   95%      3474 ms
INFO   99%      3669 ms
INFO  100%      4082 ms (longest request)
INFO
INFO  100%      4082 ms (longest request)
INFO
INFO    -1:   165 errors
```

During this test i the output of `docker stats` and it shows that most of the cpu was utilized and the memory usage got up to aroung 1.3gb which is about as high as i would want it to go because this does not include the overhead of the virtual machine running these containers.

```bash
CONTAINER ID   NAME                      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O        PIDS
5b2d7a476361   bookstore-project_db_1    21.06%    1.043GiB / 1.941GiB   53.75%    20.9MB / 1.48GB   53.3MB / 688kB   533
125dd7850b2a   bookstore-project_api_1   75.88%    292.7MiB / 1.941GiB   14.72%    1.49GB / 45.9MB   63.4MB / 0B      21
```

I ran `free -m` to look at how much memory i had left and it wasnt looking too good.

```bash
vagrant@vagrant:~/Bookstore-Project$ free -m
              total        used        free      shared  buff/cache   available
Mem:           1987        1674          98          53         214         107
Swap:           979          38         941
```

I think this might explain why `/books/` was only getting slower. Either way i want to start bringing the numbers down a bit to make sure the server wont run out of memory. During the tests i was also looking at max connections in postgres.

```sql
bookstore_db=# SELECT COUNT(pid) FROM pg_stat_activity;
 count
-------
   545
(1 row)
```

Seems like amount of sessions got up to 545 during this so 1000 max connections in postgres is a bit overkill. Also i dont have enough memory for that anyway. At this point it definitely feels like i am getting somewhere but the main issue is that i dont really know where all of this ram is going. I see that its the database container that uses it what is it used for? I see that my api container keeps printing `INFO sqlalchemy.engine.Engine [cached since 4.835s ago] ()` so its definitely doing some caching but what is it caching? I looked a bit at the [sqlalchemy documentation](https://docs.sqlalchemy.org/en/14/core/connections.html#sql-compilation-caching) and it seems like it is caching the sql queries. The size of the cache by default is 500 (statements i think?). But the thing is that im running the same query everytime so is it not the caching that is eating my memory or is every session using its own cache? Probably not but where is my memory going? Do i have a memory leak? Is it just normal python stuff? I do know that my code should close the sessions when they are done so i guess it shall remain a mystery for now. I do want to get this to a reasonable state tonight so ill go back and set the max connections to 600 in postgres and give the sync engine 150 connections in the pool.

Earlier when i set the concurrency to 200 i got high latency on `/books/` then tried running the test again but its was taking so long i just canceled it. Well i did the same thing now except i let the second test finish and got mean latency of 79721ms. Clearly the normal sync engine is just never going to handle that load with these resourses but running the same test (200 concurrency, 1000 requests) on the `/async_books/` endpoint a few times got mean latency of 1917ms at best. Not great but to be fair if we were getting that kind of traffic we could probably afford a better server. The real point of this is to squeeze all the performance we can get out of a server we can afford right now. I looked at some stats during the tests and saw all 600 connections being used in postgres and all of the memory being used by the vm. Out of curiosity i tried running the test on the async endpoint with 400 concurrency before starting to bring down the amount of connections.

```bash
PS C:\Users\Heiskane> loadtest -c 400 -n 1000 http://localhost:8000/async_books/
INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
INFO
INFO Target URL:          http://localhost:8000/async_books/
INFO Max requests:        1000
INFO Concurrency level:   400
INFO Agent:               none
INFO
INFO Completed requests:  1000
INFO Total errors:        696
INFO Total time:          4.5539912000000005 s
INFO Requests per second: 220
INFO Mean latency:        1293.4 ms
INFO
INFO Percentage of the requests served within a certain time
INFO   50%      154 ms
INFO   90%      3874 ms
INFO   95%      4047 ms
INFO   99%      4261 ms
INFO  100%      4324 ms (longest request)
INFO
INFO  100%      4324 ms (longest request)
INFO
INFO   500:   81 errors
INFO    -1:   615 errors
```

Well the mean latency is pretty good for this many requests but that is only because 69% of the requests just got 500 errors. I brought the max connections down to 400 and started blasting the backend to see how much memory it would use.

```bash
CONTAINER ID   NAME                      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O         PIDS
aeb21c18be00   bookstore-project_db_1    0.00%     811.2MiB / 1.941GiB   40.81%    143MB / 6.42GB   44.8MB / 2.13MB   407
92e2859336c4   bookstore-project_api_1   0.25%     345.2MiB / 1.941GiB   17.37%    6.43GB / 226MB   69.1MB / 0B       21

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────Every 2.0s: free -m
              total        used        free      shared  buff/cache   available
Mem:           1987        1372         104          34         510         430
Swap:           979         111         868
```

It seems to have used most of the memory but atleast nothing is crashing so i think it is reasonable considering this load is much much higher than we are expecting for this small school project. I did try running the test with 200 concurrency for 10000 requests on `/authors/` which currently just returns one author.

```bash
PS C:\Users\Heiskane> loadtest -c 200 -n 10000 http://localhost:8000/authors/
INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
INFO Requests: 1116 (11%), requests per second: 224, mean latency: 752.5 ms
INFO Errors: 540, accumulated errors: 540, 48.4% of total requests
INFO Requests: 2406 (24%), requests per second: 258, mean latency: 825.4 ms
INFO Errors: 538, accumulated errors: 1078, 44.8% of total requests
INFO Requests: 3383 (34%), requests per second: 195, mean latency: 991 ms
INFO Errors: 299, accumulated errors: 1377, 40.7% of total requests
INFO Requests: 4462 (45%), requests per second: 216, mean latency: 908.4 ms
INFO Errors: 336, accumulated errors: 1713, 38.4% of total requests
INFO Requests: 5586 (56%), requests per second: 225, mean latency: 900.9 ms
INFO Errors: 396, accumulated errors: 2109, 37.8% of total requests
INFO Requests: 6747 (67%), requests per second: 232, mean latency: 875.7 ms
INFO Errors: 422, accumulated errors: 2531, 37.5% of total requests
INFO Requests: 7905 (79%), requests per second: 232, mean latency: 883.8 ms
INFO Errors: 505, accumulated errors: 3036, 38.4% of total requests
INFO Requests: 9194 (92%), requests per second: 258, mean latency: 753.6 ms
INFO Errors: 521, accumulated errors: 3557, 38.7% of total requests
INFO
INFO Target URL:          http://localhost:8000/authors/
INFO Max requests:        10000
INFO Concurrency level:   200
INFO Agent:               none
INFO
INFO Completed requests:  10000
INFO Total errors:        3821
INFO Total time:          43.0511569 s
INFO Requests per second: 232
INFO Mean latency:        852.9 ms
INFO
INFO Percentage of the requests served within a certain time
INFO   50%      1009 ms
INFO   90%      1566 ms
INFO   95%      1717 ms
INFO   99%      1942 ms
INFO  100%      2572 ms (longest request)
INFO
INFO  100%      2572 ms (longest request)
INFO
INFO   500:   1127 errors
INFO    -1:   2694 errors
```

The mean latency is pretty reasonable with this low amount of data even with the normal sync engine although the amount of errors if fairly high at this concurrency. Finally i wanted to end with something more reasonable so i set the concurrency to 50 and the `/books/` endpoint is still getting quite high latency at about 2100ms but errors are now in single digits. Im not sure how much i want to use the async engine in this project because of the way i would have to deal with database relationships but right now it seems that i want to use it atleast for getting the books from the database. This is because the async code seems to benefit the most when fetching the data is slow like when getting a large amount of books as seen in these results yet again.

```bash
PS C:\Users\Heiskane> loadtest -c 50 -n 1000 http://localhost:8000/async_books/
INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
INFO Requests: 362 (36%), requests per second: 72, mean latency: 613.3 ms
INFO Requests: 751 (75%), requests per second: 78, mean latency: 666.8 ms
INFO
INFO Target URL:          http://localhost:8000/async_books/
INFO Max requests:        1000
INFO Concurrency level:   50
INFO Agent:               none
INFO
INFO Completed requests:  1000
INFO Total errors:        0
INFO Total time:          12.9097025 s
INFO Requests per second: 77
INFO Mean latency:        635.8 ms
INFO
INFO Percentage of the requests served within a certain time
INFO   50%      641 ms
INFO   90%      905 ms
INFO   95%      1025 ms
INFO   99%      1211 ms
INFO  100%      1263 ms (longest request)
```

Im not sure what this is going to look like when the requests are not just going over a local network but based on these results i would say that at 50 concurrency the latency should be reasonable.