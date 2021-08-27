# Redis的k8s配置

## 参考

[Docker Hub | Redis official](https://hub.docker.com/_/redis/)
[Redis Official](https://redis.io/)
[Kubernetes | API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/)
[博客园 | k8s部署单节点redis](https://blog.csdn.net/xujiamin0022016/article/details/109763447)

## 配置思路

通过`ConfigMap`添加redis的配置文件`redis.conf`，在`Deployment`中添加`volumn`将`ConfigMap`的内容映射为数据卷，然后通过`volumnMounts`将该数据卷映射为`redis`容器中的文件，在启动redis时，使用`sh`执行命令`redis-server <config-file-path>`来指定配置文件的位置并启动redis。这样，我们就可以在ConfigMap中修改redis的配置文件来修改配置了，配置的具体项目可以参考其[自描述配置](https://raw.githubusercontent.com/redis/redis/6.0/redis.conf)，或者从[Redis Official | 配置](https://redis.io/topics/config)查看不同版本的自描述配置文件列表。因为其自描述配置文件太长了，放到k8s的配置里不太合适，所以就将需要的配置添加进来即可。

但是此时产生一个问题，当仅更改`ConfigMap`但是不更改`Deployment`部分时，`Deployment`不会自动重启，这意味着修改的配置不会生效（redis并不会自动监测配置文件的更改），所以我们需要手动重启`Deployment`。为了解决这个问题，我们引入一个Reloader，参考[GitHub | Reloader](https://github.com/stakater/Reloader)。为`Deployment`添加`annotation`来帮助`Reloader`确定重启的监视关系（key为`configmap.reloader.stakater.com/reload`，value为`ConfigMap`的name）。这样一来，当我们仅仅更新`ConfigMap`，`Deployment`也会进行重启更新。

为redis容器添加了就绪探针（readinessProbe）和存活探针（livenessProbe）。就绪探针前者主要用于滚动更新，使得滚动更新时新启动的pod在可以正常服务后才会关闭旧pod。存活探针主要用于pod无法提供服务时及时进行重启。

为redis分配了`128MiB`的内存，在`k8s`和`redis`的配置中都有进行限制，如果不够，以后再加。




